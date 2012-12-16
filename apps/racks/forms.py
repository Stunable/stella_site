from django import forms
from django.db.models import Q
from apps.racks.models import Rack, Brand, Size, Color
from django.contrib.auth.models import User
from apps.racks.models import Item
from django.db.models import Q
from apps.common.forms import AjaxModelForm
from apps.racks.models import ItemType,ProductImage

from django.forms.util import flatatt
from django.utils.safestring import mark_safe

import types

class RackForm(forms.ModelForm):    
    #shared_users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),required=False, widget=forms.SelectMultiple)
    #rack_items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), required=False, widget=forms.SelectMultiple)
    
    class Meta:
        model = Rack
        exclude = ['user', 'rack_items', 'shared_users', 'category', 'publicity']
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(RackForm, self).__init__(*args, **kwargs)
        
    def clean_name(self):
        new_name = self.cleaned_data.get('name')
        racks = Rack.objects.filter(user=self.user, name__iexact=new_name)
        
        if racks.count() > 0:
            raise forms.ValidationError("This rack name has already been used! Please choose another one!")
        return self.cleaned_data['name']

class RackNameEditForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = ['name']

class RackEditForm(forms.ModelForm):
    shared_users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),required=False, widget=forms.SelectMultiple)
    rack_items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), required=False, widget=forms.SelectMultiple)
    
    class Meta:
        model = Rack
        exclude = ['user', 'category', 'publicity']
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(RackEditForm, self).__init__(*args, **(kwargs))

class InsertExistingItemToRackForm(forms.ModelForm):
    rack_items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), required=False, widget=forms.SelectMultiple)
    class Meta:
        model = Rack
        exclude = ['name', 'user', 'shared_users', 'category', 'publicity']
    
    def __init__(self, rack=None, *args, **kwargs):
        self.current_rack = rack
        super(InsertExistingItemToRackForm, self).__init__(*args, **(kwargs))
        remain_items = Item.objects.all()
        exclude = []
        for item in self.current_rack.rack_items.all():
            exclude.append(item.id)
        
        remain_items = remain_items.exclude(id__in = exclude)
        self.fields['rack_items'].queryset = remain_items

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        
class AddSizeForm(forms.ModelForm):
    class Meta:
        model = Size
        
    def clean_size(self):
        size = self.cleaned_data.get('size') 
        if size:
            sizes = Size.objects.filter(size=size) 
            if sizes.count() > 0:
                raise forms.ValidationError("This Size had already existed")                
            
            return size
        else:
            raise forms.ValidationError("Please enter a size number")
    
class AddColorForm(forms.ModelForm):
    class Meta:
        model = Color
    
    def clean_name(self):
        name = self.cleaned_data.get('name') 
        if name:
            colors = Color.objects.filter(name=name) 
            if colors.count() > 0:
                raise forms.ValidationError("This Color had already existed")
            return name
        else:
            raise forms.ValidationError("Please enter a color name")

def addPlus(widget,name,selection,queryset,url,label):

    def render_with_plus(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append(u'</select>')
        output.append('<div style="margin-left: 150px;margin-top: 5px;"> <a class="addProductImage" target="blank" href="%s"><span>+</span> Add %s</a></div>'%(url,label))
        print output
        return mark_safe(u'\n'.join(output))

    widget.render = types.MethodType(render_with_plus,widget)
    return widget

class ItemInventoryForm(AjaxModelForm):
    class Meta:
        model = ItemType

def item_inventory_form_factory(retailer):
    class ItemInventoryForm(AjaxModelForm):
        item = forms.ModelChoiceField(queryset=Item.objects.all(), widget=forms.HiddenInput())
        color = forms.ModelChoiceField(queryset=Color.objects.filter(Q(retailer=None)|Q(retailer=retailer)))
        size = forms.ModelChoiceField(queryset=Size.objects.filter(Q(retailer=None)|Q(retailer=retailer)))
        image = forms.ModelChoiceField(queryset=ProductImage.objects.filter(Q(retailer=None)|Q(retailer=retailer)))
        
        class Meta:
            model = ItemType
            
        def clean_inventory(self):
            inventory = self.cleaned_data.get('inventory')
            if int(inventory) < 1:
                raise forms.ValidationError("Inventory must be positive!")
            return self.cleaned_data.get('inventory')

        def __init__(self,*args,**kwargs):
            super(ItemInventoryForm,self).__init__(*args,**kwargs)
            print self.fields['image']


            addPlus(self.fields['image'].widget, 'image', None, ProductImage.objects.filter(Q(retailer=None)|Q(retailer=retailer)),'#','Product Image')


            self.fields['image'].widget.attrs['class'] = "imageselector"
            self.fields['image'].empty_label = '/static/images/choosepic.png'




    return ItemInventoryForm


        