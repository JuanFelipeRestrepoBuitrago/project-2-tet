# Objective 1
Deploy the BookStore Monolithic application on a Virtual Machine on AWS, with its own domain, SSL certificate and reverse proxy on NGINX. 

## Table of Contents
- [Objective 1](#objective-1)
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