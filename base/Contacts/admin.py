from django.contrib import admin
from .models import Contact, UserMapContact, Profile, spamPhoneNumber

admin.site.register(Contact)
admin.site.register(UserMapContact)
admin.site.register(Profile)
admin.site.register(spamPhoneNumber)