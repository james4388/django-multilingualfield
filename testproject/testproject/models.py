from django.db import models
from multilingualfield.fields import MLTextField, MLHTMLField

class MLText(models.Model):
    text = MLTextField()
    
    def __unicode__(self):
        return self.text.get()
        
class MLTextMultiple(models.Model):
    text1 = MLTextField()
    text2 = MLHTMLField()
    text3 = MLTextField()
    
    