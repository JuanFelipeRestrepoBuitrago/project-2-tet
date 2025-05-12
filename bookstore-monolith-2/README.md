# Objective 2
Cloud scaling of a monolithic application, scaled on EC2 virtual machines on demand, with a highly available database.

## Objective Completion Features

- [x] Completed
- **Extension of objective 1**: This new objective continues with what was implemented in objective 1, separating the different functionalities under subdomains of the application.
- **Highly available database**: We used the Aurora and RDS service to deploy a highly available database in the cloud which integrates with our application, which will later allow for auto-scaling.
- **Load balancer**: a load balancer was implemented that will redirect traffic between multiple service instances, which is the central axis in our scaling strategy, since each instance works with a remote database, so there is no dependency between application instances, something that could not be achieved following the monolithic architecture approach in objective 1.
- **AWS Autoscaling**: An auto-scaling policy was implemented based on an image created from an EC2 instance, which defines that there can be between 1 to 6 application instances maximum, with a desired number of 2, which will increase on demand.
- **Domain**: [objective2.p2tet.duckdns.org](https://objective2.p2tet.duckdns.org) is the domain which points to the Monolithic application with autoscaling.

## Table of Contents
- [Objective 2](#objective-2)
- [Objective Completion Features](#objective-completion-features)
- [Bookstore Monolith](#bookstore-monolith)
- [Table of Contents](#table-of-contents)
- [Domain](#domain)
    - [Prerequisites](#prerequisites)
    - [Code changes](#code-changes)
- [Database configuration](#database-configuration)
- [NFS configuration](#nfs-configuration)
- [Load Balancer configuration](#load-balancer-configuration)
- [Autoscaling configuration](#autoscaling-configuration)
- [Set up Deployment](#set-up-deployment)
  - [Template VM](#template-vm)
  - [Installing Docker and Docker Compose](#installing-docker-and-docker-compose)
  - [Domain](#domain-1)
  - [Deploying the Application](#deploying-the-application)
  - [Create ALB Load Balancer in EC2](#create-alb-load-balancer-in-ec2)
  - [Create AMI from the template instance](#create-ami-from-the-template-instance)
  - [Create Auto Scaling Group](#create-auto-scaling-group)


# Bookstore Monolith
A simple bookstore application that allows users to view, add, update, and delete books. The application is built using Flask and uses a MySQL database to store book information, modified for the use of an external database.

## Domain

### Prerequisites
- Python 3.x (3.12.4 was the used version)
- Docker and Docker Compose

### Strategy
Our strategy to scale the monolithic application with auto-scaling was fundamentally divided into 3 steps:
1. Modify the code to use an external database, to decouple the dependency on another container running on the same machine.
2. Create a load balancer that distributes requests among multiple machines.
3. Assign an auto-scaling policy that, together with the load balancer, can adapt to different request flows.

### Code changes
The initial **Bookstore** application was a monolith that was deployed in two docker containers, one with the application and another with the database. This approach limited its scalability in that it depended on a database docker container on the same network. The first step in our scaling strategy was to decouple this relationship between the application and the database, using one in AWS, which guarantees us high availability and fault tolerance, thus fulfilling one of the requirements of this objective (more on the database will be discussed in its respective section).

The main changes in the code were:
1. Introduction of the setup_db file, which serves the function of creating the database if it is not already created.
2. Introduction of the **_bindings_** file whose main responsibility is to handle routing between reading and writing databases, since the selected database implements two different endpoints, one for reading and another for writing data.
3. Introduction of the **_config.py_** file that serves to select between using production and development database, to facilitate the development stage.
4. There were major changes to the **_extensions.py_** file, as it now initializes the application to use the routing functionality between database endpoints.
5. There were major changes to the **_app.py_** file, refactoring code to make it much simpler to use with the new functionality.

The following code snippets allow us to appreciate the core of the change made to support the new database:
```python
class RoutingSQLAlchemy(SQLAlchemy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.write_engine_url = None
        self.read_engine_url = None

    def init_app(self, app):
        """Initializes the application with DB routing support"""
        super().init_app(app)
        
        self.write_engine_url = app.config['SQLALCHEMY_DATABASE_URI_WRITE']
        self.read_engine_url = app.config['SQLALCHEMY_DATABASE_URI_READ']
        
        if not self.read_engine_url:
            self.read_engine_url = self.write_engine_url
            
        session = create_routing_session(self.write_engine_url, self.read_engine_url)
        
        self.session = session
```
```python
class RoutingSession(scoped_session):
    def __init__(self, write_session_factory, read_session_factory):
        """
        Initializes the routing session with factories for writing and reading
        """
        self.write_session_factory = write_session_factory
        self.read_session_factory = read_session_factory
        super().__init__(write_session_factory)

    def get_bind(self, mapper=None, clause=None):
        """
        Determines which database to use based on the type of operation
        """
        if self._flushing or self.info.get('writing'):
            return self.write_session_factory.kw['bind']
        else:
            return self.read_session_factory.kw['bind']

    def using_write_bind(self):
        """
        Marks the session to use the write endpoint
        """
        self.info['writing'] = True
        return self
    
    def remove(self):
        """
        Cleans up session references
        """
        self.info.pop('writing', None)
        super().remove()

def create_routing_session(write_engine_url, read_engine_url):
    """
    Creates a session that handles routing between read and write databases
    """
    write_engine = create_engine(write_engine_url, pool_recycle=3600)
    read_engine = create_engine(read_engine_url, pool_recycle=3600)
    
    write_session_factory = sessionmaker(bind=write_engine)
    read_session_factory = sessionmaker(bind=read_engine)
    
    return RoutingSession(write_session_factory, read_session_factory)
```

## NFS Configuration
1. Create the directory where the NFS will be mounted for example.
```bash
mkdir -p /home/ubuntu/nfs-mount
```
2. Mount the NFS file system to that directory.
```bash
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-00637b010660de0c0.efs.us-east-1.amazonaws.com:/ /home/ubuntu/nfs-mount
```

3. Add the volumen to the docker-compose.yaml.
```bash
volumes:
      - /home/ubuntu/nfs-mount:/app/static
```
## Database configuration
The characteristics provided by the database we created in AWS are:

**Architecture**

1. **Deployment topology**:
   * **3 instances** distributed across **3 different availability zones (AZs)** within an AWS region.
   * **Components**:
      * **AZ 1**:
         * **Primary instance**:
            * Responsible for **read/write operations**.
            * **SSD** storage (probably Amazon EBS optimized for high performance).
      * **AZ 2 and AZ 3**:
         * **Readable standby instances**:
            * Synchronized replicas of the primary instance.
            * **Read-only** (can handle read queries to offload the primary).
            * **SSD** storage.

2. **Endpoints**:
   * **Write Endpoint**:
      * Points to the primary instance in **AZ 1**.
      * Used for write operations (INSERT, UPDATE, DELETE).
   * **Reader Endpoint**:
      * Automatically balances read queries between standby instances in **AZ 2 and AZ 3**.
      * Ideal for analytical workloads or reports.

**Key Features**

| **Attribute** | **Detail** |
|--------------|-------------|
| **Availability** | **99.95% uptime** (AWS SLA for Multi-AZ). |
| **Redundancy** | Tolerance to complete AZ failure (if AZ 1 fails, a standby is promoted). |
| **Durability** | Data replicated **synchronously** to the primary and **asynchronously** to the standbys. |
| **Read Scalability** | Up to **2 readable instances** to distribute read loads. |
| **Write Latency** | Reduced thanks to SSD use and optimized replication. |

## Load Balancer configuration
A load balancer was created together with a target group to which all new instances of the application that are deployed will belong, this way it can distribute the workload among all of them.

## Autoscaling configuration
An auto-scaling policy was configured that creates new instances of the application to the target group, specifically a policy in which when 50 percent of CPU resources are consistently used for 300 seconds, a new instance of the application is created.

## Set up Deployment


### Template VM

We need a template of the application in a VM to be able to create new instances of the application, this template will be used to create the AMI that will be used in the auto-scaling policy.

1. Create an AWS account and log in to the AWS Management Console.
2. Navigate to the EC2 Dashboard and launch a new instance.
3. Choose an Ubuntu Server 20.04 LTS AMI.
4. Select an instance type (e.g., t2.micro for free tier).
5. Configure instance details, including network settings and security groups, to allow HTTP (port 80) and HTTPS (port 443) traffic.
6. Create a new key pair or use an existing one to access the instance.
7. Launch the instance and wait for it to be in the "running" state.

### Installing Docker and Docker Compose

1. Update the package list and install dependencies:
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```

2. Add Docker's official GPG key:
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker-archive-keyring.gpg
```
3. Set up the stable repository:
```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

4. Install Docker Engine:
```bash
sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io
```
5. Start and enable Docker:
```bash
sudo usermod -aG docker $USER && logout && sudo systemctl restart docker
```
6. Verify Docker installation:
```bash
docker --version
```
7. Verify Docker Compose installation:
```bash
docker compose --version
```

### Domain
Continue with the SSL certificate, domain and inverse proxy setup at [Reverse Proxy](../reverse-proxy/README.md)

### Deploying the Application
1. Clone the repository:
```bash
git clone https://github.com/JuanFelipeRestrepoBuitrago/project-2-tet.git
cd project-2-tet/bookstore-monolith-2
```

2. Run the application:
```bash
docker compose up -d
```

### Create ALB Load Balancer in EC2

1. Go to the EC2 Dashboard.
2. Click on "Load Balancers" in the left sidebar.
3. Click on "Create Load Balancer."
4. Choose "Application Load Balancer" with the ALB option.
5. Configure the load balancer:
   - Name: `your_name`
   - Scheme: `internet-facing`
   - IP address type: `ipv4`
   - Listeners: HTTP (port 80) and HTTPS (port 443)
   - Availability Zones: Select the VPC and subnets where your instances are going to be launched. You don't need to select the zone where the template is launched, since the load balancer will be responsible for distributing the traffic.
   - Security groups: Create a new security group or select an existing one that allows HTTP and HTTPS traffic. You can select the security group that was created for the template instance.
   - Listeners and routing: Create a new target group for the load balancer to route traffic to the instances. The listener is the port where our application will be listening, in this case port 80. The target group is the group of instances that will receive the traffic from the load balancer. You can create a new target group or select an existing one.
   - Register targets: You can skip this step for now, since we will register the targets later when we create the auto-scaling group.

### Create AMI from the template instance

1. Go to the EC2 Dashboard.
2. Click on "Instances" in the left sidebar.
3. Select the instance you want to create an AMI from.
4. Click on "Actions" > "Image and templates" > "Create image."
5. Fill in the details for the image:
   - Image name: `your_name`
   - Description: `your_description`
   - Volume: Select your volume and its settings.
6. Click on "Create image."

### Create Auto Scaling Group

1. Go to the EC2 Dashboard.
2. Click on "Auto Scaling Groups" in the left sidebar.
3. Click on "Create Auto Scaling group."
4. Choose the launch template you created earlier.
    - Select instance type you want to use for the auto-scaling group.
    - Select the security group you created for the template instance.
    - In advance template settings, mount a sh file that will run the application when the instance is launched.
    ```bash
    #!/bin/bash
    cd /home/ubuntu/project-2-tet/bookstore-monolith-2
    docker compose up -d
    ```
5. Select the VPC and the availability Zones where you want to launch the instances.
6. Select the load balancer you created earlier.
7. Health check: true. To kill instances that are not running.
8. Configure scaling policies:
   - Choose "Create a new scaling policy."
   - Leave the default settings for the scaling policy. If half of the CPU is used for 300 seconds, a new instance will be created.
9. Continue without changing the rest of the settings.

### Create NFS

1. Go to the EFS Dashboard.
2. Click on "Create file system."
3. Select the VPC where the EC2 instances that will use the NFS are located.
4. Click on "Attach."
5. Copy the mount command for the NFS client.
