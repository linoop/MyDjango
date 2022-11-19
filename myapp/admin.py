from django.contrib import admin

from . models import User, Room, Topic, Message, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')



admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Product, ProductAdmin)