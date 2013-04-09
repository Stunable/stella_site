

from django.contrib.contenttypes.models import ContentType

import pprint

PP = pprint.PrettyPrinter(indent=4)

from celery import task
from johnny.cache import enable

from django.conf import settings

import datetime

import tempfile
import os
from django.core.files import File
import urllib

@task 
def refresh_all_api_products():
    enable()
    for api_connection in ContentType.objects.get(app_label="retailers", model="apiconnection").model_class().objects.all():
        for api_type in ['shopifyconnection']:
            if hasattr(api_connection,api_type):
                update_API_products.delay(getattr(api_connection,api_type))


@task
def update_API_products(api_connection):
    enable()
    print 'updating products for '+str(api_connection)

    for product_list in api_connection.get_products():
        # print 'product list:',product_list
        if settings.DEBUG:
            process_API_products(product_list,api_connection)
        else:
            process_API_products.delay(product_list,api_connection)


@task
def process_API_products(list_of_products,api_connection):
    enable()
    product_count = 0
    Retailer = api_connection.retailer_profile

    print list_of_products

    for product in list_of_products:
        try:
            d = product
            print 'A PRODUCT:',d

            Map = api_connection.field_mapping(d)

            PP.pprint(Map)
            pid = api_connection.get_id(d)

            item_class = api_connection.ITEM_API_CLASS
            api_item_object,created = item_class.objects.get_or_create(source_id=pid,api_connection=api_connection)

            # if created:

            I,created = api_connection.ITEM_CLASS.objects.get_or_create(
                name = api_connection.get_name(d),
                api_type = ContentType.objects.get_for_model(api_item_object),
                object_id = api_item_object.id,
                _retailer = Retailer
            )
            I.brand = api_connection.get_brand(d)
            
            if created:
                 I.description = api_connection.get_description(d)
                 I._retailer = Retailer
            I.save()

            if not api_connection.variants_Have_Prices:
                regular_price,sale_price = api_connection.get_prices(d)

            if created:
                product_count += 1

            # get all the images associated with this product
            for index,image in enumerate(api_connection.get_images(d)):
                path,identifier = image
                Picture = api_connection.IMAGE_CLASS.already_exists(identifier,Retailer)
                if not Picture:
                    out = tempfile.NamedTemporaryFile()
                    out.write(urllib.urlopen(path).read())
                    Picture = api_connection.IMAGE_CLASS.objects.create(
                        identifier=str(identifier),
                        image=File(out, os.path.basename(path)[:99]),
                        retailer_profile=Retailer,
                        item=I)

                if index == 0:
                    I.featured_image = Picture
                    I.save()

            # get all the variations
            for v in api_connection.get_variations(d):
                

                api_variation_object,created = api_connection.VARIATION_API_CLASS.objects.get_or_create(source_id=v[Map['itemtype']['fields']['source_id']],api_connection=api_connection)
                size_string = 'ONE SIZE'
                color_string = 'ONE COLOR'

                # PP.pprint( Map['itemtype']['fields'])
                if Map['itemtype']['fields'].has_key('size'):
                    size_string = v[Map['itemtype']['fields']['size']]

                s,created = api_connection.SIZE_CLASS.objects.get_or_create(
                    size=size_string,
                    retailer_profile = Retailer,
                )

                if Map['itemtype']['fields'].has_key('custom_color_name'):
                    color_string =v[Map['itemtype']['fields']['custom_color_name']]
                
                try:
                    it = api_connection.ITEM_TYPE_CLASS.objects.get(
                        item = I,
                        size = s,
                        custom_color_name = color_string
                    )
                except:
                    it = api_connection.ITEM_TYPE_CLASS.objects.create(
                        item = I,
                        size = s,
                        custom_color_name = color_string
                    )

                it.api_type = ContentType.objects.get_for_model(api_variation_object)
                it.object_id = api_variation_object.id
                it.inventory = int(v[Map['itemtype']['fields']['inventory']])

                if api_connection.variants_Have_Prices:
                    regular_price,sale_price = api_connection.get_prices(v)

                if regular_price != sale_price:
                    it.is_onsale = True
                it.SKU = v[Map['itemtype']['fields']['SKU']]
                it.save()

                try: #sometimes prices are screwy (with shopify)
                    it.price = regular_price
                    it.sale_price = sale_price
                    it.save()
                except Exception,e:

                    print 'PRODUCT:',d
                    print 'VARIATION:',v
                    print 'ERROR:',e
                    pass
                    # raise (Exception)


        except Exception,e:
            raise
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('ERROR:',e, exc_type, fname, exc_tb.tb_lineno)
            api_connection.update_in_progress = False
            api_connection.last_updated = datetime.datetime.now()
            api_connection.save()
    print 'done updating items'
    api_connection.update_in_progress = False
    api_connection.last_updated = datetime.datetime.now()
    api_connection.save()