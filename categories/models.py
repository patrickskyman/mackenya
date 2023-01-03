import uuid
from django.urls import reverse
import django_filters
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.utils.text import slugify
from django.template.loader import render_to_string

from django.core.validators import MinValueValidator
from django.db.models import Count, Sum



from ckeditor_uploader.fields import RichTextUploadingField 

from django.conf import settings
#from . import exceptions

import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.models import ( 
    AbstractUser,
    BaseUserManager,
)

class UserManager(BaseUserManager): 
    use_in_migrations = True
    
    def _create_user(self, email, password,**extra_fields): 
        if not email:
            raise ValueError("The given email must be set") 
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db) 
        return user

    def create_user(self, email, password=None, **extra_fields): 
        extra_fields.setdefault("is_staff", False) 
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields): 
        extra_fields.setdefault("is_staff", True) 
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True: 
            raise ValueError(
                "Superuser must have is_staff=True." )
        if extra_fields.get("is_superuser") is not True: 
            raise ValueError(
                "Superuser must have is_superuser=True." )
        return self._create_user(email, password, **extra_fields)

class User(AbstractUser): 
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    @property
    def is_employee(self):
        return self.is_active and (
            self.is_superuser
            or self.is_staff
            and self.groups.filter(name="Employees").exists()
        )

    @property
    def is_dispatcher(self):
        return self.is_active and (
            self.is_superuser
            or self.is_staff
            and self.groups.filter(name="Dispatchers").exists()
        )

from django.template.loader import render_to_string
# Create your models here.
class ActiveManager(models.Manager): 
    def active(self):
        return self.filter(active=True)

class Brand(models.Model):
    title = models.CharField(max_length=255, default='') 
    slug = models.SlugField(max_length=200, unique=True, help_text='Type the brand of your product in small letters')
    class Meta:
        ordering = ['title']


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('brand', args=[self.slug])



class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text='Type the title of your product in small letters') 
    meta_keywords = models.CharField("Meta Keywords",max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag') 
    meta_description = models.CharField("Meta Description", max_length=255,help_text='Content for description meta tag') 
    class Meta:
        ordering = ['title'] 
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.title 


    objects = ActiveManager()

class ActiveProductManager(models.Manager): 
    def get_query_set(self):
        return super(ActiveProductManager, self).get_query_set().filter(is_active=True)


class FeaturedProductManager(models.Manager): 
    def all(self):
        return super(FeaturedProductManager, self).all() .filter(is_active=True).filter(featured=True)

class Product(models.Model):
    #id = models.UUIDField(
        #primary_key=True, default=uuid.uuid4, editable=False)
    brands = models.ManyToManyField(Brand, blank=True)

    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE) 

    #release_date = models.DateField()
    title = models.CharField(max_length=200, help_text='Title of your product, e.g Sofa')
    #image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    #image2 = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    #image3 = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)

    is_active = models.BooleanField(default=True) 
    bestseller = models.BooleanField(default=False, help_text="1=bestseller") 
    flashsales = models.BooleanField(default=False, help_text="1=flashsales") 
    toppicksforyou = models.BooleanField(default=False, help_text="1=Top picks for you") 
    monthlysales= models.BooleanField(default=False, help_text="1=monthlysales") 
    bestdeals= models.BooleanField(default=False, help_text="1=bestdeals") 
    brand = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9,decimal_places=2,help_text='Current price')
    old_price = models.DecimalField(max_digits=9,decimal_places=2,blank=True,default=0.00, help_text='Old price')
    quantity = models.IntegerField()
    slug = models.SlugField(max_length=200, unique=True, help_text='Type the title of your product in small letters, e.g sofa') 
    meta_keywords = models.CharField(max_length=255,help_text='Comma-delimited set of SEO keywords for meta tag') 
    meta_description = models.CharField(max_length=255,help_text='Content for description meta tag') 
    #overview = models.TextField(help_text='Describe your product and terms')
    overview = RichTextUploadingField() # CKEditor Rich Text Field
    created = models.DateTimeField(auto_now_add=True) 
    class Meta:
        ordering = ['-created'] 
        #index_together = (('id', 'slug'),)
    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse('product_detail',
                       args=[self.id, self.slug])

   # def get_absolute_url(self):
        #return reverse('product_detail', kwargs={"pk": self.pk})
        

    objects = models.Manager() 
    active = ActiveProductManager()               
    objects = ActiveManager()

    featured = FeaturedProductManager()

    last_spoken_to = models.ForeignKey(
        User,
        null=True,
        related_name="cs_chats",
        on_delete=models.SET_NULL,
    )  


def cross_sells_hybrid(self):
        from categories.models import Basket, BasketLine
        from django.contrib.auth.models import User
        from django.db.models import Q
        baskets = Basket.objects.filter(basketline__product=self) 
        users = User.objects.filter(basket__basketline__product=self) 
        items = BasketLine.objects.filter( Q(basket__in=baskets) |
                    Q(basket__user__in=users)
                    ).exclude(product=self)
        products = Product.filter(basketline__in=items).distinct() 
        return products



class ProductImage(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE )
    image = models.ImageField(upload_to="product-images")
    featured = models.BooleanField(default=False, help_text="1=featured") 
    thumbnail = models.ImageField( upload_to="product-thumbnails", null=True
)



