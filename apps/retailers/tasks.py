from utils import getXLSdata
import zipfile
import os

from racks.models import Item,ItemType,Color,Size
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

def process_upload(upload,throughModel):

    errors = []

    path = extract_zip(upload.uploaded_zip.path)
    xls = find_xls(path)

    folder = os.path.dirname(xls)


    for d in getXLSdata(xls):
        #BRAND', u'PRODUCT NAME', u'PRODUCT IMAGE', u'PRODUCT DESCRIPTION', u'COLORWAY(S)', u'SIZES', u'INV_SIZES', u'MSRP (US DOLLARS)'
        brand,name,image,description,colorways,sizes,inv_sizes,msrp = d
        imgpath = os.path.join(folder,image+'.jpg')
        if os.path.exists(imgpath):
            try:
                pic = File(open(imgpath,'rb'))
            except:
                errors.append('Problem dealing with picture: %s'%os.path.basename(imgpath))

            try:
                I = Item.objects.create(
                    brand=brand,
                    name =name,
                    price=msrp,
                    description=description,
                    image=pic,
                )
            except Exception, e:
                errors.append(str(e))
                return errors

            si = throughModel.objects.create(
                stylist = upload.retailer.user,
                item = I
            )

    #Do ItemTypes
            try:
                sizelist = []
                invsizes = inv_sizes.split(',')

                c,created = Color.objects.get_or_create(
                    retailer = upload.retailer.user,
                    name = colorways
                )


                for s in sizes.split(','):
                    s,created = Size.objects.get_or_create(
                        size=s,
                        retailer = upload.retailer.user,
                    )
                    sizelist.append(s)

                for i,sz in enumerate(sizelist):
                    ItemType.objects.create(
                        item=I,
                        color=c,
                        size=sz,
                        custom_color_name=colorways,
                        inventory=int(invsizes[i])
                    )
            except Exception,e:
                errors.append(str(e))
        else:
            errors.append('No Image Found for Item: '+name)
            
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





