# Application Deployment Guide

## Monolithic Deployment

### AWS VM Configuration
- Set up a VM on AWS
- Expose port 5000 for TCP communication to allow connections

### Install Docker and Docker Compose
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
```

### Deploy the Application
1. Clone the repository
2. Navigate to the directory containing the docker-compose.yml file
3. Run the command:
   ```bash
   docker-compose up -d
   ```

### Access the Application
- Access the application using the VM's public IP:
  ```
  http://{public-ip}:5000
  ```

### Example
![Example](/images/proyect.png)

## 
