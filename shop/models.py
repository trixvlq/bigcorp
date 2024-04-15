import random
import string

from django.urls import reverse
from django.db import models
from django.utils.text import slugify


def random_slug():
    """
    Generates a random slug consisting of 10 characters from the set of lowercase letters and digits.
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

class Category(models.Model):
    """
       Represents a Category in the database with fields for name, parent relationship, slug, and creation timestamp.
   """
    name = models.CharField(max_length=255, db_index=True, verbose_name='category')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='parent')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, null=False, verbose_name='slug')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '->'.join(full_path[::-1])

    def save(self, *args, **kwargs):
        """
        Save the object with a slug if not already set, and then call the superclass's save method.
        """
        if not self.slug:
            self.slug = slugify(random_slug() + 'PickBetterName' + self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_list', kwargs={'slug': self.slug})


class Product(models.Model):
    '''
    Model representing a product in the system.
    '''
    title = models.CharField(max_length=255, db_index=True, verbose_name='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='category')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, null=False, verbose_name='slug')
    brand = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=99.99, verbose_name='price')
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='created_at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated_at')

    class Meta:
        unique_together = ('slug', 'category')
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})


class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Return a queryset that filters products by availability.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    objects = ProductManager()

    class Meta:
        proxy = True
        verbose_name = 'product'
        verbose_name_plural = 'products'
