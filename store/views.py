from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Customer, Order, Address, CProduct, CartItem, coupons, AvailableDateTime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django import forms
from django.core.exceptions import ObjectDoesNotExist  # Add this line
from .forms import CustomerForm, CProductForm
from cart.cart import Cart
import stripe
from django.http import JsonResponse
from django.utils import timezone



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')


def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {"categories":categories})	

def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    # Fetch other products with the same size code
    other_products = Product.objects.filter(size_code=product.size_code).exclude(id=pk)
    return render(request, 'product.html', {'product': product, 'other_products': other_products})

def personal1(request, pk):
    product = Product.objects.get(id=pk)
    other_products = Product.objects.filter(size_code=product.size_code).exclude(id=pk)
    if request.method == 'POST':
        form = CProductForm(request.POST, request.FILES, product_name=product.name)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for shopping! We will get in touch with you to discuss your order further.')
            return redirect('home')  # Redirect to the list view
    else:
        form = CProductForm(product_name=product.name)
    return render(request, 'personal.html', {'product': product, 'other_products': other_products, 'form': form})

def order(request, pk):
    try:
        order = Order.objects.get(order_id=pk)
        return render(request, 'customer_list.html', {'order': order})
    
    
    except ObjectDoesNotExist:
        messages.success(request, "There was an error, or the order does not exist.")
        return redirect('orderh')

def orderh(request):
    orders = Order.objects.all()
    return render(request, 'order.html', {'orders': orders})


def home(request):
    products = Product.objects.all()
    unique_size_codes = Product.objects.values_list('size_code', flat=True).distinct()
    unique_products = []
    for size_code in unique_size_codes:
        product = Product.objects.filter(size_code=size_code).first()
        if product:
            unique_products.append(product)
    return render(request, 'home.html', {'products': products, 'unique_products': unique_products})

def allproducts(request):
    products = Product.objects.all()
    unique_size_codes = Product.objects.values_list('size_code', flat=True).distinct()
    unique_products = []
    for size_code in unique_size_codes:
        product = Product.objects.filter(size_code=size_code).first()
        if product:
            unique_products.append(product)
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'all_products.html', {'products': products, 'unique_products': unique_products, 'categories': categories})


def service(request):
    # Fetch all products
 
    products = Product.objects.all()
    
    # Fetch products with empty size_code
    code_products = Product.objects.exclude(size_code__isnull = True)
    no_code_products = Product.objects.exclude(size_code__isnull = False)

    # Fetch unique size codes excluding empty strings
    unique_size_codes = code_products.values_list('size_code', flat=True).distinct()
    
    # Initialize list to store unique products
    unique_products = []
    
    # Iterate over unique size codes
    for size_code in unique_size_codes:
        # Fetch the first product with the current size code
        product_with_size_code = Product.objects.filter(size_code=size_code).first()
        
        # Add product to unique_products list if found
        if product_with_size_code:
            unique_products.append(product_with_size_code)
    
    # Extend unique_products list with products having empty size_code
    unique_products.extend(no_code_products)
    # Fetch all categories
    categories = Category.objects.all()

    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    # Render the template with products, unique_products, and categories
    return render(request, 'service.html', {'products': products, 'unique_products': unique_products, 'categories': categories, "cart_products":cart_products, "quantities":quantities, "totals":totals})



def about(request):
	return render(request, 'about.html', {})


def personal(request):
    products = Product.objects.all()
    unique_size_codes = Product.objects.values_list('size_code', flat=True).distinct()
    unique_products = []
    for size_code in unique_size_codes:
        product = Product.objects.filter(size_code=size_code).first()
        if product:
            unique_products.append(product)
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'product1.html', {'products': products, 'unique_products': unique_products, 'categories': categories})	

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('home')



def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("You Have Registered Successfully!! Welcome!"))
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})





