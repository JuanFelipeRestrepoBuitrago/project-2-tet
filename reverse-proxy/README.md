# Reverse Proxy

Deploy the BookStore Monolithic application on a Virtual Machine on AWS, with its own domain, SSL certificate and reverse proxy on NGINX. Our domain is `p2-tet-bookstore.duckdns.org` and we have the following subdomains:
- `objective1.p2-tet-bookstore.duckdns.org` for the objective 1 application deploying a monolithic application.
- `objective2.p2-tet-bookstore.duckdns.org` for the objective 2 application deploying a scaled application with automatic scaling.
- `objective3.p2-tet-bookstore.duckdns.org` for the objective 3 application deploying a microservices application with automatic scaling.
- `*.p2-tet-bookstore.duckdns.org` for the objective 3 application deploying a microservices application with automatic scaling.
- `p2-tet-bookstore.duckdns.org` for the objective 3 application deploying a microservices application with automatic scaling.

## Table of Contents
- [Reverse Proxy](#reverse-proxy)
- [Table of Contents](#table-of-contents)
- [Deploying Reverse Proxy on AWS](#deploying-reverse-proxy-on-aws)
  - [Launching an EC2 Instance](#launching-an-ec2-instance)
  - [Installing Docker and Docker Compose](#installing-docker-and-docker-compose)
  - [Domain](#domain)
  - [SSL Certificate (DuckDNS)](#ssl-certificate-duckdns)
  - [Executing Inverse Proxy](#executing-inverse-proxy)


## Deploying Reverse Proxy on AWS

### Launching an EC2 Instance

1. Create an AWS account and log in to the AWS Management Console.
2. Navigate to the EC2 Dashboard and launch a new instance.
3. Choose an Ubuntu Server 20.04 LTS AMI.
4. Select an instance type (e.g., t2.micro for free tier).
5. Configure instance details, including network settings and security groups, to allow HTTP (port 80) and HTTPS (port 443) traffic.
6. Create a new key pair or use an existing one to access the instance.
7. Launch the instance and wait for it to be in the "running" state.
8. Go to elastic IPs and allocate a new elastic IP, then associate it with the instance.
9. SSH into the instance using the key pair:
```bash
ssh -i "your-key.pem" ubuntu@your-elastic-ip
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
1. Register a domain name with a domain registrar (e.g., GoDaddy, Namecheap). You can also use DuckDNS for free domains.
2. Set up DNS records to point your domain to the elastic IP of your EC2 instance.
3. For example, create an A record with the following details:
   - Name: `@` (or your domain name)
   - Type: `A`
   - Value: `your-elastic-ip`
4. Save the DNS settings and wait for propagation (may take a few minutes).
5. Verify the domain is pointing to the elastic IP by running:
```bash
nslookup your-domain.com
```
6. Continue with the SSL certificate setup and inverse proxy configuration at [Reverse Proxy](../reverse-proxy/README.md)

### SSL Certificate (DuckDNS)
1. Execute the docker compose first to create the container, follow the steps at [Executing Inverse Proxy](#executing-inverse-proxy):

2. Run the following docker command for each domain or sub domain you want to secure:
```bash
docker exec acme-renewer acme.sh --issue --server https://acme-v02.api.letsencrypt.org/directory --dns dns_duckdns -d your_domain.duckdns.org --home /acme.sh --reloadcmd "/reload_nginx.sh"
```

**Note:** You should run this command for each subdomain you want or you can run twice with the `*.your_domain.com` wildcard to secure all subdomains and `your_domain.com` to secure the main domain.

3. When running the previous command, your nginx instance should be correctly running, so run the following command to reload the nginx configuration for each domain or subdomain you want to secure:
```bash
docker exec acme-renewer acme.sh --issue --server https://acme-v02.api.letsencrypt.org/directory --dns dns_duckdns -d your_domain.duckdns.org --home /acme.sh --reloadcmd "/reload_nginx.sh" --force
```
You should see a message like:
```
[Fri May  2 23:11:41 UTC 2025] Your cert is in: /acme.sh/your_domain.duckdns.org_ecc/your_domain.duckdns.org.cer
[Fri May  2 23:11:41 UTC 2025] Your cert key is in: /acme.sh/your_domain.duckdns.org_ecc/your_domain.duckdns.org.key
[Fri May  2 23:11:41 UTC 2025] The intermediate CA cert is in: /acme.sh/your_domain.duckdns.org_ecc/ca.cer
[Fri May  2 23:11:41 UTC 2025] And the full-chain cert is in: /acme.sh/your_domain.duckdns.org_ecc/fullchain.cer
[Fri May  2 23:11:41 UTC 2025] Running reload cmd: /reload_nginx.sh
2025/05/02 23:11:41 [notice] 43#43: signal process started
[Fri May  2 23:11:41 UTC 2025] Reload successful
```

4. Verify SSL renewal:
```bash
docker compose exec acme acme.sh --renew -d your_domain.duckdns.org --force
```

### Executing Inverse Proxy

1. Clone the repository:
```bash
git clone https://github.com/JuanFelipeRestrepoBuitrago/project-2-tet.git
cd project-2-tet/reverse-proxy
```
2. Modify the `nginx/conf.d` files to match your domain and subdomains, instances ips and ports, and your SSL certificate paths as `/acme.sh/*.your_domain/*.your_domain.cer` and `/acme.sh/*.your_domain/*.your_domain.key`.

3. Add the following `.env` file at `your_project_path/reverse-proxy`:
```env
DuckDNS_Token=your_duckdns_token
CA=letsencrypt
ACME_EMAIL=your_email@example.com
```

4. Run the following command to start the NGINX reverse proxy:
```bash
docker compose up -d
```
5. Verify that the reverse proxy is running by accessing your domain and subdomains in a web browser:
   - `http://your-domain.com`
   - `http://subdomain.your-domain.com`
6. If you want to add more applications or services to the reverse proxy, you can modify the `nginx/conf.d/proxy.conf` files and restart the NGINX container with the following content:
```bash
server {
    listen 443 ssl;
    server_name subdomain.your-domain.com;

    ssl_certificate     /etc/letsencrypt/live/*.your-domain.com_ecc/*.p2-your-domain.com.cer;
    ssl_certificate_key /etc/letsencrypt/live/*.your-domain.com_ecc/*.your-domain.com.key;

    proxy_set_header Host              $host;
    proxy_set_header X-Real-IP         $remote_addr;
    proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    location / {
        proxy_pass http://YOUR_INSTANCE_IP:YOUR_INSTANCE_PORT;
    }
}
```
7. Restart the NGINX container:
```bash
docker compose down
docker compose up -d
```