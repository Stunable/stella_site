from celery import task

from models import *


@task
def get_daily_posts():
	ExternalPost.objects.create(post_type='news')
	ExternalPost.objects.create(post_type='blog')