from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
	first_name = models.CharField(max_length=100, null=True, blank=True) 
	last_name = models.CharField(max_length=100, null=True, blank=True)
	email = models.CharField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=100, null=True, blank=True)
	address1 = models.CharField(max_length=200, null=True, blank=True)
	address2 = models.CharField(max_length=200, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=100, null=True, blank=True)
	zipcode = models.CharField(max_length=20, null=True, blank=True)
	country = models.CharField(max_length=200, null=True, blank=True)
	image = models.ImageField(null=True, blank=True, upload_to="images/")


	def __str__(self):
		return f'{self.first_name} {self.last_name}'