
# Messagebridge

MessageBridge is an API application that integrates with various technologies like RabbitMQ, Redis, and MongoDB to facilitate data transmission, caching, and persistent data storage. This application provides an efficient way to manage data flow and message delivery using a modern, fast, and user-friendly RESTful API with FastAPI.
## Features

- Send and receive messages using RabbitMQ.
- Cache messages using Redis.
- Persistently store messages using MongoDB.
- Modern and fast API interface with FastAPI.

  
## Requirements

- Docker [Installation Guide](https://docs.docker.com/get-docker/)
- Docker Compose [Installation Guide](https://docs.docker.com/compose/install/)
- Python 3.8+
- Operating System: Tested primarily on **Ubuntu 24.04 LTS**.
- Jenkins: For CI/CD pipelines. [Installation Guide](https://www.jenkins.io/doc/book/installing/)
  - Jenkins Plugins
    - Docker Plugin: For building and managing Docker containers.
    - Git Plugin: For integrating with Git repositories.
    - Pipeline Plugin: For defining and running jobs using Jenkins pipelines.
- Network:
  - Ensure ports `8000`, `5672`, `15672`, `6379`, and `27017` are open.
## Initial Server Setup
To prepare your Ubuntu server, execute the provided setup script which automates the installation and configuration of necessary components like Docker, Docker Compose, Python, and Jenkins.

### Steps to Run the Setup Script

1. **Clone the Repository:**

   First, clone the repository to your server:

   ```bash
   git clone https://github.com/rgokhannn/messagebridge.git
   cd messagebridge
   chmod +x initialSetup.sh
   ./initialSetup.sh
   ```
2. **Clone the Repository:**

   Ensure the setup.sh script is executable:

   ```bash
    chmod +x initialSetup.sh
   ```
3. **Clone the Repository:**

   Run the setup script to automatically install and configure the required software:

   ```bash
   ./initialSetup.sh
   ```
## Installation

1. Clone the Repository:

   ```bash
   git clone https://github.com/rgokhannn/messagebridge.git
   cd messagebridge
   ```
2. Start the Services with Docker Compose:
   ```bash
   docker-compose up --build
   ```
## Usage

The application provides the following API endpoints:

1. **Send Message:**

   - Endpoint: `/send`
   - Method: `POST`
   - Sample Request:

     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"message": "Your Message"}' http://localhost:8000/send
     ```

   - Description: Sends the specified message to RabbitMQ and caches it in Redis.

2. **Check Redis:**

   - Endpoint: `/redis`
   - Method: `GET`
   - Sample Request:

     ```bash
     curl http://localhost:8000/redis
     ```

   - Description: Returns the last cached message from Redis.

3. **Check MongoDB:**

   - Endpoint: `/mongodb`
   - Method: `GET`
   - Sample Request:

     ```bash
     curl http://localhost:8000/mongodb
     ```

   - Description: Returns all stored messages from MongoDB.