from django.forms import Textarea
from django.utils import simplejson as json
from django.conf import settings
from django.template import loader, Context
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils import six


from .language import LanguageText

class MLTextWidget(Textarea):

    def __init__(self, HTML=False, *args, **kwargs):
        super(MLTextWidget, self).__init__(*args, **kwargs)
        self.HTML = HTML
        
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
        if isinstance(value, six.string_types):
            print "Why string here ==================="
            print value
            print "========================="
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
                "langsobj":settings.LANGUAGES
            }))
        return "Invalid data '%s'" % value