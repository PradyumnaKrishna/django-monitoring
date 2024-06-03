# Website Monitoring Application

This is a simple Python Django application created to check if a website is up or not. If the website is down or takes too long to respond, the app will send an email to a configured address. This application utilizes Celery for task management.

## How to Run

1. Install all dependencies: `pip install -r requirements.txt`
2. Create a new Website entry: open the Django shell and import models from the monitoring app, then create an object for the Website model.
3. Migrate the models `python manage.py migrate`
4. Run the server: `python manage.py runserver`
5. Start a Celery worker node: `celery -A pingdom worker --loglevel=info`
6. Start Celery beat for scheduling tasks: `celery -A pingdom beat --loglevel=info`
7. Navigate to - http://localhost:8000/monitoring/
8. Open the shell and create an entry for the Website model. Once the object is created, a signal will trigger, and a new task will be added to CrontabSchedule and PeriodicTask.

```
In [13]: from monitoring.models import *

In [14]: Website.objects.create(name='stackoverflow', url='https://stackoverflow.com/questions/3772260/how-to-reload-modules-in-django-shell')
```

Here are the visuals,

![image](https://github.com/nawarkhede/monitor-webapp/assets/3713237/6594d38d-50c4-486d-a6cf-d1fd88fcc979)

![image](https://github.com/nawarkhede/monitor-webapp/assets/3713237/42d9fb3a-796e-4020-a537-a3e7194151a5)




If you are using Windows, you may encounter an issue with Celery where tasks always have a status of "PENDING". To fix this, add the `--pool=solo` parameter when starting the worker node. The command will then be: `celery -A pingdom worker --loglevel=info --pool=solo`. For more information on this issue, please refer to [this Stack Overflow thread](https://stackoverflow.com/questions/27357732/celery-task-always-pending).

## Future Scope

Future scope for this application includes allowing users to log in using their credentials or social logins, and enabling them to enter the sites they want to monitor.
