from PIL import ImageEnhance,Image,ImageChops,ImageOps,ImageColor
import os

from django.core.files import File
import StringIO
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings

from queued_storage.tasks import Transfer

from johnny.cache import enable


from celery import task

def get_dominant_color(canvas):
    pallette = Image.new("RGB",canvas.size)
    pallette.paste(canvas)
    pallette = ImageOps.posterize(pallette,3)
    return sorted(pallette.getcolors(pallette.size[0]*pallette.size[1]))[-1:][0][1]
        


@task(name='racks.prettify_image')
def prettify(instance,refresh=False):
    enable()
    pic = None
    outpic = None
    try:
        if not instance.medium or refresh and (instance.image or instance.pretty_image):
            try:
                pic = Image.open(instance.image.file)
            except:
                if os.path.exists(instance.image.path):
                    pic = Image.open(instance.image.path)
                else:
                    print 'failed to find original image'
            if pic:
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
                #causes sorl to premake thumbs for this new image
            if not outpic:
                try:
                    outpic = Image.open(instance.pretty_image.file)
                    print 'found pretty image'
                except Exception,e:
                    print e
                    try:
                        outpic = Image.open(instance.pretty_image.storage.local.open(instance.pretty_image.name))
                    except:
                        print instance.pretty_image.path
                        print instance.pretty_image.storage 
                        print 'no pretty image for ', instance
                        raise

            if outpic:            
                for key,val in settings.THUMB_SIZES.items():
                    temp = NamedTemporaryFile(delete=True)
                    newpic = outpic.copy()
                    newpic.thumbnail(val,Image.ANTIALIAS)

                    if key == 'large':
                        instance.width = newpic.size[0]
                        instance.height = newpic.size[1]

                        #get color info about the edges
                        if instance.width<instance.height:
                            rightedge = newpic.crop((newpic.size[0]-3,0,newpic.size[0],newpic.size[1]))
                            color  = get_dominant_color(rightedge)
                            instance.bg_color = str(color)


                    newpic.save(temp.name+str(instance.id),'jpeg')
                    getattr(instance,key).save("%d_%s.jpg"%(instance.id,key), File(open(temp.name+str(instance.id),'rb')))

                    temp.close()
                    # newpic.close()
                    # rightedge.close()
                    # outpic.close()

                print 'saved sizes for ',instance
                print 'height:', instance.height
                print 'width:', instance.width
                instance.save()
    except Exception, e:
        try:
            if instance.item:
                pass
                # instance.item.approved = False
                # instance.item.delete()
            print e
            if settings.DEBUG:
                if instance.item:
                    if not instance.item.item_image_set.all().count() >= 2:
                        instance.item.approved = False
                        instance.item.save()
                    instance.delete()
        except Exception,e:
            print e
            


@task(name='racks.set_sizes')
def set_size(instance):
    pic = Image.open(instance.pretty_image.file)
    instance.width = pic.size[0]
    instance.height = pic.size[1]
    instance.save()
