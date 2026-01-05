from django.db import models
from django.utils.text import slugify
# Create your models here.
# Category model
class Category(models.Model):
    name = models.CharField(max_length=100)
    # Slug URL mein use hota hai (e.g., amazon.com/products/electronics)
    slug = models.SlugField(unique=True,blank=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)


    def __str__(self):
        return self.name

# product model
class Product(models.Model):
    # Ek Category mein bohot saare Products ho sakte hain (ForeignKey)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField(blank=True)
    # Paiso ke liye hamesha DecimalField use karein, FloatField nahi (accuracy ke liye)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    # Product Image (upload_to batata hai ke image kahan save hogi)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product,self).save(*args, **kwargs)

    def __str__(self):
        return self.name