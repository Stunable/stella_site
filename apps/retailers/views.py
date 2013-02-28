from django.shortcuts import redirect
from django.forms import ValidationError
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from retailers.forms import RetailerProfileCreationForm, RetailerEditForm, ItemForm,\
                            ItemEditForm, LogoUploadForm
from retailers.models import RetailerProfile, StylistItem, ShippingType,ProductUpload,APIConnection,ShopifyConnection
from racks.models import Item, Rack, Rack_Item
from apps.common import json_view
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

from cart.models import Item as CartItem, Purchase,Shipment,Checkout
import datetime
from django.http import HttpResponse,HttpResponseRedirect
from apps.racks.forms import item_inventory_form_factory

from apps.cms.models import SiteTextContent

from django.forms import HiddenInput

from django.forms.models import inlineformset_factory
from apps.racks.models import ItemType,ProductImage
from apps.common.forms import AjaxBaseForm
from apps.accounts.models import ShippingInfo
from apps.racks.forms import ItemInventoryForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.forms.models import modelform_factory
from wepay import WePay

import urllib
import urllib2
from datetime import date,timedelta

# from apps.cart.plugins.taxcloud import TaxCloudClient
# TCC = TaxCloudClient()

from tasks import update_API_products

from cart.plugins.create_shipment import ship_it

try:
    import simplejson as json
except ImportError:
    import json

import os



def get_retailer_profile(request,retailer_id=None):
    if retailer_id:
        return RetailerProfile.objects.get(id=retailer_id)
    if request.user.is_staff:
        return RetailerProfile.objects.get(id=request.GET.get('retailer',None))
    return RetailerProfile.objects.get(user=request.user)





def retailer_help(request,  template="retailers/retailer_help.html"):
    retailer_profile = get_retailer_profile(request)

    ctx = {'retailer_profile':retailer_profile}
    return direct_to_template(request, template, ctx)

def create_retailer_profile(request, template="retailers/retailer_profile_create.html"):

    if request.method == "POST":
        form = RetailerProfileCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_retailer = form.save()
            request.session['retailer_id'] = new_retailer.id
            print request.session.items()
            template = "accounts/thank-you.html"
            return redirect(reverse('retailer_terms', args=[new_retailer.id]))
        else:
            print form.errors
    else:        
        form = RetailerProfileCreationForm()
    
    ctx = {'form':form}
    return direct_to_template(request, template, ctx)

def terms(request, retailer_id, template='retailers/terms.html'):
    ctx = {'retailer_id': retailer_id}
    return direct_to_template(request, template, ctx)

RETAILER_INFORM_SUBJECT = "retailers/retailer_inform_subject.txt"
RETAILER_INFORM_MESSAGE = "retailers/retailer_inform_message.txt"


