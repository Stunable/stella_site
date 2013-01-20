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
def update_API_products(API_OBJECT):

    for product in API_OBJECT.get_products():
        try:
            d = product.to_dict()
            Map = API_OBJECT.ITEM_API_CLASS.field_mapping(d)

            # PP.pprint(Map)
            api_item_object,created = API_OBJECT.ITEM_API_CLASS.objects.get_or_create(source_id=d[Map['API']['source_id']])

            # if created:
    
            I,created = API_OBJECT.ITEM_CLASS.objects.get_or_create(
                name =d['title'],
                api_type = ContentType.objects.get_for_model(api_item_object),
                object_id = api_item_object.id,
            )
            I.brand = d[Map['item']['fields']['brand']]
            I.save()
            API_OBJECT.STYLIST_ITEM_CLASS.objects.get_or_create(
                                                                    stylist=API_OBJECT.retailer,
                                                                    item=I
                                                                )

            # get all the images associated with this product
            for index,image in enumerate(API_OBJECT.ITEM_API_CLASS.get_images(d)):
                path,identifier = image
                Picture = API_OBJECT.IMAGE_CLASS.already_exists(identifier,API_OBJECT.retailer)
                if not Picture:
                    out = tempfile.NamedTemporaryFile()
                    out.write(urllib.urlopen(path).read())
                    Picture = API_OBJECT.IMAGE_CLASS.objects.create(identifier=identifier,image=File(out, os.path.basename(path)),retailer=API_OBJECT.retailer,item=I)

                if index == 0:
                    I.featured_image = Picture
                    I.save()

            # get all the variations
            for v in API_OBJECT.get_variations(d):

                api_variation_object,created = API_OBJECT.VARIATION_API_CLASS.objects.get_or_create(source_id=v[Map['itemtype']['fields']['source_id']])
                size_string = 'ONE SIZE'
                color_string = 'ONE COLOR'

                # PP.pprint( Map['itemtype']['fields'])
                if Map['itemtype']['fields'].has_key('size'):
                    size_string = v[Map['itemtype']['fields']['size']]

                s,created = API_OBJECT.SIZE_CLASS.objects.get_or_create(
                    size=size_string,
                    retailer = API_OBJECT.retailer,
                )

                if Map['itemtype']['fields'].has_key('custom_color_name'):
                    color_string =v[Map['itemtype']['fields']['custom_color_name']]
                

                try:
                    it = API_OBJECT.ITEM_TYPE_CLASS.objects.get(
                        item = I,
                        size = s,
                        custom_color_name = color_string
                    )
                except:
                    it = API_OBJECT.ITEM_TYPE_CLASS.objects.create(
                        item = I,
                        size = s,
                        custom_color_name = color_string
                    )

                it.api_type = ContentType.objects.get_for_model(api_variation_object)
                it.object_id = api_variation_object.id
                it.inventory = v[Map['itemtype']['fields']['inventory']]

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
    API_OBJECT.update_in_progress = False
    API_OBJECT.save()



