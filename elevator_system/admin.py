from django.contrib import admin
from .models import Elevator, Request

# Explanation: Registering the Both model in the Django admin site.
# This allows the Elevator model to be managed and accessed through the admin interface.


admin.site.register(Elevator)

admin.site.register(Request)
