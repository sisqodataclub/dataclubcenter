from django.db import models
import datetime
from django.utils import timezone


# models.py



###########################################################################
class AvailableDateTime(models.Model):
    datetime = models.DateTimeField(unique=True)

    def __str__(self):
        return str(self.datetime)




# Categories of Products
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/product/', null=True, blank=True, default='promo.jpeg')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


# Categories of Products
class CategoryA(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categorya'

# Customers
class Customer(models.Model):
	first_name = models.CharField(max_length=50)
	selected_date = models.CharField(max_length=50, default='', blank=True, null=True)
	email =models.EmailField(max_length=100, default='', blank=True)
	address = models.CharField(max_length=100, default='', blank=True)
	postcode = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=100, default='', blank=True)
	country =models.CharField(max_length=100, default='',blank=True)
	phone = models.CharField(max_length=100, default='',blank=True)
	paymentM= models.CharField(max_length=1000, default='', blank=True, null=True)

	def __str__(self):
		return f'{self.first_name} {self.email}'
	
################################################################################################################################
class Address(models.Model):
	address = models.CharField(max_length=1000)
	postcode = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	
	def __str__(self):
		return f'{self.address}, {self.postcode}, {self.city}, {self.country}'

# All of our Products
class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	categorya= models.ForeignKey(CategoryA, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	description = models.CharField(max_length=250, default='', blank=True, null=True)
	image = models.ImageField(upload_to='uploads/product/')
	image1 = models.ImageField(upload_to='uploads/product/', blank=True, null=True, default='default_image.jpg')
	size_code= models.CharField(max_length=250, default='', blank=True, null=True)

	# Add Sale Stuff
	is_sale = models.BooleanField(default=False)
	sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	size = models.CharField(max_length=20, choices=[('-', '-'),('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('yes', 'Yes'), ('no', 'No'),])

	def __str__(self):
		return self.name


# Custom Products
class CProduct(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, default='', blank=True)
    product = models.CharField(max_length=50)
    description = models.CharField(max_length=2000, default='', blank=True, null=True)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='uploads/product/')
    image1 = models.ImageField(upload_to='uploads/product/', blank=True, null=True, default='default_image.jpg')

    def __str__(self):
        return self.name




# Customer Orders
class Order(models.Model):
	order_id = models.CharField(max_length=100, primary_key=True)
	product = models.ManyToManyField(Product)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	address = models.ForeignKey(Address, on_delete=models.CASCADE)
	email = models.EmailField(max_length=1000)
	delivery_status = models.CharField(max_length=100, default='', blank=True)
	delivery_company = models.CharField(max_length=100, default='', blank=True)
	tracking_id = models.CharField(max_length=100, default='', blank=True)
	date = models.DateField(default=datetime.datetime.today)
	status = models.BooleanField(default=False)
	
	def __str__(self):
		products_str = ', '.join(str(product) for product in self.product.all())
		return f'{self.customer} - {products_str} - {self.address}'
##################################################################################################



class CartItem(models.Model):
	items = models.CharField(max_length=1000)
	quantity = models.CharField(max_length=1000)
	total = models.CharField(max_length=1000)
	first_name = models.CharField(max_length=1000)
	email = models.CharField(max_length=1000)
	selected_date= models.CharField(max_length=1000, null=True,blank=True)
	paymentM= models.CharField(max_length=1000, default='', blank=True, null=True)


	def __str__(self):
		return str(self.email)

##################################################################################################
class coupons(models.Model):
	code = models.CharField(max_length=50, unique=True)
	discountid = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return self.code 
