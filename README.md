# Flask Web Application

This repository contains a Flask web application that you can easily set up using Docker.

## Prerequisites

Before you begin, make sure you have [Docker](https://www.docker.com/get-started) installed on your system.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 2. Build the docker image

```bash
docker build -t webapp:latest .
```


### 2. Run the docker container

```bash
docker run -d -p 5000:5000 webapp:latest
```

### 2. Access the web application
Open your web browser and navigate to http://localhost:5000 or http://0.0.0.0:5000 to view the running application.

