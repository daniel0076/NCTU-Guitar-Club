from django.db import models

# Create your models here.
class staff(models.Model):
    name = models.CharField(max_length=20);
    email= models.EmailField();
    phone = models.CharField(max_length=10);
    stuid= models.CharField(max_length=7);

    def __unicode__(self):
        return self.name;
