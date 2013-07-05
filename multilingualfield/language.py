from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models, DatabaseError, transaction
from django.utils.translation import ugettext_lazy as _, get_language

try:
    import json
except ImportError:
    from django.utils import simplejson as json

def get_base_language(lang):
    if '-' in lang:
        return lang.split('-')[0]
    return lang
    
def get_current_language(base=True):
    l = get_language()
    if base:
        return get_base_language(l)
    return l
    

class LanguageText(object):
    '''
        Store text with language code in JSON format
    '''
    values = {}
    default_language = None
    max_length = -1
    
    def __init__(self, value=None, language=None, default_language=None, max_length=-1):
        self.max_length = max_length
        self.default_language = default_language
        self.values = {}
        if value is not None:
            self.value(value,language)
            
    def __call__(self, value=None, language=None):
        self.value(value,language)
        return self
            
    def get_available_language(self):
        return self.values.keys()
    
    def get_current_language(self, base=False):
        return get_current_language(base)
    
    def remove_language(self, lang):
        try:
            return self.values.pop(lang)
        except:
            pass
    
    def has_language(self, lang):
        return self.values.has_key(lang)
            
    def get(self, language=None, fallback=True):
        if language is None:
            curr_lang = get_current_language(False)
        else:
            curr_lang = language
        curr_lang_base = get_current_language(True)
        if curr_lang in self.values:
            return self.values[curr_lang]
        if not fallback:
            return None
        if curr_lang_base in self.values:
            return self.values[curr_lang_base]
        if self.default_language in self.values:
            return self.values[self.default_language]
        try:
            first_lang = self.values.keys()[0]
            return self.values[first_lang]
        except:
            pass
        return None
    
    def value(self, value=None, language=None):
        if value is None:   #Get value
            return self.get(language)
        else: #Set value
            if language is None:
                language = get_current_language(False)
            if self.max_length != -1:
                value = value[:self.max_length]
            self.values[language] = value
            return None
        
    def __unicode__(self):
        return self.value()
        
    def __str__(self):
        return unicode(self.value()).encode('utf-8')
    
    def __repr__(self):
        return unicode(self.value()).encode('utf-8')