from django.forms import Textarea
from django import forms
from django.utils import simplejson as json
from django.conf import settings
from django.template import loader, Context
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils import six, translation
from django.core.exceptions import ImproperlyConfigured
from multilingualfield import settings as ml_settings

from .language import LanguageText

DEFAULT_CKCONFIG = {

}

class MLTextWidget(Textarea):
    HTML = False
    
    def __init__(self, HTML=False, *args, **kwargs):
        self.HTML = HTML
        
        super(MLTextWidget, self).__init__(*args, **kwargs)
      
    @property
    def media(self):
        js = ['multiligualfield/js/jquery-1.10.2.min.js','multiligualfield/js/jquery-ui-1.10.3.custom.min.js',
        'multiligualfield/js/json.js']
        if self.HTML:
            js += ['multiligualfield/ckeditor/ckeditor.js']
        css = ['multiligualfield/css/ui-darkness/jquery-ui-1.10.3.custom.min.css']
        return forms.Media(js=js,css={'all':css})
        
    def render(self, name, value, attrs=None):
        is_valid = False
        if value is None or value == '': #New create or edit none
            ml_json = '{}'
            ml_language = '[]'
            is_valid = True
        if isinstance(value, LanguageText):
            ml_json = json.dumps(value.values)
            ml_language = json.dumps(value.get_available_language())
            is_valid = True
        if isinstance(value, six.string_types): #Debug :(
            print "Why string here ==================="
            print value
            print "===============================Why?"
        if is_valid :
            Langs = json.dumps(dict(settings.LANGUAGES))
            if self.HTML:
                widgettmpl = "multilingualfield/MLHTMLWidget.html"
            else:
                widgettmpl = "multilingualfield/MLTextWidget.html"
            return mark_safe(render_to_string(widgettmpl,{
                "name":name,
                "raw":value,
                "ml_json":ml_json,
                "ml_language":ml_language,
                "langs":Langs,
                "langsobj":settings.LANGUAGES,
                'current_language': translation.get_language(),
                'CKEDITOR_FILER' : ml_settings.CKEDITOR_FILER,
                'CKEDITOR_BROWSER_URL': ml_settings.CKEDITOR_BROWSER_URL
            }))
        return "Invalid data '%s'" % value