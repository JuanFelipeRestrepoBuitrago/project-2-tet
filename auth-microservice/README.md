# Objective 3
Re-engineer the BookStore Monolitica app, to be divided into 3 coordinating microservices:
- Microservice 1: Authentication: will manage register, login, logout.
- Microservice 2: Catalog: will allow to visualize the offer of books on the platform.
- Microservice 3: Purchase, Payment and Delivery of books sold on the platform.

## Objective Completion Features

- [x] Completed
- **Extension of objective 1**: This new objective continues with what was implemented in objective 1, separating the different functionalities under subdomains of the application.
- **Highly available database**: We used the Aurora and RDS service to deploy a highly available database in the cloud which integrates with our application, which will later allow for auto-scaling.
- **Load balancer**: a load balancer was implemented that will redirect traffic between multiple service instances, which is the central axis in our scaling strategy, since each instance works with a remote database, so there is no dependency between application instances, something that could not be achieved following the monolithic architecture approach in objective 1.
- **AWS Autoscaling**: An auto-scaling policy was implemented based on an image created from an EC2 instance, which defines that there can be between 1 to 6 application instances maximum, with a desired number of 2, which will increase on demand.
- **Domain**: [objective3.p2tet.duckdns.org](https://objective2.p2tet.duckdns.org) is the domain which points to the Monolithic application with autoscaling.

## Table of Contents
- [Objective 2](#objective-2)
- [Objective Completion Features](#objective-completion-features)
- [Bookstore Monolith](#bookstore-monolith)
- [Table of Contents](#table-of-contents)
- [Domain](#domain)
    - [Prerequisites](#prerequisites)
    - [Code changes](#code-changes)
- [Database configuration](#database-configuration)
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


# Authentication Microservice
The authentication microservice is responsible for managing user authentication and authorization. It provides endpoints for user registration, login, and logout. The microservice uses JWT (JSON Web Tokens) for secure token-based authentication.

## Domain

### Prerequisites
- Python 3.x (3.12.4 was the used version)
- Docker and Docker Compose

### Strategy
The authentication microservice is designed to be stateless, meaning it does not store any session information on the server. Instead, it relies on JWT tokens to authenticate users. When a user logs in, the microservice generates a JWT token that contains the user's information and expiration time. This token is then sent back to the client and must be included in subsequent requests to access protected resources.

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

## Set up Development

### Execution

1. Clone the repository:
```bash
git clone https://github.com/JuanFelipeRestrepoBuitrago/project-2-tet.git
cd project-2-tet/bookstore-monolith
```

2. Create a virtual environment (optional):
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install the required packages:
```bash
pip install -r requirements.txt
```
4. Execute the database or docker compose with the following specifications:
```bash
MYSQL_DATABASE: bookstore
MYSQL_USER: bookstore_user
MYSQL_PASSWORD: 123
MYSQL_ROOT_PASSWORD: 123
```
or docker compose with the following specifications:
```bash
docker compose -f ./docker-compose-dev.yml up -d
```
5. Set up the environment variables as in the `.env.example` file:
In windows run:
```bash
set FLASK_ENV=development
set SECRET_KEY=secretkey
set SQLALCHEMY_TRACK_MODIFICATIONS=False
set WRITE_ENGINE=mysql+pymysql://bookstore_user:123@localhost/bookstore
set READER_ENGINE=mysql+pymysql://bookstore_user:123@localhost/bookstore
set CREATION_DB=mysql+pymysql://bookstore_user:123@localhost/bookstore
```
or in Linux run:
```bash
export FLASK_ENV=development
export SECRET_KEY=secretkey
export SQLALCHEMY_TRACK_MODIFICATIONS=False
export WRITE_ENGINE=mysql+pymysql://bookstore_user:123@localhost/bookstore
export READER_ENGINE=mysql+pymysql://bookstore_user:123@localhost/bookstore
export CREATION_DB=mysql+pymysql://bookstore_user:123@localhost/bookstore
```
6. Run the application:
```bash
python app.py
```
7. Access the application at `http://localhost:5000`.
8. To stop the application, press `Ctrl+C` in the terminal where the application is running and to stop the docker compose, run:
```bash
docker compose -f ./docker-compose-dev.yml down
```

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
