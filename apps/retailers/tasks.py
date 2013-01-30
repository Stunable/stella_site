from utils import getXLSdata
import zipfile
import os
import copy
import urllib
import pprint
import tempfile

from django.contrib.contenttypes.models import ContentType
from racks.models import Item,ItemType,Color,Size,ProductImage
from django.core.files import File

from celery import task

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
def save_inventory_modification(api_connection,variant):
    pass


@task
def save_shopify_inventory_update(api_connection,source_id,new_value):
    SV = api_connection.shopifyconnection.get_session().Variant.find(source_id)
    if SV.attributes['inventory_quantity'] != new_value:
        print 'updating inventory for variant:',SV
        SV.attributes['inventory_quantity'] = new_value
        try:
            SV.save()
            print 'success'
        except:
            raise


@task
def update_API_products(api_connection):
    print 'updating products for '+str(api_connection)

    for product_list in api_connection.get_products():
        process_API_products.delay(product_list,api_connection)
    
@task
def process_API_products(list_of_products,api_connection):

    Retailer = ContentType.objects.get(app_label="retailers", model="retailerprofile").model_class().objects.get(user=api_connection.retailer)

    for product in api_connection.get_products():
        try:
            d = product
            Map = api_connection.field_mapping(d)

            # PP.pprint(Map)
            api_item_object,created = api_connection.ITEM_API_CLASS.objects.get_or_create(source_id=d[Map['API']['source_id']],api_connection=api_connection)

            # if created:

            I,created = api_connection.ITEM_CLASS.objects.get_or_create(
                name =d['title'],
                api_type = ContentType.objects.get_for_model(api_item_object),
                object_id = api_item_object.id,
            )
            I.brand = d[Map['item']['fields']['brand']]

            I.description = api_connection.get_description(d)
            I._retailer = Retailer
            I.save()
            
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
                    Picture = api_connection.IMAGE_CLASS.objects.create(identifier=identifier,image=File(out, os.path.basename(path)),retailer=api_connection.retailer,item=I)

                if index == 0:
                    I.featured_image = Picture
                    I.save()

            # get all the variations
            for v in api_connection.get_variations(d):
                # print v

                api_variation_object,created = api_connection.VARIATION_API_CLASS.objects.get_or_create(source_id=v[Map['itemtype']['fields']['source_id']],api_connection=api_connection)
                size_string = 'ONE SIZE'
                color_string = 'ONE COLOR'

                # PP.pprint( Map['itemtype']['fields'])
                if Map['itemtype']['fields'].has_key('size'):
                    size_string = v[Map['itemtype']['fields']['size']]

                s,created = api_connection.SIZE_CLASS.objects.get_or_create(
                    size=size_string,
                    retailer = api_connection.retailer,
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

                regular_price,sale_price = api_variation_object.get_prices(v,Map)

                if regular_price != sale_price:
                    it.is_onsale = True

                it.price = regular_price
                it.sale_price = sale_price
                it.SKU = v[Map['itemtype']['fields']['SKU']]
                it.save()

        except Exception,e:
            raise
            print 'ERROR:',e
    print 'done updating items'
    api_connection.update_in_progress = False
    api_connection.save()



