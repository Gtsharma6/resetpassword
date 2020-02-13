from django.db import models

# Create your models here.


class Country(models.Model):
	name = models.CharField(max_length=200)


	def __str__(self):
		return self.name




class State(models.Model):
	country = models.ForeignKey(Country,on_delete=models.CASCADE)
	name = models.CharField(max_length=200)


	def __str__(self):
		return self.name



class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name