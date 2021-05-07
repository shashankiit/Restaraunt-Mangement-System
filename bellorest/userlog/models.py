from django.db import models
from reserve_tab.models import *
# Create your models here.
class Loyalty_level(models.Model):
	loyalty_points = models.IntegerField(unique=True)
	discount_perc = models.IntegerField()

	def __str__(self):
		return f"Loyalty level:{self.loyalty_points}"

class User(models.Model):
    phone = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField(default = None,blank = True)
    area_code = models.IntegerField(null=True,default=None,blank = True)
    mon_spent = models.IntegerField()
    loyalty = models.ForeignKey(Loyalty_level,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}->{str(self.phone)}"

    def loyaltyupdate(self):
        if self.mon_spent < 2000 :
            self.loyalty = Loyalty_level.objects.get(loyalty_points=0)
        elif self.mon_spent < 4000 :
            self.loyalty = Loyalty_level.objects.get(loyalty_points=1)
        elif self.mon_spent < 6000 :
            self.loyalty = Loyalty_level.objects.get(loyalty_points=2)
        elif self.mon_spent < 8000 :
            self.loyalty = Loyalty_level.objects.get(loyalty_points=3)
        elif self.mon_spent < 12000 :
            self.loyalty = Loyalty_level.objects.get(loyalty_points=4)
        else :
            self.loyalty = Loyalty_level.objects.get(loyalty_points=5)
    

class Delivery_staff(models.Model):
    name = models.CharField(max_length=100)
    area_code = models.IntegerField(null=True,default=None,blank = True)
    available_stat = models.IntegerField(choices = [(0,0),(1,1)])
    phone = models.BigIntegerField()

    def __str__(self):
        return f"{self.name}->{str(self.area_code)}"
    

class Budget(models.Model):
    day = models.DateField()
    spent = models.IntegerField(help_text = "Money spent on ingredients",default=0)
    earned = models.IntegerField(help_text = "Money earned from sale",default=0)

    def __str__(self):
        return str(self.day)