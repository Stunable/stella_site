"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import pprint

PP = pprint.PrettyPrinter(indent=4)

from base import *

class Store(PortableResource):
    pass

    @classmethod
    def current(cls):
        return cls.find_one("" + cls.format.extension)

class item(PortableResource):
    pass

class variation(PortableResource):

    _prefix_source = "/items/$item_id/"

    @classmethod
    def _prefix(cls, options={}):
        item_id = options.get("item_id")
        return  "/items/%s" % (item_id)


def test_portable():
	PortableResource.activate_session()

	items = item.find()
	for i in items:
		PP.pprint(i.to_dict())

	items[0].attributes['variation'][0].attributes['stock'] == 99
	# items[0].attributes['variation'][0].save()
	items[0].save()



if __name__ == "__main__":
	test_portable()