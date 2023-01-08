# Social network database project

Application is an API that workers as a simple social network that support registration of users, and simple posts
management.

## Requirements

- Python 3.9+
- Docker
- Docker-compose

## Setup with docker-compose

Application can be started with docker-compose.
Before launching adjust environment variables in ```.env``` file according to your needs.
All data in ```.env``` is a just an example.

Use the following command to launch application according to current configuration in detached mode.

```
docker-compose up -d
```

Use command to stop application and clean data

```
docker-compose down
```

## Setup locally

In order to setup and run application locally

0. Setup virtual environment

```
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requiremetns.txt
```

Make sure you use only venv environment.

1. Setup container with database using python script

```
python ci/setup_env.py
```

2. Run application

```
python main.py
```

After application starts go to http://127.0.0.1:8000/ to see the basic information about the app.

## Tests

In order to run tests follow the logic:

1. Start application
2. Run command ```PYTHONPATH=$(pwd) pytest --host 127.0.0.1:8000``` where you should replace host with location of your application.