# store/views.py
from .forms import CustomerForm


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def create_customer(request):
    available_dates = AvailableDateTime.objects.values_list('datetime', flat=True)
    
    if request.method == 'POST':
        
        form = CustomerForm(request.POST)

        if form.is_valid():
            # Save the customer instance
            customer = form.save(commit=False)

            # Create a new Address instance
            address = Address.objects.create(
                address=form.cleaned_data['address'],
                postcode=form.cleaned_data['postcode'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country']
            )

            # Assign the created address to the customer
            customer.address = address
            customer.save()
            
            # Save cart items to the database
            cart = Cart(request)
            total = str(cart.cart_total())
            items = str(cart.get_prods())
            #cart_items = cart.get_items()  # Retrieve cart items
            quantity = str(cart.get_quants())
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            # Retrieve cart items from session
            cart_products = cart.get_prods()
            quantities = cart.get_quants()
            totals = cart.cart_total()

            
            # Get the selected date

            # Create CartItem instance with selected date
            
            CartItem.objects.create(
                items=items,
                quantity=quantity,
                total=total,
                first_name=first_name,
                email=email,
                selected_date=request.POST.get('selected_date'),
                paymentM=request.POST.get('paymentM')
            )
            
            # Sending email
            subject = 'Thank you for your Booking!'
            html_message = render_to_string('email_template.html', {'customer': customer, "cart_products":cart_products, "quantities":quantities, "totals":totals})
            plain_message = strip_tags(html_message)
            from_email = 'your-email@example.com'
            to_email = [email]  # Assuming email is a field in the customer form
            send_mail(subject, plain_message, from_email, to_email, html_message=html_message)
            # Send quote by email if selected

            # Redirect based on payment method
            paymentM = request.POST.get('paymentM')

            if paymentM == 'CASH':
                return redirect('home')  # Redirect to customer detail page
            else:
                return redirect('create_payment_link')
                  

    else:
        form = CustomerForm()

    return render(request, 'create_customer.html', {'form': form, 'available_dates': available_dates})




# Set your Stripe API key
stripe.api_key = "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" 

def cart_summary1(request):
    # Get the cart
    cart = Cart(request)
    totals1 = cart.cart_total()

    # Store the total in the session as a numerical value
    request.session['totals1'] = totals1

    return totals1

def create_payment_link(request):
    cart = Cart(request)
    total = str(cart.cart_total())
    
    # Get the cart total using the cart_summary1 method
    totals1 = float(request.session.get('totals1', total))  # Default to 0 if 'totals1' is not in the session

    amount = int(totals1 * 100)  # Convert to cents (e.g., $50.00)
    currency = "usd"
    success_url = "http://localhost:8000/success/"  # Update with your success URL
    cancel_url = "http://localhost:8000/cancel/"  # Update with your cancel URL

    try:
        line_items = [{
            'price_data': {
                'currency': currency,
                'unit_amount': amount,
                'product_data': {
                    'name': 'Payment'
                },
            },
            'quantity': 1,
        }]
        payment_link = stripe.checkout.Session.create(
            success_url=success_url,
            cancel_url=cancel_url,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
        )

        # Retrieve the payment link URL
        link_url = payment_link.url

        # Render the template with the payment link
        return redirect(link_url)

    except stripe.error.StripeError as e:
        # Handle any errors that occur during payment link creation
        print(f"Error creating payment link: {e}")
        return render(request, 'payment_error.html')
	




def create_order(request):
    if request.method == 'POST':
        # Assuming you have cart_products and quantities available from somewhere
        cart_products = [1, 2, 3]  # Example list of product IDs
        quantities = [3, 2, 1]     # Example list of quantities
        q1 = request.session.get('q1', cart_products)
        q2 = request.session.get('q2', quantities)

        CartItem.objects.create(product=q1, quantity=q2)

        # Redirect to create_customer view after saving cart items
        return redirect('create_customer')

    else:
        return redirect('home')  # Redirect to cart summary page if the request method is not POST

def save_data(request):
    cart = Cart(request)
    total = str(cart.cart_total())
    items = str(cart.get_prods())
    quantity = str(cart.get_quants())
    first_name = 'na'
    email = 'na'
    
    # Create a new CartItem object and save it to the database
    CartItem.objects.create(
        items=items, 
        quantity=quantity, 
        total=total, 
        first_name=first_name, 
        email=email,
        
    )
    return redirect('create_customer')

def save_quote(request):
    cart = Cart(request)
    total = str(cart.cart_total())
    items = str(cart.get_prods())
    quantity = str(cart.get_quants())
    first_name = 'hi'
    email = request.POST.get('email')
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    
    # Create a new CartItem object and save it to the database
    CartItem.objects.create(
        items=items, 
        quantity=quantity, 
        total=total, 
        first_name=first_name, 
        email= email,
        
    )

    # Sending email
    subject = 'Thank you for your Booking!'
    html_message = render_to_string('quote.html', {"cart_products":cart_products, "quantities":quantities, "totals":totals})
    plain_message = strip_tags(html_message)
    from_email = 'your-email@example.com'
    to_email = [email]  # Assuming email is a field in the customer form
    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)


    return redirect('create_customer')



def fetch_product_id(request):
    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')
        try:
            coupon = coupons.objects.get(code=coupon_code)
            product_id = coupon.discountid_id  # Retrieve the product ID from the coupon object
            return JsonResponse({'product_id': product_id})
        except coupons.DoesNotExist:
            return JsonResponse({'error': 'Coupon not found'}, status=404)