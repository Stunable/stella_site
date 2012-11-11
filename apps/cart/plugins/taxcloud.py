import suds

from django.conf import settings



class TaxCloudClient(object):
    """Client for TaxCloud's SOAP API"""
    url = "https://api.taxcloud.net/1.0/?wsdl"
    client = suds.client.Client(url)

    def get_tax_rate_for_item(self, source_address, destination_address, item_list):
        self.index = 0
        cartItem_list = self.prep_cartItems(item_list)

        origin = self.convert_verified_address(self.verify_address(source_address))
        dest  = self.verify_address(destination_address)

        l = self.client.factory.create('Lookup')
        l.apiLoginID = settings.TAX_TAXCLOUD_API_ID
        l.apiKey = settings.TAX_TAXCLOUD_API_KEY
        l.customerID = "1"
        l.cartID = "1123"
        l.cartItems = cartItem_list
        l.origin = origin   
        l.destination = dest
        l.deliveredBySeller = False

        return self.client.service.Lookup(l).CartItemsResponse.CartItemResponse[0].TaxAmount


    def verify_address(self,address_object):
        a = self.client.factory.create('VerifyAddress')
        a.uspsUserID = settings.USPS_ID
        a.address1 = address_object.address1
        a.address2 = address_object.address2
        a.city = address_object.city
        a.state = address_object.state
        a.zip5 = address_object.zip_code
        return self.client.service.VerifyAddress(a)


    def prep_cartItems(self,item_list):
        CIs = self.client.factory.create("ArrayOfCartItem")
        for item in item_list:
            i = self.client.factory.create("CartItem")
            i.Index = self.index
            i.ItemID = item.object_id
            i.TIC = 20010
            i.Price = item.unit_price
            i.Qty = item.quantity

            CIs.CartItem.append(i)
            self.index += 1

        return CIs

    def convert_verified_address(self,verified_address):
        v = verified_address
        a = self.client.factory.create('Address')
        a.Address1 = v.Address1
        if hasattr(v,'Address2'):
            a.Address2 = v.Address2
        a.City = v.City
        a.State = v.State
        a.Zip5 = v.Zip5
        a.Zip4 = v.Zip4

        return a




        