class Address(models.Model): 
    SUPPORTED_COUNTRIES = (
        ("uk", "United Kingdom"),
        ("us", "United States of America"), 
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=60)
    telephone = models.CharField(max_length=60)
    address1 = models.CharField("Address line 1", max_length=60) 
    address2 = models.CharField(
    "Address line 2", max_length=60, blank=True 
    )
    zip_code = models.CharField(
        "ZIP / Postal code", max_length=12
    )
    city = models.CharField(max_length=60) 
    country = models.CharField(max_length=3, choices=SUPPORTED_COUNTRIES 
    )

    def __str__(self): 
        return ", ".join(
        [
                self.name,
                self.telephone,
                self.address1, 
                self.address2, 
                self.zip_code, 
                self.city, 
                self.country,
        ] 
        )

class Basket(models.Model):
    OPEN = 10
    SUBMITTED = 20
    STATUSES = ((OPEN, "Open"), (SUBMITTED, "Submitted"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.IntegerField(choices=STATUSES, default=OPEN)

    def is_empty(self):
        return self.basketline_set.all().count() == 0

    def count(self):
        return sum(i.quantity for i in self.basketline_set.all())

    def create_order(self, billing_address, shipping_address):
        if not self.user:
            raise exceptions.BasketException(
                "Cannot create order without user"
            )

        logger.info(
            "Creating order for basket_id=%d"
            ", shipping_address_id=%d, billing_address_id=%d",
            self.id,
            shipping_address.id,
            billing_address.id,
        )

        order_data = {
            "user": self.user,
            "billing_name": billing_address.name,
            "billing_address1": billing_address.address1,
            "billing_address2": billing_address.address2,
            "billing_zip_code": billing_address.zip_code,
            "billing_city": billing_address.city,
            "billing_country": billing_address.country,
            "shipping_name": shipping_address.name,
            "shipping_address1": shipping_address.address1,
            "shipping_address2": shipping_address.address2,
            "shipping_zip_code": shipping_address.zip_code,
            "shipping_city": shipping_address.city,
            "shipping_country": shipping_address.country,
        }
        order = Order.objects.create(**order_data)
        c = 0
        for line in self.basketline_set.all():
            for item in range(line.quantity):
                order_line_data = {
                    "order": order,
                    "product": line.product,
                }
                order_line = OrderLine.objects.create(
                    **order_line_data
                )
                c += 1

        logger.info(
            "Created order with id=%d and lines_count=%d",
            order.id,
            c,
        )

        self.status = Basket.SUBMITTED
        self.save()
        return order

class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE) 
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE )
    quantity = models.PositiveIntegerField( default=1, validators=[MinValueValidator(1)]
)


class Order(models.Model):
    NEW = 10
    PAID = 20
    DONE = 30
    STATUSES = ((NEW, "New"), (PAID, "Paid"), (DONE, "Done"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUSES, default=NEW)

    billing_name = models.CharField(max_length=60)
    billing_address1 = models.CharField(max_length=60)
    billing_address2 = models.CharField(
        max_length=60, blank=True
    )
    billing_zip_code = models.CharField(max_length=12)
    billing_city = models.CharField(max_length=60)
    billing_country = models.CharField(max_length=3)

    shipping_name = models.CharField(max_length=60)
    shipping_address1 = models.CharField(max_length=60)
    shipping_address2 = models.CharField(
        max_length=60, blank=True
    )
    shipping_zip_code = models.CharField(max_length=12)
    shipping_city = models.CharField(max_length=60)
    shipping_country = models.CharField(max_length=3)

    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    #last_spoken_to = models.ForeignKey(
        #User,
        #null=True,
        #related_name="cs_chats",
        #on_delete=models.SET_NULL,
    #)  

    @property
    def mobile_thumb_url(self):
        products = [i.product for i in self.lines.all()] 
        if products:
            img = products[0].productimage_set.first()
            if img:
                return img.thumbnail.url
    
    @property
    def summary(self):
        product_counts = self.lines.values( 
            "product__title"
        ).annotate(c=Count("product__title")) 
        pieces = []
        for pc in product_counts:
            pieces.append(
                "%s x %s" % (pc["c"], pc["product__title"])
            )
        return ", ".join(pieces)

    @property
    def total_price(self):
        res = self.lines.aggregate( 
            total_price=Sum("product__price")
        )
        return res["total_price"]


class OrderLine(models.Model):
    NEW = 10
    PROCESSING = 20
    SENT = 30
    CANCELLED = 40
    STATUSES = (
        (NEW, "New"),
        (PROCESSING, "Processing"),
        (SENT, "Sent"),
        (CANCELLED, "Cancelled"),
    )

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="lines"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT
    )
    status = models.IntegerField(choices=STATUSES, default=NEW)

class SearchTerm(models.Model):
    q = models.CharField(max_length=200)
    tracking_id = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True) 
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __unicode__(self): 
        return self.q

    def __str__(self):
        return self.q

class PageView(models.Model): 
    ##model class for tracking the pages that a customer views """
    class Meta:
        abstract = True
    
    date = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=255, db_index=True)
    
class ProductView(PageView):
    ##""" tracks product pages that customer views """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.tracking_id
    