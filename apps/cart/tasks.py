from celery import task

from models import Shipment






@task()
def update_active_shipments():

	for S in Shipment.objects.exclude(status='Delivered'):
		S.update_tracking_info()


