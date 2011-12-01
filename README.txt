### shopwithstella.com
## README.txt
## PROJECT_ROOT

The project root, stella_project, contains those files that remain immutable while the site
is running. This includes code, static media, and config files. This directory IS checked
into source control. Technically, it is a Django project directory. 

The diagram below describes the directory structure. The only difference currently is
the lack of a settings directory, which will come into play later as the Django
project begins to deploy. Right now it is an unnecessary complication. 

IMPORTANT: Always update the REQUIREMENTS.txt file with new PIP dependencies that you
have added to your working branch. 


PROJECT_ROOT/
|-- apps/         # Site-specific Django apps
|-- etc/          # A symlink to an `etcs/` sub-directory
|-- etcs/         # Assorted plain-text configuration files
|-- libs/         # Site-specific Python libs
|-- media/        # Static site media (images, stylesheets, JavaScript)
|-- settings/     # Settings directory
|-- templates/    # Site-wide Django templates
|-- services/     # Site-specific service programs and scripts
|-- .gitignore    # Git ignore file
|-- README        # Instructions/assistance for other developers/admins (This file)
|-- REQUIREMENTS  # pip dependencies file
|-- __init__.py   # Makes the project root a Python package
`-- urls.py       # Root URLconf

