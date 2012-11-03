#!/usr/bin/env python
"""
This example shows how to validate addresses. Note that the validation
class can handle up to 100 addresses for validation.
"""
import logging
from django.conf import settings

#CONFIG_OBJ = settings.FEDEX_CONFIG

from st_fedex.services.address_validation_service import FedexAddressValidationRequest

from st_fedex.config import FedexConfig


CONFIG_OBJ = FedexConfig(key='G9zxZissGIQkOgo4',
                         password='bX3GkoY0uIQjrIl1m66jT2OTa',
                         account_number='510087968',
                         meter_number='118562345',
                         use_test_server=True)

def validate_this(address):
    # Set this to the INFO level to see the response from Fedex printed in stdout.
    logging.basicConfig(level=logging.INFO)

    # This is the object that will be handling our tracking request.
    # We're using the FedexConfig object from example_config.py in this dir.
    connection = FedexAddressValidationRequest(CONFIG_OBJ)

    # The AddressValidationOptions are created with default values of None, which
    # will cause WSDL validation errors. To make things work, each option needs to
    # be explicitly set or deleted.

    ## Set the flags we want to True (or a value).
    connection.AddressValidationOptions.CheckResidentialStatus = False
    connection.AddressValidationOptions.VerifyAddresses = True
    connection.AddressValidationOptions.RecognizeAlternateCityNames = True
    connection.AddressValidationOptions.MaximumNumberOfMatches = 3

    ## Delete the flags we don't want.
    del connection.AddressValidationOptions.ConvertToUpperCase
    del connection.AddressValidationOptions.ReturnParsedElements

    ## *Accuracy fields can be TIGHT, EXACT, MEDIUM, or LOOSE. Or deleted.
    connection.AddressValidationOptions.StreetAccuracy = 'LOOSE'
    del connection.AddressValidationOptions.DirectionalAccuracy
    del connection.AddressValidationOptions.CompanyNameAccuracy

    ## Create some addresses to validate
    address1 = connection.create_wsdl_object_of_type('AddressToValidate')
    address1.CompanyName = address.company_name
    address1.Address.StreetLines = [address.line1, address.line2]
    address1.Address.City = address.city
    address1.Address.StateOrProvinceCode = address.state
    address1.Address.PostalCode = address.zip_code
    address1.Address.CountryCode = address.country
    address1.Address.Residential = False
    connection.add_address(address1)

    # address2 = connection.create_wsdl_object_of_type('AddressToValidate')
    # address2.Address.StreetLines = ['320 S Cedros', '#200']
    # address2.Address.City = 'Solana Beach'
    # address2.Address.StateOrProvinceCode = 'CA'
    # address2.Address.PostalCode = 92075
    # address2.Address.CountryCode = 'US'
    # connection.add_address(address2)

    ## Send the request and print the response
    connection.send_request()
    print connection.response