def setup_wepay(request):
    code = request.GET.get('code',None)
    if code:
        url = 'https://'+{'stage':'stage.','production':'' }[settings.WEPAY_STAGE]+'wepayapi.com/v2/oauth2/token'
        data = {
          "client_id":settings.WEPAY_CLIENT_ID,
          "client_secret":settings.WEPAY_CLIENT_SECRET,
          "redirect_uri":settings.RETAILER_SUBDOMAIN+'retailers/wepay/',
          "code":code,
        }
        url += '?'+urllib.urlencode(data)
        # print url
        response = urllib2.urlopen(url)
        resp_data = json.loads(response.read())
        # print resp_data
        print request.session.keys()
        #{"user_id":121042660,"access_token":"e4423c3a3a3a3f62aa53151a9b2fca1718af0bc78b40dba6578716b9a2979fa5","token_type":"BEARER"}
        if request.session.get('retailer_id',None):

            retailer_profile = get_retailer_profile(request, retailer_id=request.session.get('retailer_id'))
        else:
            retailer_profile = get_retailer_profile(request)
        # retailer_profile.wepay_acct = resp_data['user_id']
        retailer_profile.wepay_token = resp_data['access_token']

        WEPAY = WePay(settings.WEPAY_PRODUCTION, resp_data['access_token'])


        # response = WEPAY.call('/account/find', {
        #     'name': 'stunable payments account',
        # })

        # if type(response) == type([]):
        #     if len(response):
        #         retailer_profile.wepay_acct = response[-1]['account_id']
        #     else:
        try:
            response = WEPAY.call('/account/create', {
                'reference_id': 'stunable_payment_account_001',
                'name': 'stunable payments account',
                'description': 'your account for transactions with Stunable.com. Email payment@stunable.com for any questions.'
            })

            retailer_profile.wepay_acct = response['account_id']
        except:
            try:
                response  = WEPAY.call('/account/find',{
                    'reference_id': 'stunable_payment_account_001',
                    'name': 'stunable payments account',
                })[0]
                retailer_profile.wepay_acct = response['account_id']
                print 'user already had stunable_payment_account_001'
            except:
                raise



        retailer_profile.save()

        template="accounts/thank-you.html"
        ctx = {'retailer': True}
        return direct_to_template(request, template, ctx)


    else:
        url = 'https://'+{'stage':'stage.','production':'' }[settings.WEPAY_STAGE]+'wepay.com/v2/oauth2/authorize?client_id='+settings.WEPAY_CLIENT_ID+'&redirect_uri='+settings.RETAILER_SUBDOMAIN+'wepay/&scope=manage_accounts,collect_payments,refund_payments,preapprove_payments,send_money'
        return HttpResponseRedirect(url)


def terms_complete(request, retailer_id, template="accounts/thank-you.html"):
    ctx = {'retailer': True}

    if int(request.session['retailer_id']) != int(retailer_id):
        print request.session['retailer_id']
        raise

    print request.session.items()
    
    # send email to notify user
    retailer = get_object_or_404(RetailerProfile, pk=retailer_id)
    email_ctx = {"retailer": retailer}
    subject = render_to_string(RETAILER_INFORM_SUBJECT, email_ctx)
    email_message = render_to_string(RETAILER_INFORM_MESSAGE, email_ctx)
    if not retailer.welcome_message_sent:
        send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [retailer.email_address])
        retailer.welcome_message_sent = True
        retailer.save()
    return setup_wepay(request)


@login_required
@csrf_exempt
def update_retailer_profile(request, template="retailers/account_information.html"):
    ctx = {}
    try:
        retailer_profile = get_retailer_profile(request)
        if request.method == "POST":
            form = RetailerEditForm(request.POST, instance=retailer_profile)
            if form.is_valid():
                # print 'VALID'
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
                print form.errors
                
        else:        
            form = RetailerEditForm(instance=retailer_profile)
        
        ctx['form']=form
        ctx['retailer_profile'] = retailer_profile
    except:
        raise
        #login as user
        return redirect(reverse("home"))
    return direct_to_template(request, template, ctx)


def inventory_type_formset_factory(retailer, data=None, instance=None,extra=1):
    # All so we can limit the Color and Size choices on the ItemInventoryForm
    # by passing the retailer (instance of User) to it's constructor.
