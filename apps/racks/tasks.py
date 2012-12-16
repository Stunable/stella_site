from PIL import ImageEnhance,Image,ImageChops,ImageOps,ImageColor
import os

from django.core.files import File
import StringIO
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings



def get_dominant_color(image):
    pallette = Image.new("RGB",image.size)
    pallette.paste(image)
    pallette = ImageOps.posterize(pallette,3)
    c = pallette.getcolors(pallette.size[0]*pallette.size[1])
    #print c
    return c[-1:][0][1]

def prettify(instance):
    pic = Image.open(instance.image.file)
    enhancer  = ImageEnhance.Contrast(pic)
    outpic = enhancer.enhance(1.1)

    temp = NamedTemporaryFile(delete=True)
     
    grad = Image.open(os.path.join(settings.PROJECT_ROOT,'static','item_grad.jpg'))
    gradsize = grad.resize(outpic.size)
    try:
        outpic = ImageChops.add(outpic,gradsize)
    except:
        print 'error adding gradient:',instance


    outpic.save(temp.name+str(instance.id),'jpeg')


    instance.pretty_image.save("%d_pretty.jpg"%instance.id, File(open(temp.name+str(instance.id),'rb')))
    instance.save()