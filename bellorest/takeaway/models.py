from django.db import models
from userlog.models import *
# Create your models here.

class Menu_item(models.Model):
	item_name = models.CharField(max_length=200, null=True,unique=True)
	selling_price = models.IntegerField(null=True)
	order_frequency = models.IntegerField(default=0)

	def __str__(self):
		return self.item_name
	
	def getingred(self):
		return self.ingredient_list_set.all()

class Inventory(models.Model):
	ingredient_name = models.CharField(max_length=100,unique=True)
	quantity = models.IntegerField(help_text = "in grams")
	min_quantity = models.IntegerField(help_text = "in grams")
	cost_price = models.IntegerField(help_text = "cost per gram")

	def __str__(self):
		return self.ingredient_name

class Ingredient_list(models.Model):
	item = models.ForeignKey(Menu_item, on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Inventory, on_delete=models.CASCADE)
	use_quantity = models.IntegerField(help_text = "in grams")

	class Meta:
		unique_together = ('item','ingredient')
	def __str__(self):
		return f"Item : {self.item.item_name} --> Ingredient : {self.ingredient.ingredient_name}"


class Order_Ingredient(models.Model):
	day = models.DateField(auto_now_add=True,blank=True)
	ingredient = models.ForeignKey(Inventory, on_delete = models.CASCADE)
	amount = models.IntegerField(help_text = "in grams")