#    form = ItemInventoryForm(retailer)
    form = item_inventory_form_factory(retailer)
    formset_class = inlineformset_factory(Item, ItemType, form=form, extra=extra, can_delete=True, exclude=['api_connection','object_id','api_type','position'])
    
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
    initial = None
    
    if item_id:
        item_instance = Item.objects.get(pk=item_id)
    else:
        item_instance = Item()


    retailer = get_retailer_profile(request)
    
    post = request.POST.copy()
    if request.method == 'POST':
        response = {'success' : True, 'errors': {}}
        try:
            form = ItemForm(request.user, post, request.FILES, instance=item_instance)
            
            if not form.is_valid():
                response.update({'success' : False})
                response['errors'].update(form.errors_as_json()['errors'])
            else:
                print 'saving item form'
                item_instance = form.save(commit=False)  
                item_instance._retailer = retailer
            print 'after save item form'
            
            inventory_form = inventory_type_formset_factory(request.user, post, item_instance)        
            # print inventory_form
            if not inventory_form.is_valid():
                response.update({'success' : False})
                response['errors'].update(inventory_form.errors_as_json()['errors'])
            else:
                instances = inventory_form.save(commit=False)
                print 'variation instances:',instances
                if not len(instances) and not item_instance.pk:
                    response.update({'success' : False})
                    response['errors'].update({'types-0-inventory': '<ul class="errorlist"><li>This field is required.</li></ul>'})
            
            if response['success']:
                form.finish_save()
                
                try:
                    inventory_form = inventory_type_formset_factory(request.user, post, item_instance)
                    if inventory_form:
                        new_thing = inventory_form.save()
                        # print new_thing
                except IndexError, e:
                    # TODO
                    raise
                    pass
                except:
                    # TODO
                    pass
                print 'saving instance line 287'
                
                
        except Exception, e:
            raise
            response.update({'success' : False, 'message': str(e)})
                   
        return HttpResponse(json.dumps(response, ensure_ascii=False), mimetype='application/json')
    else:
        try:
            initial = {'Colors': [i.pk for i in item_instance.colors.all()], 
                       'Sizes': [i.pk for i in item_instance.sizes.all()],
                       # 'brand': RetailerProfile.objects.get(user=request.user).name
                       }
        except:
            pass
            # initial={'brand': retailer.name}
        form = ItemForm(user=request.user,instance=item_instance, initial=initial)
    
    if request.is_ajax():
        template = 'racks/size_input.html'
    ctx['next']=request.get_full_path()
    ctx['image_upload_form'] = modelform_factory(ProductImage,fields=["image","item"])(initial={'retailer':retailer.id,'item':item_instance.id},prefix="new")
    ctx['image_upload_form'].fields['item'].widget = HiddenInput()
    ctx['item'] = item_instance
    ctx['form'] = form #MyForm()
    ctx['inventory_forms'] = inventory_type_formset_factory(request.user, None, item_instance,extra=1)


    # print ctx['inventory_forms']

    ctx['retailer_profile'] = retailer
    ctx['item_pk'] = item_id

    return direct_to_template(request, template, ctx)

@login_required
def add_item(request, item_id=None, template='retailers/add_item.html'):
    return edit_item(request, item_id, template)

def bulk_upload(request,upload_id=None,template="retailers/product_list.html"):
    uploadObject = None
    try:
        retailer_profile = get_retailer_profile(request)
    except:
        raise

    if upload_id:
        up = ProductUpload.objects.get(id=upload_id)
        pl = up.item_set.all()
        print pl
        ctx = {'retailer_profile': retailer_profile, 'product_list': pl, 'upload':up,'confirm':True}    
    else:            
        try:
            form = modelform_factory(ProductUpload,fields=['uploaded_zip'])()
            if request.method == 'POST':
                form = modelform_factory(ProductUpload,fields=['uploaded_zip'])(request.POST,request.FILES)
                if form.is_valid():
                    print 'valid form'
                    up = form.save(commit=False)
                    up.retailer = retailer_profile
                    up.save()

                    uploadObject = up
                    return product_list(request,upload=uploadObject)

            pl = retailer_profile.retailer_item_set.all()

            ctx = {'retailer_profile': retailer_profile, 'product_list': pl,'bulk_upload_form':form,'upload':uploadObject}
        except:
            raise
        # e redirect(reverse("home"))
    return direct_to_template(request, template, ctx)

@login_required 
def product_list(request, upload=None, template="retailers/product_list.html"):
    try:
        form = modelform_factory(ProductUpload,fields=['uploaded_zip'])()
        retailer_profile = get_retailer_profile(request)
        pl = retailer_profile.retailer_item_set.all()

        yesterday = date.today() - timedelta(days=1)

        for API_type in [ShopifyConnection]:
            need_updates = API_type.objects.filter(retailer=request.user,last_updated__lte=yesterday)
            if need_updates.count():
                for api in need_updates:
                    api.update_in_progress = True
                    api.last_updated = datetime.datetime.now()
                    api.save()
                    update_API_products.delay(getattr(api,'shopifyconnection'))

        in_progress = APIConnection.objects.filter(retailer=request.user,update_in_progress=True)


        ctx = {'retailer_profile': retailer_profile, 'product_list': pl,'bulk_upload_form':form,'updates_in_progress':in_progress, 'upload':upload}
    except:
        raise
        return redirect(reverse("home"))
    return direct_to_template(request, template, ctx)

