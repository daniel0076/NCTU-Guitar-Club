from django.db import models

# Create your models here.
class staff(models.Model):
    name = models.CharField(max_length=20);
    email= models.EmailField();
    phone = models.CharField(max_length=10);
    stuid= models.CharField(max_length=7);

    def __unicode__(self):
        return self.name;

class Records(models.Model):
    act_name = models.CharField(max_length=40);
    place = models.CharField(max_length=20);
    date = models.CharField(max_length=20);
    time = models.CharField(max_length=20);
    contact_man = models.CharField(max_length=20);
    status = models.CharField(max_length=10);
    serial = models.CharField(max_length=40);

class Memo(models.Model):
    act_name = models.CharField(max_length=40);
    place = models.CharField(max_length=20);
    date = models.CharField(max_length=20);
    time = models.CharField(max_length=20);
    status = models.CharField(max_length=10);
    other = models.CharField(max_length=100);


class Misc(models.Model):
    db_updated_time = models.CharField(max_length=20);
