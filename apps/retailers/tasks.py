from utils import getXLSdata
import zipfile
import os
import copy

from racks.models import Item,ItemType,Color,Size,ProductImage
from django.core.files import File

# Item
# image = models.ImageField(upload_to='upload', null=True, blank=True, verbose_name="Product Image")
# pretty_image = models.ImageField(upload_to='upload', null=True, blank=True, verbose_name="Product pretty Image",storage=OverwriteStorage())
# bg_color = models.CharField(max_length=32,default='white',blank=True,null=True)

# brand = models.CharField(max_length=200, null=True, blank=True)
# name = models.CharField(max_length=200, verbose_name='Product Name')
# price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Retail Price')
# is_onsale = models.BooleanField(default=False, verbose_name='Currently On Sale?')
# description = models.TextField()
# category = models.ForeignKey(Category, verbose_name='Product Category', null=True, blank=True)
# fabrics = models.CharField(max_length=200, null=True, blank=True)
# image_urls = models.TextField(null=True, blank=True)
# order = models.IntegerField(default=0, db_index=True)
# is_deleted = models.BooleanField(default=False,blank=True)

# retailers = models.ManyToManyField(User, through='retailers.StylistItem', null=True, blank=True)
# sizes = models.ManyToManyField(Size, through='racks.ItemType', null=True, blank=True)
# colors = models.ManyToManyField(Color, through='racks.ItemType', null=True, blank=True)
# created_date = models.DateField(auto_now=True, auto_now_add=True, default=datetime.date.today)

# approved = models.BooleanField(default=False)

# ItemType:
# item = models.ForeignKey('Item', related_name='types')
# color = models.ForeignKey('Color')
# size = models.ForeignKey('Size')
# custom_color_name = models.CharField(max_length=100, blank=True, null=True,
#                                      help_text="An optional custom name for the color of this item")
# inventory = models.PositiveIntegerField(default=0)

# Size
# size = models.CharField(max_length=30)
# description = models.TextField(null=True, blank=True)
# retailer = models.ForeignKey(User, blank=True, null=True)

# StylistItem
# stylist = models.ForeignKey(User)
# item = models.ForeignKey(Item)
def find_image(folder,image):
    for f in os.listdir(folder):
        # print f.lower()
        for ext in ['jpg','jpeg','png']:
            print image.replace('.'+ext,'')+'.'+ext
            if f.lower() == image.lower().replace('.'+ext,'')+'.'+ext:
                print 'GOT IT' , image.lower().replace('.'+ext,'')+'.'+ext
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

            if d[2] != prev[2]:#the image is different
                imgpath = find_image(folder,d[2])
                if imgpath:
                    pic = File(open(imgpath,'rb'))
                    Picture = ProductImage.objects.create(image=pic,retailer=upload.retailer.user)
                    # a new image has been created and is now the picture for the following items

            if Picture: # we don't proceed if there's no picture
                for i in range(0,len(d)):  #update our working info to use all the fields from the current row that aren't empty
                    if d[i].lstrip().rstrip():
                        current[i] = d[i]

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
                        image=Picture
                    )

                    if upload.retailer.user:
                        si = throughModel.objects.create(
                            stylist = upload.retailer.user,
                            item = I)



                c,created = Color.objects.get_or_create(
                    retailer = upload.retailer.user,
                    name = color
                )

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
                errors.append('No Image Found for Row: '+str(i))
        except Exception,e:
            errors.append('Error in Row '+i+':'+str(e))
        
        for i,f in enumerate(current):
            prev[i] = current[i]

    for error in errors:
        print error
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





