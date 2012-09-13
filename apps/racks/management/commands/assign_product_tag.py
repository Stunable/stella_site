from django.core.management.base import NoArgsCommand
from stella_crawler.models import Item as CrawledItem
from racks.models import Item, Item_Category, Rack, Rack_Item
import json
from django.contrib.auth.models import User
import sys
from apps.tagging.models import Tag
from django.conf import settings

class Command(NoArgsCommand):
    help = ""

    def handle_noargs(self, **options):
        # delete every existing item
        groups = settings.PRODUCT_GROUPS    
        
        acum = {} # 'brand': {, sum: , count: })
        
        for obj in Item.objects.all():
            brand = obj.brand.strip()
            if brand not in acum:
                acum[brand] = {'sum': 0, 'count': 0 }
            price = float(obj.price)
    
            acum[brand]['sum'] += price
            acum[brand]['count'] += 1
        
    
        for (brand, value) in acum.items():
            av = value['sum']/value['count']
            av = float("%.02f" % av)
            value['val'] = av
                    
        for obj in Item.objects.all():
            tags = [tag.name for tag in Tag.objects.get_for_object(obj) if not tag.name.startswith('product_group_')]
            for (group, (val_min, val_max)) in groups.items():
                av_price = acum[obj.brand]['val']
                
                if av_price > val_min and av_price < val_max:
                    tags.append(group)
                    print av_price, group
                 
            Tag.objects.update_tags(obj, ','.join(tags))
            
        print 'Finished uploading product group based on avarage price of the brand'
            
                
            
            

            
        