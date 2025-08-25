from django.contrib import admin
from .models import Post, FAQ, Event


# Register your models here.
admin.site.register(Post)
admin.site.register(FAQ)
admin.site.register(Event)