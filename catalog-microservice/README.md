# Objective 3
Re-engineer the BookStore Monolitica app, to be divided into 3 coordinating microservices:
- Microservice 1: Authentication: will manage register, login, logout.
- Microservice 2: Catalog: will allow to visualize the offer of books on the platform.
- Microservice 3: Purchase, Payment and Delivery of books sold on the platform.

## Objective Completion Features

- [x] Completed
- **Domain**: [objective3.p2tet.duckdns.org](https://objective2.p2tet.duckdns.org) is the domain which points to the Monolithic application with autoscaling.

## Table of Contents
- [Objective 3](#objective-3)
  - [Objective Completion Features](#objective-completion-features)
  - [Table of Contents](#table-of-contents)
- [Catalog Microservice](#catalog-microservice)
  - [Domain](#domain)
    - [Prerequisites](#prerequisites)
    - [Strategy](#strategy)
  - [Database configuration](#database-configuration)
  - [Load Balancer configuration](#load-balancer-configuration)
  - [Autoscaling configuration](#autoscaling-configuration)
  - [Set up Development](#set-up-development)
    - [Execution](#execution)
  - [Set up Deployment](#set-up-deployment)
    - [Template VM](#template-vm)
    - [Installing Docker and Docker Compose](#installing-docker-and-docker-compose)
    - [Domain](#domain-1)
    - [Deploying the Application](#deploying-the-application)

# Catalog Microservice
The catalog microservice is responsible for managing and displaying the list of books available in the bookstore. It provides endpoints to view, add, update and delete book entries.

## Domain

### Prerequisites
- Python 3.x (3.12.4 was the used version)
- Docker and Docker Compose

### Strategy
The catalog microservice is designed to be independent and focused on all catalog-related logic. It connects to the shared bookstore database and exposes endpoints for book retrieval and management. It uses SQLAlchemy with read/write routing logic, and Flask to manage views or API endpoints.

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
cd project-2-tet/catalog-microservice
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
7. Access the application at `http://localhost:5002`.
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
cd project-2-tet/catalog-microservice
```
2. Create a `.env` file in the root directory of the project and set the environment variables as in the `.env.example` file:
```bash
FLASK_ENV=production
SECRET_KEY=secretkey
SQLALCHEMY_TRACK_MODIFICATIONS=False
WRITE_ENGINE=mysql+pymysql://YOUR_USER:YOUR_PASS@YOUR_URL/YOUR_DB
READER_ENGINE=mysql+pymysql://YOUR_USER:YOUR_PASS@YOUR_URL/YOUR_DB
CREATION_DB=mysql+pymysql://YOUR_USER:YOUR_PASS@YOUR_URL/YOUR_DB
```

3. Run the application:
```bash
docker compose up -d
```
