import httplib2
http = httplib2.Http()

url = 'http://localhost:8000/api/product/7083/'

import urllib
params = urllib.urlencode({
    'name': "cool",
    'brand': "blah",
    'price': "123.00"
})

http.add_credentials('bombom@test.com', 'test123')

"""
    Update existing product
"""


response, content = http.request(url, 'PUT', params,
    headers={'Content-type': 'application/x-www-form-urlencoded'}
)


"""
    Create new product
"""

response, content = http.request('http://localhost:8000/api/product/', 'POST', params,
    headers={'Content-type': 'application/x-www-form-urlencoded'}
)

"""
    Update inventory
"""


params = urllib.urlencode({
    'inventory': 234,
    'color_id': 7,
    'size_id': 38,
    'price': "5",
    'item_id': 7085
})


response, content = http.request('http://localhost:8000/api/inventory/66/', 'PUT', params,
    headers={'Content-type': 'application/x-www-form-urlencoded'}
)


"""
    Create inventory
"""

params = urllib.urlencode({
    'inventory': 111,
    'color_id': 7,
    'size_id': 38,
    'price': "5",
    'item_id': 7085
})


response, content = http.request('http://localhost:8000/api/inventory/', 'POST', params,
    headers={'Content-type': 'application/x-www-form-urlencoded'}
)

"""
    Delete inventory
"""

params = urllib.urlencode({
    'inventory': 111,
    'color_id': 7,
    'size_id': 38,
    'price': "5",
    'item_id': 7085
})

response, content = http.request('http://localhost:8000/api/inventory/69/', 'DELETE', params,
    headers={'Content-type': 'application/x-www-form-urlencoded'}
)

print response, content