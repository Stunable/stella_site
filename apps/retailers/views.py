from django.shortcuts import redirect
from django.forms import ValidationError
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from retailers.forms import RetailerProfileCreationForm, RetailerEditForm, ItemForm,\
                            ItemEditForm, LogoUploadForm
from retailers.models import RetailerProfile, StylistItem, ShippingType
from racks.models import Item, Rack, Rack_Item
from apps.common import json_view
from django.views.decorators.csrf import csrf_exempt

from cart.models import Item as CartItem, Purchase
import datetime
from django.http import HttpResponse
from apps.racks.forms import item_inventory_form_factory
from django.forms.models import inlineformset_factory
from apps.racks.models import ItemType
from apps.common.forms import AjaxBaseForm
from apps.racks.forms import ItemInventoryForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

try:
    import simplejson as json
except ImportError:
    import json


def create_retailer_profile(request, template="retailers/retailer_profile_create.html"):
    ctx = {}
    if request.method == "POST":
        form = RetailerProfileCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_retailer = form.save()
            template = "accounts/thank-you.html"
            return redirect(reverse('retailer_terms', args=[new_retailer.id]))
            
        else:
            ctx['day_1'] = request.POST.get('day_1')
            ctx['day_2'] = request.POST.get('day_2')
            ctx['time_picker_1'] = request.POST.get('time_picker_1')
            ctx['time_picker_2'] = request.POST.get('time_picker_2')
    else:        
        form = RetailerProfileCreationForm()
    
    ctx['form']=form
    return direct_to_template(request, template, ctx)

def terms(request, retailer_id, template='retailers/terms.html'):
    ctx = {'retailer_id': retailer_id}
    return direct_to_template(request, template, ctx)

RETAILER_INFORM_SUBJECT = "retailers/retailer_inform_subject.txt"
RETAILER_INFORM_MESSAGE = "retailers/retailer_inform_message.txt"

def terms_complete(request, retailer_id, template="accounts/thank-you.html"):
    ctx = {'retailer': True}
    
    # send email to notify user
    retailer = get_object_or_404(RetailerProfile, pk=retailer_id)
    email_ctx = {"retailer": retailer}
    subject = render_to_string(RETAILER_INFORM_SUBJECT, email_ctx)
    email_message = render_to_string(RETAILER_INFORM_MESSAGE, email_ctx)
    send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [retailer.email_address])
    
    return direct_to_template(request, template, ctx)


@login_required
@csrf_exempt
def update_retailer_profile(request, template="retailers/account_information.html"):
    ctx = {}
    try:
        retailer_profile = RetailerProfile.objects.get(user=request.user)
        if request.method == "POST":
            form = RetailerEditForm(request.POST, instance=retailer_profile)
            if form.is_valid():
                user = request.user
                # TODO: check and fix bug here
                if form.cleaned_data.get('shipping_type'):
                    retailer_profile.shipping_type = form.cleaned_data.get('shipping_type')
                if form.cleaned_data.get('email_address'):
                    retailer_profile.email_address = form.cleaned_data.get('email_address')
                    user.username = retailer_profile.email_address
                    user.email = retailer_profile.email_address
                if form.cleaned_data.get('password'):
                    user.set_password(form.cleaned_data.get('password'))
                if request.POST.get('account_page'):
                    template="retailers/retailer_information.html"
                
                form.save()
                user.save()
                
                retailer_profile.save()
                
                if request.POST.get('others'):
                    if request.POST.get('new_shipping_type') and len(request.POST.get('new_shipping_type')):
                        new_shipping_type = ShippingType(name=request.POST.get('new_shipping_type'))
                        new_shipping_type.save()
                        retailer_profile.shipping_type.add(new_shipping_type.id)
                        retailer_profile.save();
                    
                
        else:        
            form = RetailerEditForm(instance=retailer_profile)
        
        ctx['form']=form
        ctx['retailer_profile'] = retailer_profile
    except:
        #login as user
        return redirect(reverse("home"))
    return direct_to_template(request, template, ctx)


