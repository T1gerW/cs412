#blog/models.py
#Definte data objects for our application

from django.db import models

# Create your models here.

class Article(models.Model):
    '''Encapsulate the idea of one Article by some author.'''

    #data attributes for Article 
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return String Representation of Object'''

        return f'{self.title} by {self.author}'
    


    

