from django.db import models
from userlog.models import User
# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(blank = True, default = None)
    rating = models.IntegerField()