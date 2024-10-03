from django.db import models

# Create your models here.
class Contact(models.Model):
    firstname = models.CharField( max_length=20,blank=False)
    lastname = models.CharField( max_length=30,blank=False)
    email = models.EmailField( max_length=250)
    tel= models.IntegerField(unique=True,blank=False)
    address= models.CharField( max_length=50) 
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering= ['-id']
        