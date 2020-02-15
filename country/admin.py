from django.contrib import admin


from .models import Country,State,Person

# Register your models here.


class CountryAdmin(admin.ModelAdmin):
	model = Country
	list_display = ['name']


admin.site.register(Country,CountryAdmin)
admin.site.register(State)
admin.site.register(Person)

