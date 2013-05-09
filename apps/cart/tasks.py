from celery import task

from models import Shipment,Purchase
import datetime






@task()
def update_active_shipments():

    for S in Shipment.objects.exclude(status='Delivered'):
        S.update_tracking_info()


@task()
def check_for_complete_purchases():
    for P in Purchase.objects.filter(status='delivered'):
        P.check_if_complete()


@task()
def check_for_unshipped_items():
    one_day = datetime.timedelta(days = 1)
    one_day_ago = datetime.datetime.now()-one_day

    checkouts_sent = []

    for P in Purchase.objects.filter(status='placed',purchased_at__lte=one_day_ago):
        if not P.checkout.id in checkouts_sent:# prevent multiple emails going out about one order
            P.send_ship_reminder()
        checkouts_sent.append(P.checkout.id)


