from django.db import models
from django.urls import reverse
from datetime import date

SHOPS = (
    ('C', 'City Customs'),
    ('D', 'Downtown Customs'),
    ('W', 'Westside Customs')
)

# Create your models here.
class Part(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('parts_detail', kwargs={'pk': self.id})

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    # M:M relationship
    parts = models.ManyToManyField(Part)

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
        
class Photo(models.Model):
    url = models.CharField(max_length=200)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for car_id: {self.car_id} @{self.url}"