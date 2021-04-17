from django.db import models

# Create your models here.

class User(models.Model):
	phone = models.BigIntegerField()
	name = models.CharField(max_length=100)
	address = models.TextField(default = None,blank = True)
	area_code = models.IntegerField(null=True,default=None,blank = True)
	mon_spent = models.IntegerField()
	loyalty = models.IntegerField()

	def __str__(self):
		return self.phone

class Delivery_staff(models.Model):
	name = models.CharField(max_length=100)
	area_code = models.IntegerField(null=True,default=None,blank = True)
	available_stat = models.IntegerField(choices = [(0,0),(1,1)])
	phone = models.BigIntegerField()

	def __str__(self):
		return self.name