# Website Monitoring Application

This project is a fork of <https://github.com/nawarkhede/monitor-webapp> that is a simple website monitoring application. It is a simple web application that allows users to monitor the status of their websites. I used this project and improved it's functionality including mintoring views, user authentication, and background tasks.

![Main](/images/main.png)

## About project

This project is built with Django, and it uses Celery for background tasks. Celery is a distributed task queue that is used to execute tasks asynchronously. It is used to monitor the status of the websites in the background. The results of the monitoring are stored in the database and can be viewed by the user. There are functionality of user authentication with GitHub oAuth, and alerts can be sent to the user using Webhooks or Email.

![Websites](/images/websites.png)
![Results](/images/results.png)

## New Features Implemented

* The original project lacks user authentication. So, I decided to add a GitHub oAuth Login system, so that user can
easily Single Sign On (SSO) into the Application
* There was email alerts, I decided to add Webhook Alerts, so it can be plugged into 3rd party services like Slack, Discord, etc.
* The models and views for the monitoring system were improved to make it more user friendly and easy to use. Added views to add and delete websites to monitor.

## Getting Started

1. This project is built using Django. To get started install the dependencies using the following command:

   ```bash
   pip install -r requirements.txt
   ```

2. You can setup `.env` for environment variables to run the project. You can use `.env.template` as a template for the `.env` file. You require `CLIENT_ID` and `CLIENT_SECRET` in environemtn for GitHub oAuth, otherwise it won't work.

3. To run the django server, use the following command:

   ```bash
   python manage.py runserver
   ```

4. There are two Celery workers, one is a task worker and another is a beat worker. You must need to setup `CELERY_BROKER_URL` in environment, in order to run the Celery workers. To run the Celery workers, use the following command:

   ```bash
   celery -A config worker --loglevel=info
   celery -A config beat --loglevel=info
   ```

You can now browse the website at <http://localhost:8000>

## Building Docker Container

By default docker doesn't run multiple subprocess at the same time. This project requires Celery wrokers to run with the Django server.

`supervisord` is used to run multiple subprocesses in a Docker container, so that both Django server and Celery workers can run at the same time. A [`supervisord.conf`](docker/supervisord.conf) file is provided in the project to run the Django server and Celery workers.

The Dockerfile is provided in the project to build the Docker container. To build the Docker container, use the following command:

```bash
docker build -t django-monitoring .
```

To run the Docker container, use the following command:

```bash
docker run -p 8000:8000 django-monitoring
```

You need to setup the environment variables, either you can mount the `.env` file to the Docker container or you can set the environment variables using `-e` flag.

```bash
docker run -p 8000:8000 -v $(pwd)/.env:/app/.env django-monitoring
```

or

```bash
docker run -p 8000:8000 \
    -e DEBUG=False \
    -e ALLOWED_HOSTS=localhost \
    -e SECRET_KEY=<secret_key> \
    -e DATABASE_URL="sqlite:///db.sqlite3" \
    -e CLIENT_ID=<client_id> \
    -e CLIENT_SECRET=<client_secret> \
    -e CELERY_BROKER_URL=<broker_url> \
    django-monitoring
```

## Cloud Deployment

This project can be deployed to the cloud using the Docker container. You can use services like Heroku, AWS, GCP, etc. to deploy the Docker container.
