from django.db import models

# Create your models here.

class Dining_table(models.Model):
	table_id = models.IntegerField(unique=True)
	capacity = models.IntegerField()
	phone_occupied = models.BigIntegerField(null=True, default=None, blank=True)

	def __str__(self):
		strti = str(self.table_id)
		return strti
		
class Reservation(models.Model):
	table_id = models.IntegerField()
	phone = models.BigIntegerField(default=None)
	date_for_res = models.DateField()
	num_diners = models.IntegerField()
	time_for_res = models.TimeField()
	reservation_duration = models.TimeField()

	def __str__(self):
		strp = str(self.phone)
		return strp