@login_required
def retailer_information(request, name=None, template="retailers/retailer_information.html"):
    retailer_profile = get_retailer_profile(request)
    shipping_types = ShippingType.objects.all()
    form = RetailerEditForm(instance=retailer_profile)
    ctx = {'retailer_profile': retailer_profile, 'shipping_types': shipping_types, 'form': form}

    return direct_to_template(request, template, ctx)

@json_view
@login_required
def retailer_logo_upload(request):
    try:
        retailer_profile = get_retailer_profile(request)
        if request.method == "POST":
            form = LogoUploadForm(request.POST, request.FILES, instance=retailer_profile)
            form.save()
            return {'result': 'ok', 'source': retailer_profile.logo_image.url}
        else:
            raise ValidationError("Errors Occur!")
    except:
        pass
    
def retailer_list(request, template='retailers/retailer_list.html'):
    retailer_list = RetailerProfile.objects.all()
    return direct_to_template(request, template, {'retailer_list': retailer_list})

def retailer_modal(request, item_id, template="retailers/retailer_information_modal.html"):
    current_item = get_object_or_404(Item, pk=item_id)

    retailer_profile = current_item._retailer
    return direct_to_template(request, template, {'retailer_profile': retailer_profile})    

@login_required
def order_history(request, template='orders/order_history.html'):
    ctx = {'purchase_actions': 'orders/retailer_purchase_actions.html'}
    try:
        retailer_profile = get_retailer_profile(request)
        shipping_types = ShippingType.objects.all()
        form = RetailerEditForm(instance=retailer_profile)
        ctx.update({'retailer_profile': retailer_profile, 'shipping_types': shipping_types, 'form': form})
    
        _from = request.GET.get('from')
        _to = request.GET.get('to')

        checkouts = request.user.retailer_checkout_set.all()
        
        if not _from and not _to:
            checkouts = checkouts.filter(complete=False)
        else:
            if _from:
                checkouts = checkouts.filter(last_modified__gte=_from)
            if _to:
                checkouts = checkouts.filter(last_modified__lte=_to)
                             
        ctx['checkouts']= checkouts.order_by('-last_modified')
    except:
        raise
        #login as regular user
        return redirect(reverse("home"))
    return direct_to_template(request, template, ctx)

@login_required
def view_all_products(request, retailer_id):
    retailer = get_object_or_404(RetailerProfile, pk=retailer_id)
    try:
        user_racks = Rack.objects.filter(user=request.user, name=retailer.name)
        if user_racks.count() > 0:
            pass
        else:
            new_rack = Rack.objects.create(name=retailer.name, user=request.user, publicity=0)
            retailer_items = StylistItem.objects.filter(stylist=retailer.user)
            for retailer_item in retailer_items:
                Rack_Item.objects.create(item=retailer_item.item, rack=new_rack, user=request.user)
    except:
        raise
    
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
        
        
@login_required 
def item_action(request, template="retailers/product_list.html"):
    if request.method=='POST':
        try:
            retailer_profile = get_retailer_profile(request)
            pl = []
            s = set()
            for si in StylistItem.objects.filter(stylist=request.user):
                if si.item.pk not in s and si.item.pk in [int(pk) for pk in request.POST.getlist('selected_items')]:
                    pl.append(si.item)
                    s.add(si.item.pk)
            if request.POST.get('action_name','None') and request.POST.get('confirm_%s'%request.POST.get('action_name')):
                for i in pl:
                    getattr(i,request.POST.get('action_name','None'))()
                return redirect(request.get('next',reverse("product_list")))
            else:   
                data = {
                    'action_name': request.POST.get('action_name')
                }
                ctx = {'retailer_profile': retailer_profile, 'product_list': pl, 'confirm': data,'action':True}
                return direct_to_template(request, template, ctx)

        except:    
            return redirect(reverse("product_list"))

