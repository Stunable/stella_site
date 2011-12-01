### Shopwithstella.com
## Settings README.txt
# 

This is the intended structure of the settings directory once we move to staging and
production. common.py lists all the settings that remain unchanged across various deployments. 
The other three files, development.py, production.py, and staging.py, list those settings that are
specific to development, production, and staging respectively. They all import common.py and redefine
and/or introduce the specific settings they need. 

settings/
|-- __init__.py     # Empty; makes this a Python package
|-- common.py       # All the common settings are defined here
|-- development.py  # Settings for development
|-- production.py   # Settings for production
`-- staging.py      # Settings for staging

Further customizations are possible for working on your local machine. For instance,
Mish uses mish_dev.py to customize the location of his local media root and 
database files. 

The DJANGO_SETTINGS_MODULE environment variable needs to be set manually in this
case, and there will be no manage.py file in the project root. To set it, perform
the following: 

$ export DJANGO_SETTINGS_MODULE=settings.development #If you were working on dev (which you should always be)
$ echo "!!" >> ../bin/activate

The last line saves the operation to your virtualenv activate script. 

NOTE: Make sure your PYTHONPATH environment variable includes the project_root,
"stella_project". To add this to your virtual environment, add the following line
in the bin/activate script before the DJANGO_SETTINGS_MODULE is set.

export PYTHONPATH=$PYTHONPATH:/path/to/stella_root/stella_project

