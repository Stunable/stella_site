### shopwithstella.com
## README.txt
## PROJECT_ROOT

The project root, stella_site, contains those files that remain immutable while the site
is running. This includes code, static media, and config files. This directory IS checked
into source control. Technically, it is a Django project directory. 

IMPORTANT: Always update the REQUIREMENTS.txt file with new PIP dependencies that you
have added to your working branch. 

Below is the directory structure and details for a generic project deployment. ShopwithStella doesn't
currently have all these directories, but when the need for them arises, you'll know where to put them.

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

------------------------------------------------

The STELLA_ROOT directory is a container for individual deployments. You should
have your own on your development machine that is configured to work with the 
project. It is an extension of the existing virtual environment directory. All
files contained within are those that will vary from deployment to deployment,
and as such, this directory is not checked into version control. 

To create this directory container, create a new virtual environment for this
project named STELLA_ROOT. Then, install the necessary libraries from the 
project-included REQUIREMENTS file in the PROJECT_ROOT. You will have to edit your
virtualenv activate script to support the custom settings configuration; more details
in the settings README.

Below is the directory structure and details for a generic deployment: 

STELLA_ROOT/
|-- PROJECT_ROOT   # Django project directory (see above)
|-- bin/      	   # Part of the virtualenv
|-- cache/    	   # A filesystem-based cache
|-- db/       	   # Store SQLite files in here (during development)
|-- include/  	   # Part of the virtualenv
|-- lib/      	   # Part of the virtualenv
|-- log/      	   # Log files
|-- pid/      	   # PID files
|-- share/    	   # Part of the virtualenv
|-- sock/     	   # UNIX socket files
|-- tmp/      	   # Temporary files
`-- uploads/  	   # Site uploads

