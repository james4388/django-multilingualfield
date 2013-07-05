from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models, DatabaseError, transaction
from django.utils.translation import ugettext_lazy as _, get_language
from django.utils import six

try:
    import json
except ImportError:
    from django.utils import simplejson as json
    
from .language import LanguageText
from .forms import MLTextFormField
from .widgets import MLTextWidget

def get_base_language(lang):
    if '-' in lang:
        return lang.split('-')[0]
    return lang
    
def get_current_language(base=True):
    l = get_language()
    if base:
        return get_base_language(l)
    return l
    
class MLTextField(six.with_metaclass(models.SubfieldBase, models.Field)):
    """
    A field that support multilingual text for your model
    """
    __metaclass__ = models.SubfieldBase
    
    default_error_messages = {
        'invalid': _("'%s' is not a valid JSON string.")
    }
    
    description = "Multilingual Text Field"
    
    def __init__(self, *args, **kwargs):
        self.lt_max_length = kwargs.pop('max_length',-1)
        self.default_language = kwargs.get('default_language', get_current_language())
        super(MLTextField, self).__init__(*args, **kwargs)        
    
    def get_prep_value(self, value):
        if value is None:
            if not self.null and self.blank:
                return ""
            return None
        if isinstance(value, six.string_types):
            value = LanguageText(value,language=None,max_length=self.lt_max_length,default_language=self.default_language)
        if isinstance(value, LanguageText):
            value.max_length = self.lt_max_length
            value.default_language = self.default_language
            return json.dumps(value.values)
        return None
        
    def get_db_prep_value(self, value, connection=None, prepared=None):
        return self.get_prep_value(value)
        
    def validate(self, value, model_instance):
        if not self.null and value is None:
            raise ValidationError(self.error_messages['null'])
        try:
            self.get_prep_value(value)
        except:
            raise ValidationError(self.error_messages['invalid'] % value)
    
    def get_internal_type(self):
        return 'TextField'
    
    def db_type(self, connection):
        return 'text'
        
    def to_python(self, value):
        if isinstance(value, six.string_types):
            if value == "" or value is None:
                if self.null:
                    return None
                if self.blank:
                    return LanguageText("",language=None,max_length=self.lt_max_length,default_language=self.default_language)   #a A blank LanguageText object
            try:
                valuejson = json.loads(value)
                Lang = LanguageText(max_length=self.lt_max_length,default_language=self.default_language)
                Lang.values = valuejson
                return Lang
            except ValueError:
                try:
                    Lang = LanguageText(value,language=None,max_length=self.lt_max_length,default_language=self.default_language)
                    return Lang
                except:
                    msg = self.error_messages['invalid'] % value
                    raise ValidationError(msg)
        if isinstance(value, LanguageText):
            return value
        return None

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in ["exact", "iexact"]:
            return self.to_python(self.get_prep_value(value))
        if lookup_type == "in":
            return [self.to_python(self.get_prep_value(v)) for v in value]
        if lookup_type == "isnull":
            return value
        if lookup_type in ["contains", "icontains"]:
            if isinstance(value, (list, tuple)):
                raise TypeError("Lookup type %r not supported with argument of %s" % (
                    lookup_type, type(value).__name__
                ))
                # Need a way co combine the values with '%', but don't escape that.
                return self.get_prep_value(value)[1:-1].replace(', ', r'%')
            if isinstance(value, dict):
                return self.get_prep_value(value)[1:-1]
            return self.to_python(self.get_prep_value(value))
        raise TypeError('Lookup type %r not supported' % lookup_type)
    
    def formfield(self, **kwargs):
        defaults = {
            'form_class': MLTextFormField,
            'widget': MLTextWidget
        }
        defaults.update(**kwargs)
        return super(MLTextField, self).formfield(**defaults)
        
    def value_to_string(self, obj):
        return self._get_val_from_obj(obj)
        
class MLHTMLField(MLTextField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': MLTextFormField,
            'widget': MLHTMLWidget(HTML=True)
        }
        defaults.update(**kwargs)
        return super(MLHTMLField, self).formfield(**defaults)
        
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^multilingualfield\.fields\.MLTextField'])
    add_introspection_rules([], ['^multilingualfield\.fields\.MLHTMLField'])
except ImportError:
    pass