def inventory_type_formset_factory(retailer, data=None, instance=None):
    # All so we can limit the Color and Size choices on the ItemInventoryForm
    # by passing the retailer (instance of User) to it's constructor.
#    form = ItemInventoryForm(retailer)
    form = item_inventory_form_factory(retailer)
    formset_class = inlineformset_factory(Item, ItemType, form=form, extra=5, can_delete=True)
    
    def errors_as_json(self, strip_tags=False):
        error_summary = {}
        errors = {}
        counter = 0
        for form_error in self.errors:
            for error in form_error.iteritems():
                if self.prefix:
                    errors.update({self.prefix + '-' + str(counter) + '-' + error[0] : unicode(striptags(error[1]) \
                        if strip_tags else error[1])})
                else:
                    errors.update({error[0] : unicode(striptags(error[1]) \
                        if strip_tags else error[1])})
            counter += 1
        error_summary.update({'errors' : errors })
        return error_summary
    
    formset_class.errors_as_json = errors_as_json
    
    return formset_class(data, instance=instance)


@login_required
def delete_item(request, item_id, template='racks/item_management.html'):
    ctx = {}
    delete_item = get_object_or_404(Item, pk=item_id)
    delete_item.delete()
    return redirect(reverse("item"))

@login_required
def edit_item(request, item_id=None, template='retailers/add_item.html'):
    ctx = {}
    
    if item_id:
        item_instance = Item.objects.get(pk=item_id)
    else:
        item_instance = Item()
        
    post = request.POST.copy()
    if request.method == 'POST':
        response = {'success' : True, 'errors': {}}
        try:
            form = ItemForm(request.user, post, request.FILES, instance=item_instance)
            
            if not form.is_valid():
                response.update({'success' : False})
                response['errors'].update(form.errors_as_json()['errors'])
            else:
                item_instance = form.save(commit=False)  
    
            
            inventory_form = inventory_type_formset_factory(request.user, post, item_instance)        
    
            if not inventory_form.is_valid():
                response.update({'success' : False})
                response['errors'].update(inventory_form.errors_as_json()['errors'])
            else:
                instances = inventory_form.save(commit=False)
                if not instances and not item_instance.pk:
                    response.update({'success' : False})
                    response['errors'].update({'types-0-inventory': '<ul class="errorlist"><li>This field is required.</li></ul>'})
            
            if response['success']:
                if not item_instance.pk:
                    item_instance.save()
                
                try:
                    inventory_form = inventory_type_formset_factory(request.user, post, item_instance)
                    if inventory_form:
                        inventory_form.save()
                except IndexError, e:
                    # TODO
                    pass
                except:
                    # TODO
                    pass
                
                item_instance.save()
                
        except Exception, e:
            response.update({'success' : False, 'message': str(e)})
                   
        return HttpResponse(json.dumps(response, ensure_ascii=False), mimetype='application/json')
    else:
        try:
            initial = {'Colors': [i.pk for i in item_instance.colors.all()], 
                                 'Sizes': [i.pk for i in item_instance.sizes.all()]}
        except:
            initial={}
        form = ItemForm(instance=item_instance, initial=initial)
    
    if request.is_ajax():
        template = 'racks/size_input.html'
    
    
    ctx['form'] = form #MyForm()
    ctx['inventory_forms'] = inventory_type_formset_factory(request.user, None, item_instance)
    ctx['retailer_profile'] = RetailerProfile.objects.get(email_address=request.user.email)
    ctx['item_pk'] = item_id

    return direct_to_template(request, template, ctx)

@login_required
def add_item(request, item_id=None, template='retailers/add_item.html'):
    return edit_item(request, item_id, template)

@login_required 
def product_list(request, template="retailers/product_list.html"):
    try:
        retailer_profile = RetailerProfile.objects.get(user=request.user)
        pl = []
        s = set()
        for si in StylistItem.objects.filter(stylist=request.user):
            if si.item.pk not in s:
                pl.append(si)
                s.add(si.item.pk)
        
        ctx = {'retailer_profile': retailer_profile, 'product_list': pl}
    except:
        return redirect(reverse("home"))
    return direct_to_template(request, template, ctx)

