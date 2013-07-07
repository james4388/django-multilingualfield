from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from multilingualfield import settings as ml_settings

import json

def admin_required(orig_view_fn):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_staff:
            return orig_view_fn(request, *args, **kwargs)
        return redirect('/')
    return wrapped_view
    
@admin_required
def ckfiler(request):
    CKEditorFuncNum  = request.GET.get('CKEditorFuncNum')
    CKEditor = request.GET.get('CKEditor')
    langCode = request.GET.get('langCode','en')
    filetype = request.GET.get('type')
    CKEDITOR_FILER_FILEBROWSER_URL = ml_settings.CKEDITOR_FILER_FILEBROWSER_URL
    CKEDITOR_FILER_FILEBROWSER_GET = ml_settings.CKEDITOR_FILER_FILEBROWSER_GET
    CKEDITOR_BROWSER_URL = ml_settings.CKEDITOR_BROWSER_URL
    CKEDITOR_FILER = ml_settings.CKEDITOR_FILER
    return render(request, 'multilingualfield/browser.html', {
        "CKEditorFuncNum": CKEditorFuncNum,
        "CKEditor": CKEditor,
        "langCode": langCode,
        "filetype": filetype,
        "CKEDITOR_FILER_FILEBROWSER_URL":CKEDITOR_FILER_FILEBROWSER_URL,
        "CKEDITOR_FILER_FILEBROWSER_GET":CKEDITOR_FILER_FILEBROWSER_GET,
        "CKEDITOR_BROWSER_URL":CKEDITOR_BROWSER_URL,
        "CKEDITOR_FILER":CKEDITOR_FILER
    })