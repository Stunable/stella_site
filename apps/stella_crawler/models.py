from django.db import models

class Item(models.Model):
    # All items have these fields
    item_id = models.CharField(max_length=500, null=True, blank=True)
    brand = models.CharField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=19,decimal_places=2, null=True, blank=True)
    fabric = models.CharField(max_length=500, null=True, blank=True)
    colors = models.CharField(max_length=500, null=True, blank=True)          # There may be more than one color
    num_colors = models.IntegerField(null=True, blank=True)
    length = models.DecimalField(max_digits=19,decimal_places=2, null=True, blank=True)
    fabrication = models.CharField(max_length=500, null=True, blank=True)
    embellishment = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)           # The name of the item
    print_style = models.CharField(max_length=500, null=True, blank=True)    # The print
    
    # Specific fields that only apply to certain items
    wash = models.CharField(max_length=500, null=True, blank=True)           # Denim
    rise = models.CharField(max_length=500, null=True, blank=True)           # Denim, Pants
    fit = models.CharField(max_length=500, null=True, blank=True)            # Denim 
    distressing = models.CharField(max_length=500, null=True, blank=True)    # Denim
    neckline = models.CharField(max_length=500, null=True, blank=True)       # Tops, dresses, sweaters
    sleeves = models.CharField(max_length=500, null=True, blank=True)
    guage_weight = models.CharField(max_length=500, null=True, blank=True)
    sheer_level = models.CharField(max_length=500, null=True, blank=True)
    lining = models.CharField(max_length=500, null=True, blank=True)
    waist_rise = models.CharField(max_length=500, null=True, blank=True)
    padding = models.CharField(max_length=500, null=True, blank=True)
    trim = models.CharField(max_length=500, null=True, blank=True)

    # These define the item's type
    category = models.CharField(max_length=500, null=True, blank=True)
    subcategory = models.CharField(max_length=500, null=True, blank=True)

    # The item's image(s)
    image_urls = models.URLField(max_length=500, null=True, blank=True)
    
    def __unicode__(self):
        return self.name