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





