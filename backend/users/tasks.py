from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def daily_refresh():
    logger.info("Выполняется периодическая задача каждые 10 секунд")
    for i in range(11):
        print('--->', i+1)
    return "Задача выполнена"
