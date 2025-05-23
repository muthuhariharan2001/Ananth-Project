# admin.py
from django.contrib import admin
from .models import ImageHashDBA, ImageHashDBB, HashPair

admin.site.register(ImageHashDBA)
admin.site.register(ImageHashDBB)
admin.site.register(HashPair)