@login_required
def create_shipping_label(request, ref=None, template='retailers/retailer_shipping_label.html'):
    ctx = {}
    try:
        checkout = Checkout.objects.get(ref=ref)

        if request.user == checkout.purchaser:
            sender = ShippingInfo.objects.get(customer=request.user.get_profile(),is_default=True)
            receiver = RetailerProfile.objects.get(user=checkout.retailer)
            purchase_status = 'return requested'
            redirect_url = "order_history"
        elif request.user == checkout.retailer:
            sender = RetailerProfile.objects.get(user=checkout.retailer)
            receiver = ShippingInfo.objects.get(customer=checkout.purchaser.get_profile(),is_default=True)
            purchase_status = 'placed'
            redirect_url = "retailer_order_history"
        else:
            raise

        purchases = checkout.purchase_set.all()
        ctx['checkout'] = checkout
    except:
        raise
        return redirect(reverse("home"))

    if request.method == "POST":
        purchase_list = request.POST.getlist('ship_purchase')
        if len(purchase_list)<1:
            ctx['error_message'] = "Select at least one item to ship."
            print 'error'
        else:
            item_count = len(purchase_list)
            tracking_number,label = ship_it(sender,receiver,item_count,purchases[0].shipping_method.vendor_tag)

            if os.path.exists(label):
                f = File(open(label,'rb'))
                shipment = Shipment.objects.create()
                shipment.originator = request.user
                shipment.label.save(tracking_number+'.png', f)
                shipment.tracking_number = tracking_number
                

                for purchase_id in purchase_list:
                    purchase = purchases.filter(id=purchase_id)[0]
                    purchase.status = purchase_status
                    purchase.save()

                    shipment.purchases.add(purchase)
                    print 'adding purchase to shipment',purchase,shipment

                shipment.save()

                return redirect(reverse(redirect_url))

            ctx['shipment'] = shipment
    try:
        ctx['purchases']= purchases
    except:
        raise
        #login as regular user
        return redirect(reverse("home"))
    return direct_to_template(request, template, ctx)

@login_required
def print_packing_slip(request, shipping_number=None, template='retailers/print_packing_slip.html'):
    ctx={}
    try:
        # retailer_profile = RetailerProfile.objects.get(user=request.user)
        shipment = Shipment.objects.get(tracking_number = shipping_number)
        # items = [p.item for p in shipment.purchases.all()]
        purchases = shipment.purchases.all()
        # ctx.update({'retailer_profile': retailer_profile})
        try:
            ctx['packing_slip_text'] = SiteTextContent.objects.get(item_name='packing_slip_retailer')
        except:
            ctx['packing_slip_text'] = SiteTextContent.objects.get(item_name='packing_slip_customer')


        ctx['shipping_label'] = shipment
        ctx['purchases']= purchases
    except:
        raise
        #login as regular user
        return redirect(reverse("home"))
    return direct_to_template(request, template, ctx)

def view_shipping_label(request, shipping_number=None,template='retailers/retailer_shipping_label.html'):
    ctx={}
    try:
        shipment = Shipment.objects.get(tracking_number = shipping_number)
        # items = [p.item for p in shipment.purchases.all()]
        purchases = shipment.purchases.all()
        # ctx.update({'retailer_profile': retailer_profile})

        try:
            ctx['advice_text'] = SiteTextContent.objects.get(item_name='shipping_label_instructions')
        except:
            ctx['advice_text'] = SiteTextContent.objects.get(item_name='return_label_instructions')

        ctx['shipping_label'] = shipment
        ctx['purchases']= purchases
    except:
        raise
        #login as regular user
        return redirect(reverse("home"))
    return direct_to_template(request, template, ctx)



