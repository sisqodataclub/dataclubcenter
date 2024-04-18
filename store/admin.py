from django.contrib import admin
from .models import Category, Customer, Product, Order, Address, CProduct, CartItem, coupons, CategoryA, AvailableDateTime

class ProductAdmin(admin.ModelAdmin):
    # Get all field names including the primary key
    list_display = [field.name for field in Product._meta.fields]



admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('product',)

admin.site.register(Order, OrderAdmin)
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(CProduct)
admin.site.register(CartItem)
admin.site.register(coupons)
admin.site.register(CategoryA)
admin.site.register(AvailableDateTime)



