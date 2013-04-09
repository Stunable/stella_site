from utils import getXLSdata
import zipfile
import os
import sys
import copy
import urllib
import pprint
import tempfile

import datetime

from django.contrib.contenttypes.models import ContentType
from racks.models import Item,ItemType,Color,Size,ProductImage
from django.core.files import File


from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from celery import task


from johnny.cache import enable


def find_image(folder,image):
    for f in os.listdir(folder):
        # print f.lower()
        for ext in ['jpg','jpeg','png']:
            # print image.replace('.'+ext,'')+'.'+ext
            if f.lower() == image.lower().replace('.'+ext,'')+'.'+ext:
                # print 'GOT IT' , image.lower().replace('.'+ext,'')+'.'+ext
                return os.path.join(folder,f)


def process_upload(upload,throughModel,errorClass):

    errors = []

    path = extract_zip(upload.uploaded_zip.path)
    xls = find_xls(path)

    folder = os.path.dirname(xls)
    current = [None for i in range(0,9)]
    prev = copy.copy(current)
    Picture = None
    I = None # the item in question

    for i,d in enumerate(getXLSdata(xls)):
        try:
            if i == 0:
                continue
            #BRAND', u'PRODUCT NAME', u'PRODUCT IMAGE', u'PRODUCT DESCRIPTION', u'COLOR', u'SIZE', u'INVENTORY', u'MSRP', 'SKU'
               #0           1                 2                     3                 4        5          6           7     8
            
            fullrow = ''.join([cel for cel in d if cel.lstrip().rstrip()])
            if not fullrow.lstrip().rstrip():
                continue
            # if not fullrow

            if d[2] != prev[2]:#the image is different
                Picture = None
                imgpath = find_image(folder,d[2])
                if imgpath:
                    pic = File(open(imgpath,'rb'))
                    Picture = ProductImage.objects.create(image=pic,retailer=upload.retailer.user)
                    # a new image has been created and is now the picture for the following items

            if Picture: # we don't proceed if there's no picture
                for j in range(0,len(d)):  #update our working info to use all the fields from the current row that aren't empty
                    if d[j].lstrip().rstrip():
                        current[j] = d[j]

                brand,name,image,description,color,size,inventory,msrp,SKU = current
                msrp = msrp.lstrip('$')

                if brand != prev[0] or name != prev[1]:

                    brand,name,image,description,color,size,inventory,msrp,SKU = d
                    msrp = msrp.lstrip('$')

                    I = Item.objects.create(
                        brand=brand,
                        name =name,
                        price=msrp,
                        description=description,
                        image=Picture,
                        upload=upload
                    )

                    if upload.retailer.user:
                        si = throughModel.objects.create(
                            stylist = upload.retailer.user,
                            item = I)



                c,created = Color.objects.get_or_create(
                    retailer = upload.retailer.user,
                    name = color
                )

                # print 'row:'+str(i)+', size:',size
                s,created = Size.objects.get_or_create(
                    size=size,
                    retailer = upload.retailer.user,
                )
                
                ItemType.objects.create(
                    item = I,
                    size = s,
                    custom_color_name = color,
                    inventory = int(inventory),
                    image = Picture,
                    price = msrp,
                    SKU = SKU
                )

                if I:
                    I.save()
                
            else:
                errors.append('Could not find a picture for Row: '+str(i)+ ' (looking for a file called <strong>%s</strong>)'%d[2])
        except Exception,e:
            if 'unique' in str(e):
                error = str(e) + '... looks like you might have two of the same color/size/item.'
            else:
                error = str(e)
            errors.append('Row '+str(i)+':'+error)
        
        for k,f in enumerate(current):
            prev[k] = current[k]

    for error in errors:
        # print error
        errorClass.objects.create(text=error,upload=upload)

    upload.processed = True
    upload.save()


def find_xls(path):
    for root,dirs,files in os.walk(path):
        if len(files):
            for f in files:
                if '.xls' in f and not f.startswith('.'):
                    return os.path.join(root,f)

def extract_zip(filepath):
    zf = zipfile.ZipFile(filepath, 'r')
    name = 'extracted_'+os.path.basename(filepath)
    path = os.path.dirname(filepath)

    outdir = os.path.join(path,name)
    try:
        os.makedirs(outdir)
    except:
        pass
    zf.extractall(outdir)
    return outdir    



