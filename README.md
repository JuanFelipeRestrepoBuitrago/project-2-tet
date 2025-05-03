# Project 2 - TET Bookstore
This repository contains the code for the Bookstore Monolithic application, which is a simple bookstore application that allows users to view, add, update, and delete books. The application is built using Flask and uses a MySQL database to store book information. We must deploy these application in different ways to complete 3 objectives. The first objective is to deploy the application on a Virtual Machine on AWS, with its own domain, SSL certificate and reverse proxy on NGINX. The second objective is to deploy the application using autoscaling and load balancing on AWS, with its own domain, SSL certificate and reverse proxy on NGINX. The third objective is to deploy the application modified to use microservices on AWS, with its own domain, SSL certificate and reverse proxy on NGINX.

## Table of Contents
- [Project 2 - TET Bookstore](#project-2---tet-bookstore)
- [Objective 1](#objective-1)
  - [Objective Completion Features](#objective-completion-features)

## Objective 1
Deploy the BookStore Monolithic application on a Virtual Machine on AWS, with its own domain, SSL certificate and reverse proxy on NGINX. 

### Objective Completion Features

- [x] Completed
- **Domain**: [objective1.p2-tet-bookstore.duckdns.org](https://objective1.p2-tet-bookstore.duckdns.org) is the domain which points to the Monolithic application.
- **SSL Certificate**: The SSL certificate is provided by Let's Encrypt and is automatically renewed every 90 days.
- **Reverse Proxy**: NGINX is used as a reverse proxy to handle incoming requests and route them to the appropriate application container. In this case, the domain we own is `p2-tet-bookstore.duckdns.org`, but with the reverse proxy, we can access the application using `objective1.p2-tet-bookstore.duckdns.org`. The reverse proxy is configured to handle SSL termination and forward requests to the application running on port 5000. This reverse proxy was set up in a different aws EC2 instance, so I can be able to add the other objectives in the same domain, changing the subdomain for each objective. 