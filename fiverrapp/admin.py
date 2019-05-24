from django.contrib import admin
from .models import Gig, Profile, Purchase, Review

# Register your models here.
admin.site.register(Profile)
admin.site.register(Gig)
admin.site.register(Purchase)
admin.site.register(Review)