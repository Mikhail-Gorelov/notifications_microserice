from src.celery import app


@app.task(name='update_prices')
def update_prices(**kwargs):
    print('hello world!', kwargs)