@login_required
def retailer_information(request, name, template="retailers/retailer_information.html"):
    retailer_profile = RetailerProfile.objects.get(user=request.user)
    shipping_types = ShippingType.objects.all()
    form = RetailerEditForm(instance=retailer_profile)
    ctx = {'retailer_profile': retailer_profile, 'shipping_types': shipping_types, 'form': form}
    return direct_to_template(request, template, ctx)

@json_view
@login_required
def retailer_logo_upload(request):
    try:
        retailer_profile = RetailerProfile.objects.get(email_address=request.user.email)
        if request.method == "POST":
            form = LogoUploadForm(request.POST, request.FILES, instance=retailer_profile)
            form.save()
            return {'result': 'ok', 'source': retailer_profile.logo_image}
        else:
            raise ValidationError("Errors Occur!")
    except:
        pass
    
def retailer_list(request, template='retailers/retailer_list.html'):
    retailer_list = RetailerProfile.objects.all()
    return direct_to_template(request, template, {'retailer_list': retailer_list})

def retailer_modal(request, item_id, template="retailers/retailer_information_modal.html"):
    current_item = get_object_or_404(Item, pk=item_id)
    stylist_item = StylistItem.objects.filter(item=current_item)
    user = stylist_item[0].stylist
    retailer_profile = RetailerProfile.objects.get(user=user)
    return direct_to_template(request, template, {'retailer_profile': retailer_profile})    

@login_required
def order_history(request, template='retailers/order_history.html'):
    ctx = {}
    try:
        retailer_profile = RetailerProfile.objects.get(user=request.user)
        shipping_types = ShippingType.objects.all()
        form = RetailerEditForm(instance=retailer_profile)
        ctx = {'retailer_profile': retailer_profile, 'shipping_types': shipping_types, 'form': form}
    
        _from = request.GET.get('from')
        _to = request.GET.get('to')
        
        items = ItemType.objects.filter(item__retailers=request.user)
        purchases = Purchase.objects.filter(cart__item__object_id__in=items).distinct()
        
        if not _from and not _to:
            today = datetime.date.today()
            thirty_days_ago = today - datetime.timedelta(days=30)
            purchases = purchases.filter(purchased_at__gte=thirty_days_ago)
        else:
            if _from:
                purchases = purchases.filter(purchased_at__gte=_from)
            if _to:
                purchases = purchases.filter(purchased_at__lte=_to)
                        
        for purchase in purchases:
            purchase.this_retailer_items = purchase.cart.item_set.filter(object_id__in=items) 
        
        ctx['purchases']= purchases
    except:
        #login as regular user
        return redirect(reverse("home"))
    return direct_to_template(request, template, ctx)

@login_required
def view_all_products(request, retailer_id):
    retailer = get_object_or_404(RetailerProfile, pk=retailer_id)
    try:
        user_racks = Rack.objects.filter(owner=request.user, name=retailer.name)
        if user_racks.count() > 0:
            pass
        else:
            new_rack = Rack.objects.create(name=retailer.name, owner=request.user, publicity=0)
            retailer_items = StylistItem.objects.filter(stylist=retailer.user)
            for retailer_item in retailer_items:
                Rack_Item.objects.create(item=retailer_item.item, rack=new_rack, user=request.user)
    except:
        pass
    
    return redirect(reverse("racks_detail", args=[user_racks[0].id]))


@login_required
def update_order_item(request, order_item_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        item = CartItem.objects.get(pk=order_item_id)
        if new_status == 'shipped':
            item.mark_as_shipped(request, request.POST.get('tracking_number'))
            
        if new_status == 'return-item':
            item.return_item(request)
            
        if new_status == 'cancel-order-return':
            item.cancel_order_return()    
        
    return HttpResponse(json.dumps({'success': True}, ensure_ascii=False), mimetype='application/json')
        
        
    