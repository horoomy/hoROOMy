from .sites import tasks as parser_tasks
from .sites.randomproxy.proxyparser import parse_proxy
from celery import shared_task
from .sites.utils import Logger, TgBot
from .models import *


@shared_task(name='parsers.clear_duplicates')
def clear_duplicates():
    logger = Logger()
    logger.name = 'Clear'
    logger.timestamp('clear')
    logger.info('Clearing duplicates...')
    count = 0
    for ad in Ad.objects.all():
        if not ad.description: continue
        qs = Ad.objects.filter(description=ad.description).exclude(id=ad.id)
        count += len(qs)
        qs.delete()
    delta = logger.timestamp('clear')
    logger.info('Succeed in {:.3f} seconds'.format(delta.seconds))
    logger.info('Total duplicates removed: {}'.format(count))
    if count: TgBot.send(logger.get_text())