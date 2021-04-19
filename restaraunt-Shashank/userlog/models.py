from django.db import models

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
    

class Delivery_staff(models.Model):
    name = models.CharField(max_length=100)
    area_code = models.IntegerField(null=True,default=None,blank = True)
    available_stat = models.IntegerField(choices = [(0,0),(1,1)])
    phone = models.BigIntegerField()

    def __str__(self):
        return f"{self.name}->{str(self.area_code)}"
    

class Budget(models.Model):
    day = models.DateField()
    spent = models.IntegerField(help_text = "Money spent on ingredients")
    earned = models.IntegerField(help_text = "Money earned from sale")

    def __str__(self):
        return str(self.day)