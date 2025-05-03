# Objective 1
Deploy the BookStore Monolithic application on a Virtual Machine on AWS, with its own domain, SSL certificate and reverse proxy on NGINX. 

## Objective Completion Features

- [x] Completed
- **Domain**: [objective1.p2-tet-bookstore.duckdns.org](https://objective1.p2-tet-bookstore.duckdns.org) is the domain which points to the Monolithic application.
- **SSL Certificate**: The SSL certificate is provided by Let's Encrypt and is automatically renewed every 90 days.
- **Reverse Proxy**: NGINX is used as a reverse proxy to handle incoming requests and route them to the appropriate application container. In this case, the domain we own is `p2-tet-bookstore.duckdns.org`, but with the reverse proxy, we can access the application using `objective1.p2-tet-bookstore.duckdns.org`. The reverse proxy is configured to handle SSL termination and forward requests to the application running on port 5000. This reverse proxy was set up in a different aws EC2 instance, so I can be able to add the other objectives in the same domain, changing the subdomain for each objective. 

## Table of Contents
- [Objective 1](#objective-1)
- [Objective Completion Features](#objective-completion-features)
- [Bookstore Monolith](#bookstore-monolith)
- [Table of Contents](#table-of-contents)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Execution](#execution)
- [Deployment in AWS](#deployment-in-aws)


# Bookstore Monolith
A simple bookstore application that allows users to view, add, update, and delete books. The application is built using Flask and uses a MySQL database to store book information. 

## Setup

### Prerequisites
- Python 3.x (3.12.4 was the used version)
- MySQL 8.x or Docker

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
MYSQL_PASSWORD: bookstore_pass
MYSQL_ROOT_PASSWORD: root_pass
```
or docker compose with the following specifications:
```bash
docker compose -f ./docker-compose-dev.yml up -d
```
5. Run the application:
```bash
python app.py
```
6. Access the application at `http://localhost:5000`.
7. To stop the application, press `Ctrl+C` in the terminal where the application is running and to stop the docker compose, run:
```bash
docker compose -f ./docker-compose-dev.yml down
```

## Deployment in AWS

### Launching an EC2 Instance

1. Create an AWS account and log in to the AWS Management Console.
2. Navigate to the EC2 Dashboard and launch a new instance.
3. Choose an Ubuntu Server 20.04 LTS AMI.
4. Select an instance type (e.g., t2.micro for free tier).
5. Configure instance details, including network settings and security groups, to allow HTTP (port 80) and HTTPS (port 443) traffic.
6. Create a new key pair or use an existing one to access the instance.
7. Launch the instance and wait for it to be in the "running" state.
8. Go to elastic IPs and allocate a new elastic IP, then associate it with the instance. (Optional)
   - Go to the EC2 Dashboard.
   - Click on "Elastic IPs" in the left sidebar.
   - Click on "Allocate Elastic IP address."
   - Choose the instance you launched and associate the elastic IP with it.
9. SSH into the instance using the key pair:
```bash
ssh -i "your-key.pem" ubuntu@your-elastic-ip
```
or
```bash
ssh -i "your-key.pem" ubuntu@your-aws-domain
```

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
cd project-2-tet/bookstore-monolith
```

2. Run the application:
```bash
docker compose up -d
```