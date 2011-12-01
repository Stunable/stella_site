""" URLConf for beta invite.
"""

from django.conf.urls.defaults import *

from beta_invite.views import signup


urlpatterns = patterns('',
                       url(r'^signup/', signup),
                       )
