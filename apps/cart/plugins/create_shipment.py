#!/usr/bin/env python
"""
This example shows how to create shipments. The variables populated below
represents the minimum required values. You will need to fill all of these, or
risk seeing a SchemaValidationError exception thrown.

Near the bottom of the module, you'll see some different ways to handle the
label data that is returned with the reply.
"""
import logging
import binascii
from django.conf import settings
import time
from st_fedex.services.ship_service import FedexProcessShipmentRequest

from st_fedex.config import FedexConfig

if settings.DEBUG:
    CONFIG_OBJ = FedexConfig(key='zA9Z6uz3gHNKkU3L',
                         password='8TA1Z49ZTJztPJ8a6uPqsjqKF',
                         account_number='147593830',
                         meter_number='104573181',
                         use_test_server=False)

else:
    CONFIG_OBJ = FedexConfig(key='zA9Z6uz3gHNKkU3L',
                             password='8TA1Z49ZTJztPJ8a6uPqsjqKF',
                             account_number='147593830',
                             meter_number='104573181',
                             use_test_server=False)

def ship_it(retailer,customer,item_count,shipping_method):
    # Set this to the INFO level to see the response from Fedex printed in stdout.
    logging.basicConfig(level=logging.INFO)


    # This is the object that will be handling our tracking request.
    # We're using the FedexConfig object from example_config.py in this dir.
    shipment = FedexProcessShipmentRequest(CONFIG_OBJ)

    # This is very generalized, top-level information.
    # REGULAR_PICKUP, REQUEST_COURIER, DROP_BOX, BUSINESS_SERVICE_CENTER or STATION
    shipment.RequestedShipment.DropoffType = 'REGULAR_PICKUP'

    # See page 355 in WS_ShipService.pdf for a full list. Here are the common ones:
    # STANDARD_OVERNIGHT, PRIORITY_OVERNIGHT, FEDEX_GROUND, FEDEX_EXPRESS_SAVER
    shipment.RequestedShipment.ServiceType = shipping_method

    # What kind of package this will be shipped in.
    # FEDEX_BOX, FEDEX_PAK, FEDEX_TUBE, YOUR_PACKAGING
    shipment.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

    # No idea what this is.
    # INDIVIDUAL_PACKAGES, PACKAGE_GROUPS, PACKAGE_SUMMARY 
    #shipment.RequestedShipment.PackageDetail = 'INDIVIDUAL_PACKAGES'
    # Shipper contact info.
    shipment.RequestedShipment.Shipper.Contact.PersonName = '%s %s'%(retailer.user.first_name,retailer.user.last_name)
    shipment.RequestedShipment.Shipper.Contact.CompanyName = retailer.name
    shipment.RequestedShipment.Shipper.Contact.PhoneNumber = retailer.phone_number

    # Shipper address.
    origin_address = retailer.address1
    if retailer.address2:
        origin_address = retailer.address1 + ', ' + retailer.address2
    shipment.RequestedShipment.Shipper.Address.StreetLines = origin_address
    shipment.RequestedShipment.Shipper.Address.City = retailer.city
    shipment.RequestedShipment.Shipper.Address.StateOrProvinceCode = retailer.state
    shipment.RequestedShipment.Shipper.Address.PostalCode = retailer.zip_code
    shipment.RequestedShipment.Shipper.Address.CountryCode = 'US'
    shipment.RequestedShipment.Shipper.Address.Residential = True

    # Recipient contact info.
    shipment.RequestedShipment.Recipient.Contact.PersonName = '%s %s'%(customer.firstname,customer.lastname)
    shipment.RequestedShipment.Recipient.Contact.CompanyName = {True:customer.company_name,False:"%s %s"%(customer.firstname,customer.lastname)}[customer.company_name != '']
    shipment.RequestedShipment.Recipient.Contact.PhoneNumber = customer.phone

    # Recipient address
    dest_address = customer.address1
    if customer.address2:
        dest_address = customer.address1 + ', ' + customer.address2
    shipment.RequestedShipment.Recipient.Address.StreetLines = dest_address
    shipment.RequestedShipment.Recipient.Address.City = customer.city
    shipment.RequestedShipment.Recipient.Address.StateOrProvinceCode = customer.state
    shipment.RequestedShipment.Recipient.Address.PostalCode = customer.zip_code
    shipment.RequestedShipment.Recipient.Address.CountryCode = 'US'
    # This is needed to ensure an accurate rate quote with the response.
    shipment.RequestedShipment.Recipient.Address.Residential = {False:False,True:True}[shipping_method=='FEDEX_2_DAY']

    # Who pays for the shipment?
    # RECIPIENT, SENDER or THIRD_PARTY
    shipment.RequestedShipment.ShippingChargesPayment.PaymentType = 'THIRD_PARTY' 

    # Specifies the label type to be returned.
    # LABEL_DATA_ONLY or COMMON2D
    shipment.RequestedShipment.LabelSpecification.LabelFormatType = 'COMMON2D'

    # Specifies which format the label file will be sent to you in.
    # DPL, EPL2, PDF, PNG, ZPLII
    shipment.RequestedShipment.LabelSpecification.ImageType = 'PNG'

    # To use doctab stocks, you must change ImageType above to one of the
    # label printer formats (ZPLII, EPL2, DPL).
    # See documentation for paper types, there quite a few.
    shipment.RequestedShipment.LabelSpecification.LabelStockType = 'PAPER_4X6'

    # This indicates if the top or bottom of the label comes out of the 
    # printer first.
    # BOTTOM_EDGE_OF_TEXT_FIRST or TOP_EDGE_OF_TEXT_FIRST
    shipment.RequestedShipment.LabelSpecification.LabelPrintingOrientation = 'BOTTOM_EDGE_OF_TEXT_FIRST'

    package1_weight = shipment.create_wsdl_object_of_type('Weight')
    # Weight, in pounds.
    package1_weight.Value = 1.0 * float(item_count)
    package1_weight.Units = "LB"

    package1 = shipment.create_wsdl_object_of_type('RequestedPackageLineItem')
    package1.Weight = package1_weight
    
    # Un-comment this to see the other variables you may set on a package.
    #print package1
    del shipment.RequestedShipment.ErrorLabelBehavior
    del shipment.RequestedShipment.EdtRequestType
    del package1.PhysicalPackaging
    # This adds the RequestedPackageLineItem WSDL object to the shipment. It
    # increments the package count and total weight of the shipment for you.
    shipment.add_package(package1)

    # If you'd like to see some documentation on the ship service WSDL, un-comment
    # this line. (Spammy).
    #print shipment.client

    # Un-comment this to see your complete, ready-to-send request as it stands
    # before it is actually sent. This is useful for seeing what values you can
    # change.
    #print shipment.RequestedShipment

    # If you want to make sure that all of your entered details are valid, you
    # can call this and parse it just like you would via send_request(). If
    # shipment.response.HighestSeverity == "SUCCESS", your shipment is valid.
    #shipment.send_validation_request()
    #print shipment
    # Fires off the request, sets the 'response' attribute on the object.
    #shipment.send_validation_request()


    shipment.send_request()

    # This will show the reply to your shipment being sent. You can access the
    # attributes through the response attribute on the request object. This is
    # good to un-comment to see the variables returned by the Fedex reply.
    print shipment.response

    # Here is the overall end result of the query.
    # print "HighestSeverity:", shipment.response.HighestSeverity
    # # Getting the tracking number from the new shipment.
    tracking_number = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].TrackingIds[0].TrackingNumber
    # # Net shipping costs.
    # print "Net Shipping Cost (US$):", shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].PackageRating.PackageRateDetails[0].NetCharge.Amount

    # # Get the label image in ASCII format from the reply. Note the list indices
    # we're using. You'll need to adjust or iterate through these if your shipment
    # has multiple packages.
    ascii_label_data = shipment.response.CompletedShipmentDetail.CompletedPackageDetails[0].Label.Parts[0].Image
    # Convert the ASCII data to binary.
    label_binary_data = binascii.a2b_base64(ascii_label_data)

    """
    This is an example of how to dump a label to a PNG file.
    """
    # This will be the file we write the label out to.
    file_out = 'media/label_temp/%d_.png'%int(round(time.time() * 1000))
    png_file = open(file_out, 'wb')
    png_file.write(label_binary_data)
    png_file.close()

    return tracking_number,file_out
