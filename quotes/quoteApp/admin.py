from django.contrib import admin
from quoteApp.models import User, Quote, Like
# Register your models here.
admin.site.register(User)
admin.site.register(Quote)
admin.site.register(Like)
