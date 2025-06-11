from src.celery_app import celery
import time
import requests

@celery.task(name="src.tasks.task.add")
def add(x, y):
    time.sleep(2)
    return x + y

@celery.task(name="src.tasks.fetch_data_daily")
def fetch_data_daily():
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        return response.status_code