from django.db import models
from django.db.models import CASCADE

from user.models import CustomUser


# Create your models here.
class Advertisement(models.Model):
    FIELD_CHOICES = (
        ('fashion', 'Fashion'), ('food', 'Food'), ('health', 'Health'), ('other', 'Other'),
    )
    SNS_CHOICES = (
        ('instagram', 'Instagram'), ('youtube', 'Youtube'), ('other', 'Other'),
    )

    post_account = models.ForeignKey(CustomUser, on_delete=CASCADE, blank=True)
    thumbnail = models.ImageField(upload_to='advertisement/', default='product.svg')
    title = models.CharField(max_length=128, blank=True)
    name = models.CharField(max_length=128, blank=True)
    sns = models.CharField(max_length=50, choices=SNS_CHOICES, blank=True)
    method = models.CharField(max_length=128, blank=True)
    field = models.CharField(max_length=50, choices=FIELD_CHOICES, blank=True)  #분야
    description = models.TextField(default='description of the product')
    min_budget = models.PositiveIntegerField(default=0)
    max_budget = models.PositiveIntegerField(default=0)
    detail_1 = models.ImageField(upload_to='advertisement/', default='product.svg')
    detail_2 = models.ImageField(upload_to='advertisement/', default='product.svg')

    def __str__(self):
        return self.title
