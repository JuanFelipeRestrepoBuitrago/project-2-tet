# Objective 3
Re-engineer the BookStore Monolitica app, to be divided into 3 coordinating microservices:
- Microservice 1: Authentication: will manage register, login, logout.
- Microservice 2: Catalog: will allow to visualize the offer of books on the platform.
- Microservice 3: Purchase, Payment and Delivery of books sold on the platform.

## Objective Completion Features

- [x] Completed
- **Domain**: [objective3.p2tet.duckdns.org](https://objective3.p2tet.duckdns.org) is the domain which points to the Monolithic application with autoscaling.
- **Microservices**: we integrated the 3 microservices which were asked for in the objective.
- **Swarm**: we used Docker Swarm to deploy the application in a cluster of 3 nodes.
- **NFS**: we used NFS to share the favicon of the page between the 3 nodes and the objective 2.

## Table of Contents
- [Objective 3](#objective-3)
- [Objective Completion Features](#objective-completion-features)
- [Bookstore 3 with Microservices](#bookstore-3-with-microservices)
- [Table of Contents](#table-of-contents)
- [Domain](#domain)
    - [Prerequisites](#prerequisites)
- [Database configuration](#database-configuration)
- [Load Balancer configuration](#load-balancer-configuration)
- [Autoscaling configuration](#autoscaling-configuration)
- [Set up Development](#set-up-development)
    - [Execution](#execution)
- [Set up Deployment](#set-up-deployment)
    - [Deploy 3 EC2 instances](#deploy-3-ec2-instances)
    - [Installing Docker and Docker Compose in all instances](#installing-docker-and-docker-compose-in-all-instances)
    - [Domain](#domain-1)
    - [NFS](#nfs)
    - [Swarm](#swarm)
    - [Deploying the Application in the First Instance](#deploying-the-application-in-the-first-instance)

# Bookstore 3 with Microservices
The authentication microservice is responsible for managing user authentication and authorization. It provides endpoints for user registration, login, and logout. The microservice uses JWT (JSON Web Tokens) for secure token-based authentication.

## Domain

### Prerequisites
- Python 3.x (3.12.4 was the used version)
- Docker and Docker Compose

### Strategy
The main application is designed to be connected to 3 different microservices, which are:
- **Authentication**: This microservice is responsible for managing user authentication and authorization. It provides endpoints for user registration, login, and logout. The microservice uses JWT (JSON Web Tokens) for secure token-based authentication.
- **Catalog**: This microservice is responsible for managing the catalog of books available on the platform. It provides endpoints for retrieving book information, searching for books, and managing book inventory.
- **Purchase**: This microservice is responsible for managing the purchase process, including payment processing and order management. It provides endpoints for creating orders, processing payments, and managing order status.

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

You must have run the microservices in the following order:
1. **Authentication**: Follow the instructions in the [auth-microservice](../auth-microservice/README.md) directory.
2. **Catalog**: Follow the instructions in the [catalog-microservice](../catalog-microservice/README.md) directory.
3. **Purchase**: Follow the instructions in the [purchase-microservice](../purchase-microservice/README.md) directory.

1. Clone the repository:
```bash
git clone https://github.com/JuanFelipeRestrepoBuitrago/project-2-tet.git
cd project-2-tet/bookstore-3
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
4. Set up the environment variables as in the `.env.example` file:
In windows run:
```bash
set FLASK_ENV=development
set SECRET_KEY=secretkey
set SQLALCHEMY_TRACK_MODIFICATIONS=False
set WRITE_ENGINE=mysql+pymysql://bookstore_user:123@localhost/bookstore
set READER_ENGINE=mysql+pymysql://bookstore_user:123@localhost/bookstore
set CREATION_DB=mysql+pymysql://bookstore_user:123@localhost/bookstore
set AUTH_SERVICE_URL=http://YOUR_URL:YOUR_PORT/auth
```
or in Linux run:
```bash
export FLASK_ENV=development
export SECRET_KEY=secretkey
export SQLALCHEMY_TRACK_MODIFICATIONS=False
export WRITE_ENGINE=mysql+pymysql://bookstore_user:123@localhost/bookstore
export READER_ENGINE=mysql+pymysql://bookstore_user:123@localhost/bookstore
export CREATION_DB=mysql+pymysql://bookstore_user:123@localhost/bookstore
export AUTH_SERVICE_URL=http://YOUR_URL:YOUR_PORT/auth
```
5. Run the application:
```bash
python app.py
```
6. Access the application at `http://localhost:5000`.
7. You can stop the application by pressing `Ctrl+C` in the terminal.

## Set up Deployment


### Deploy 3 EC2 instances

To deploy the application on AWS, you need to set up three EC2 instances. Follow these steps:

1. Create an AWS account and log in to the AWS Management Console.
2. Navigate to the EC2 Dashboard and launch a new instance.
3. Choose an Ubuntu Server 20.04 LTS AMI.
4. Select an instance type (e.g., t2.micro for free tier).
5. Configure instance details, including network settings and security groups, to allow HTTP (port 80) and HTTPS (port 443) traffic.
6. Create a new key pair or use an existing one to access the instance.
7. Launch the instance and wait for it to be in the "running" state.

### Installing Docker and Docker Compose in all instances

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

### NFS

1. Install NFS server on the EC2 instances:
```bash
sudo apt update && sudo apt install -y nfs-common
```
2. Create a directory to mount the NFS share:
```bash
sudo mkdir -p ~/nfs-mount && sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport YOUR_URL:/ ~/nfs-mount
```
3. Verify the NFS share is mounted:
```bash
df -h
```

### Swarm

1. Initialize Docker Swarm on the first instance:
```bash
docker swarm init
```

2. Join the other instances to the swarm:
```bash
docker swarm join --token YOUR_TOKEN YOUR_MANAGER_IP:2377
```

### Deploying the Application in the First Instance
1. Clone the repository:
```bash
git clone https://github.com/JuanFelipeRestrepoBuitrago/project-2-tet.git
cd project-2-tet/bookstore-3
```
2. Create a `.env` file in the root directory of the project and set the environment variables as in the `.env.example` file:
```bash
FLASK_ENV=production
SECRET_KEY=secretkey
SQLALCHEMY_TRACK_MODIFICATIONS=False
WRITE_ENGINE=mysql+pymysql://YOUR_USER:YOUR_PASS@YOUR_URL/YOUR_DB
READER_ENGINE=mysql+pymysql://YOUR_USER:YOUR_PASS@YOUR_URL/YOUR_DB
CREATION_DB=mysql+pymysql://YOUR_USER:YOUR_PASS@YOUR_URL/YOUR_DB
AUTH_SERVICE_URL=http://YOUR_URL:YOUR_PORT/auth
```

3. Run the application:
```bash
docker stack deploy -c docker-compose.yml bookstore
```