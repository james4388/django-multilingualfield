django-multilingualfield
===================

Simply store your multilingual text content in json language : content pair value.

This is first django model field approach that store multilingual text in json format. It's auto return in current system lenguage (determine by translation.get_current_language). Just use it like normal text field, everything is handle automatically

This project based on Matthew Schinckel's jsonfield https://bitbucket.org/schinckel/django-jsonfield/. Thank Schinckel

Usage
-----

To use, just install the package, and then use the field::

    from django.db import models
    from multilingualfield import MLTextField, MLHTMLField
    
    class MyModel(models.Model):
        text = MLTextField()
        html = MLHTMLField()
        
Then use it like normal text field

    >>>from django.utils import translation
    >>>translation.active('en')
    
    >>>m = MyModal.objects.create(text='Hello world',html='<b>Hello world</b>');
    >>>m.text
    Hello world
    >>>translation.active('fr')
    >>>m.text       #Auto fallback to first language (if any).
    Hello world
    >>>m.text.value('Bonjour')
    >>>m.text.value('Ciao','es')
    >>>m.text
    Bonjour
    >>>m.save()
    >>>m.text.get_available_language()
    ['en', 'fr']
    >>>m.text.remove_language('en')
    
Now, it will store multilingual text as a json string in the
database.  When you instantiate/fetch the object, it will be turned back
into a python LanguageText object.

There is also a form and widget that automatic create language tab when you edit a field in admin. CKEditor may be add for html field.

Notes
~~~~~
Please help me test this approach, is it good/bad approach?

  
History
----------

0.1 Initilize


Todo
----------
A LOTS