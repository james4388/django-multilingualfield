#-*- coding: utf-8 -*-
from django.conf import settings


CKEDITOR_FILERBROWSER = getattr(settings, 'CKEDITOR_FILERBROWSER', False)
CKEDITOR_BROWSER_URL = '/mlfield/ckfiler/?type=Images'
CKEDITOR_FILER_FILEBROWSER_URL = '/admin/filer/folder/?_popup=1'
CKEDITOR_FILER_FILEBROWSER_GET = '/admin/filer/file/{0}/?_popup=1'

FILER_INSTALLED = False
if 'filer' in settings.INSTALLED_APPS:
    FILER_INSTALLED = True
    
CKEDITOR_FILER = False    
if CKEDITOR_FILERBROWSER and FILER_INSTALLED:
    CKEDITOR_FILER = True
    