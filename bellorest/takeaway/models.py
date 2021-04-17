from django.db import models

# Create your models here.

class Menu_item(models.Model):
	item_name = models.CharField(max_length=200, null=True)
	selling_price = models.IntegerField(null=True)

	def __str__(self):
		return self.item_name