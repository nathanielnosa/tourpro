from datetime import datetime
import secrets
from django.db import models
from multiselectfield import MultiSelectField

from users.models import Customer

from .paystack import PayStack
# Create your models here.
class Banner(models.Model):
    image = models.ImageField(upload_to="banner")
    created_at = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    def __str__(self):
        return str(self.created_at)

class Place(models.Model):
    PACKAGES = (
        ('Air fares','Air fares'),
        ('4 Nights Hotel Accomodation','4 Nights Hotel Accomodation'),
        ('Entrance Fees','Entrance Fees'),
        ('Tour Guide','Tour Guide'),
    )

    name = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    description = models.TextField()
    age_range = models.IntegerField()
    price = models.IntegerField()
    main_photo = models.ImageField(upload_to="photos")
    photo_1 = models.ImageField(upload_to="photos")
    photo_2 = models.ImageField(upload_to="photos")
    photo_3 = models.ImageField(upload_to="photos")
    refund_policy = models.CharField(max_length=200)
    package = MultiSelectField(max_length=200, choices=PACKAGES, null=True, blank=True)
    departure = models.DateTimeField(default=datetime.now)
    arrival = models.DateTimeField(default=datetime.now)
    created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.name}:::{self.destination}'
        
    @property
    def get_day(self):
        day = (self.arrival - self.departure).days
        return day
    

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'cart ::: {str(self.id)}'

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True,blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    per_person = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'cart ::: {str(self.cart.id)} - cartproduct ::: {str(self.id)}'



ORDER_STATUS = (
	('Payment Received','Payment Received'),
	('Payment Completed','Payment Completed'),
	('Order Canceled','Order Canceled'),
	)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True, blank=True)
    ordered_by =models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=11)
    email = models.EmailField(null=True,blank=True)
    discount = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(null=True,blank=True)
    order_status = models.CharField(max_length=200, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20,default='PayStack')
    payment_completed = models.BooleanField(default=False,null=True,blank=True)
    ref = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return f'{self.order_status} ::: {str(self.id)}'

    # paystack code
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref=ref)
            if not obj_with_sm_ref:
                self.ref = ref
        super().save(*args,**kwargs)
    
    def amount_value(self)->int:
        return self.amount * 100
        
    def verify_payment(self):
        paystack = PayStack()
        status, result =  paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] /100 == self.amount:
                self.payment_completed = True
            self.save()
        
        if self.order_status == 'Payment Completed':
            self.save()
            self.cart.delete()
        if self.payment_completed:
            return True
        return False
