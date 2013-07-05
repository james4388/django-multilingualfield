from django.db import models
from multilingualfield.fields import MLTextField

class MLText(models.Model):
    text = MLTextField()
    
    def __unicode__(self):
        return self.text.get()
        
class MLTextMultiple(models.Model):
    text1 = MLTextField()
    text2 = MLTextField()
    text3 = MLTextField()
    
    