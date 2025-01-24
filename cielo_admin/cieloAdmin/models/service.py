from django.db import models

class OptionGroup(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Option(models.Model):
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
