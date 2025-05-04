# Objective 2
Cloud scaling of a monolithic application, scaled on EC2 virtual machines on demand, with a highly available database.

## Objective Completion Features

- [x] Completed
- **Extension of objective 1**: This new objective continues with what was implemented in objective 1, separating the different functionalities under subdomains of the application.
- **Highly available database**: We used the Aurora and RDS service to deploy a highly available database in the cloud which integrates with our application, which will later allow for auto-scaling.
- **Load balancer**: a load balancer was implemented that will redirect traffic between multiple service instances, which is the central axis in our scaling strategy, since each instance works with a remote database, so there is no dependency between application instances, something that could not be achieved following the monolithic architecture approach in objective 1.
- **AWS Autoscaling**: An auto-scaling policy was implemented based on an image created from an EC2 instance, which defines that there can be between 1 to 6 application instances maximum, with a desired number of 2, which will increase on demand.

## Table of Contents
- [Objective 2](#objective-2)
- [Objective Completion Features](#objective-completion-features)
- [Bookstore Monolith](#bookstore-monolith)
- [Table of Contents](#table-of-contents)
- [Deploy](#setup)
  - [Prerequisites](#prerequisites)
  - [Strategy](#strategy)
  - [Code changes](#code-changes)
  - [Database configuration](#database-configuration)
  - [Load Balancer configuration](#load-balancer-configuration)
  - [Autoescaling configuration](#autoscaling-configuration)

# Bookstore Monolith
A simple bookstore application that allows users to view, add, update, and delete books. The application is built using Flask and uses a MySQL database to store book information, modified for the use of an external database.

## Setup

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
