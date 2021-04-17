from django.db import models

# Create your models here.

class loyalty_level(models.Model):
	loyalty_points = models.IntegerField(null=True)
	discount_perc = models.IntegerField(null=True)

	def __str__(self):
		return self.loyalty_points

class menu_items(models.Model):
	item_id = models.IntegerField(null=True)
	item_name = models.CharField(max_length=200, null=True)
	selling_price = models.IntegerField(null=True)

	def __str__(self):
		return self.item_name