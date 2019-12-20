from celery import Celery

# 定义celery对象
app = Celery("ihome", broker="redis://:2017916@127.0.0.1:6379/1")

@app.task
def send_sms():
    pass
