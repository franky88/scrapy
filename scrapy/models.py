from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

# Create your models here.
class URLaddress(models.Model):
    url = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'URL addresses'
        ordering = ['-timestamp']

    def __str__(self):
        return self.url
    
class Page(models.Model):
    url_address = models.ForeignKey(URLaddress, on_delete=models.CASCADE)
    link = models.URLField(verbose_name="links", blank=True, null=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.link
    
class Product(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=False)
    link = models.URLField()
    disclosure = models.TextField(verbose_name="disclosure", null=True, blank=True)

    def __str__(self):
        return self.name