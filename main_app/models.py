from django.db import models
from django.urls import reverse

SHOPS = (
    ('C', 'City Customs'),
    ('D', 'Downtown Customs'),
    ('W', 'Westside Customs')
)

# Create your models here.
class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.make
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'car_id': self.id})
    
class Tuning(models.Model):
    date = models.DateField()
    shop = models.CharField(max_length=1,
        choices=SHOPS,
        default=SHOPS[0][0]
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.get_shop_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']
