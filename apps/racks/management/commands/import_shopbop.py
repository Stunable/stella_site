from django.core.management.base import NoArgsCommand
from stella_crawler.models import Item as CrawledItem
from racks.models import Item, Item_Category, Rack, Rack_Item
import json
from django.contrib.auth.models import User

class Command(NoArgsCommand):
    help = ""

    def handle_noargs(self, **options):
        # delete every existing item        
        for i in Item.objects.all():
            i.delete()
        
        c = 0    

        # find the appropriate racks 
        racks = Rack.objects.all()[:]
        
        administrator = User.objects.get(username='admin')
        
        category_count = {}        
        
        for i in CrawledItem.objects.all():
            if i.category in category_count and category_count[i.category] > 20:
                continue
            
            if i.category in category_count:
                category_count[i.category] = category_count[i.category] + 1
            else:
                category_count[i.category] = 0
            
            try:
                # colors field stored as "[u'red', u'green']"
                c += 1
                                
                colors = fabrics = image_urls = []
                
                try:
                    colors = i.colors and i.colors.replace("u'", '"').replace("'", '"')
                    colors = json.loads(colors)
                    
                    fabrics = i.fabric.lstrip('0123456789% ') and i.fabric.replace("u'", '"').replace("'", '"')             
                    fabrics = json.loads(fabrics)
                    
                    image_urls = i.image_urls and i.image_urls.replace("u'", '"').replace("'", '"')             
                    image_urls = json.loads(image_urls)            
                except:
                    pass
                
                # tagging products
                tags = [i.brand]
                tags.extend(colors)
                tags.extend(fabrics)
                tags = [tag.lstrip('0123456789% ').lower().replace(' ', '_') for tag in tags]            
                
                ic = Item_Category.objects.filter(name=i.category)[:]
                if ic:
                    ic = ic[0]
                else:
                    ic = Item_Category(name=i.category)
                    ic.save()
                
                
                product = Item(name=i.name,
                               price=i.price,
                               brand=i.brand,
                               colors = ','.join(colors)[:199],
                               fabrics=','.join(fabrics)[:199],
                               category=ic,
                               tags=','.join(tags),
                               image_urls=','.join(image_urls),
                               description=i.description,
                               label=i.brand,                   
                               )
                product.save()
                
                for rack in racks:
                    
                    
#                    rack_name = rack.name.lower()
#                    if rack_name.endswith('es'):
#                        rack_name = rack_name[:-2]
#                        
#                    if rack_name.endswith('s'):
#                        rack_name = rack_name[:-1]
#                    
#                    rack_name = ('dress' in rack_name and 'dress') or rack_name
#                    rack_name = ('winter' in rack_name and 'winter') or rack_name
#                    rack_name = ('weekend' in rack_name and 'weekend') or rack_name
                    
                    if rack.name.lower() == i.category.lower():
                        rack_item = Rack_Item(rack=rack, item=product, user=administrator)
                        rack_item.save()
            except:
                pass # missing some items would not be a big problem            
            
            
            
            
            
        