@task
def save_shopify_inventory_update(api_connection,source_id,item_variation,number_sold):

    enable()
    SV = api_connection.shopifyconnection.get_session().Variant.find(source_id)
    print 'updating inventory for variant:',SV
    print 'current inventory',SV.attributes['inventory_quantity']
    print 'with number sold:',number_sold
    SV.attributes['inventory_quantity'] = SV.attributes['inventory_quantity']  - number_sold
    try:
        SV.save()
        print 'success'

        item_variation.inventory = SV.attributes['inventory_quantity']
        item_variation.save()
        print 'api inventory:',SV.attributes['inventory_quantity']
        print 'stunable inventory:',item_variation.inventory
    except:
        raise


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
        process_API_products.delay(product_list,api_connection)
    
@task
def process_API_products(list_of_products,api_connection):
    enable()
    product_count = 0
    Retailer = ContentType.objects.get(app_label="retailers", model="retailerprofile").model_class().objects.get(user=api_connection.retailer)

    for product in list_of_products:
        try:
            d = product.to_dict()
            Map = api_connection.field_mapping(d)

            # PP.pprint(Map)
            api_item_object,created = api_connection.ITEM_API_CLASS.objects.get_or_create(source_id=d[Map['API']['source_id']],api_connection=api_connection)

            # if created:

            I,created = api_connection.ITEM_CLASS.objects.get_or_create(
                name =d['title'],
                api_type = ContentType.objects.get_for_model(api_item_object),
                object_id = api_item_object.id,
                _retailer = Retailer
            )
            I.brand = d[Map['item']['fields']['brand']]
            
            if created:
                 I.description = api_connection.get_description(d)
                 I._retailer = Retailer
            I.save()

            if created:
                product_count += 1
            
            api_connection.STYLIST_ITEM_CLASS.objects.get_or_create(
                                                                    stylist=api_connection.retailer,
                                                                    item=I
                                                                )
            # get all the images associated with this product
            for index,image in enumerate(api_connection.get_images(d)):
                path,identifier = image
                Picture = api_connection.IMAGE_CLASS.already_exists(identifier,api_connection.retailer)
                if not Picture:
                    out = tempfile.NamedTemporaryFile()
                    out.write(urllib.urlopen(path).read())
                    Picture = api_connection.IMAGE_CLASS.objects.create(
                        identifier=str(identifier),
                        image=File(out, os.path.basename(path)[:99]),
                        retailer=api_connection.retailer,
                        item=I)

                if index == 0:
                    I.featured_image = Picture
                    I.save()

            # get all the variations
            variation_list = api_connection.get_variations(d)
            for v in variation_list:
                

                api_variation_object,created = api_connection.VARIATION_API_CLASS.objects.get_or_create(source_id=v[Map['itemtype']['fields']['source_id']],api_connection=api_connection)
                size_string = 'ONE SIZE'
                color_string = 'ONE COLOR'

                # PP.pprint( Map['itemtype']['fields'])
                if Map['itemtype']['fields'].has_key('size') and len(variation_list) > 1:
                    size_string = v[Map['itemtype']['fields']['size']]

                s,created = api_connection.SIZE_CLASS.objects.get_or_create(
                    size=size_string,
                    retailer = api_connection.retailer,
                )

                if Map['itemtype']['fields'].has_key('custom_color_name') and len(variation_list) > 1:
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

                regular_price,sale_price = api_variation_object.get_prices(v,Map)

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

#     ctx = {

#                 }
#     subject = 'Product API refresh completed'
#     email_message = """

# %(retailer)s just had their



#     """     
    
# #                send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [self.email_address])
#     send_mail(subject, email_message, settings.STELLA_DEFAULT_EMAIL, [self.email_address])

#     subject = "NEW RETAILER:%s"%self.name
#     email_message = "THE FOLLOWING EMAIL WAS SENT TO %s\n"%self.email_address + email_message
#     send_mail(subject, email_message, settings.STELLA_DEFAULT_EMAIL, [settings.RETAILER_EMAIL])





