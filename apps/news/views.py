import datetime
import re
import os

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import Http404
    
from django.db.models import Q
from django.conf import settings

from apps.news.models import *
from apps.cms.models import *

from apps.news.constants import STOP_WORDS_RE
from tagging.models import Tag, TaggedItem

def post_list(request, page=0, paginate_by=20, **kwargs):
    return redirect('/')