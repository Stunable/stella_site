from celery import task

from models import Shipment,Purchase






@task()
def update_active_shipments():

	for S in Shipment.objects.exclude(status='Delivered'):
		S.update_tracking_info()


@task()
def check_for_complete_purchases():
	for P in Purchase.objects.filter(status='delivered'):
		P.check_if_complete()

