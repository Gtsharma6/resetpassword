from django.contrib import admin
#from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Post,Comment
#from .forms import UserFrom

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [ 'username','bio','dob','email']



admin.site.register(CustomUser,CustomUserAdmin)

class PostAdmin(admin.ModelAdmin):
	model = Post
	list_display = ("author","created_date","title")
	list_filter = ("created_date",)

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)

		
