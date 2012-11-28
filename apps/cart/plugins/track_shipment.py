#!/usr/bin/env python
"""
This example shows how to track shipments.
"""
import logging
from django.conf import settings
from fedex.services.track_service import FedexTrackRequest

CONFIG_OBJ = settings.FEDEX_CONFIG


# Set this to the INFO level to see the response from Fedex printed in stdout.
logging.basicConfig(level=logging.DEBUG)



def track_it(package_identifier,package_type='TRACKING_NUMBER_OR_DOORTAG'):
    # NOTE: TRACKING IS VERY ERRATIC ON THE TEST SERVERS. YOU MAY NEED TO USE
    # PRODUCTION KEYS/PASSWORDS/ACCOUNT #.
    # We're using the FedexConfig object from example_config.py in this dir.
    track = FedexTrackRequest(CONFIG_OBJ)
    track.TrackPackageIdentifier.Type = package_type
    track.TrackPackageIdentifier.Value = package_identifier

    # Fires off the request, sets the 'response' attribute on the object.
    track.send_request()

    # See the response printed out.
    print track.response

    # Look through the matches (there should only be one for a tracking number
    # query), and show a few details about each shipment.
    print "== Results =="
    for match in track.response.TrackDetails:
        print match
        print "Tracking #:", match.TrackingNumber
        print "Status:", match.StatusDescription