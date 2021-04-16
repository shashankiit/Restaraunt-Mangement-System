from django.db import models

# Create your models here.
class review(models.Model):
    phone = models.CharField(max_length=10)
    date = models.DateField()
    comment = models.TextField()
    rating = models.CharField(max_length=1)