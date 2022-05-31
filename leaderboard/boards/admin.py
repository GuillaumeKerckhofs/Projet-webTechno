from django.contrib import admin
from .models import submittedModel,Boards,Link,Category

# Register your models here.

admin.site.register(Boards)
admin.site.register(Link)
admin.site.register(Category)
admin.site.register(submittedModel)
