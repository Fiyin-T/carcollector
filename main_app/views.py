from django.shortcuts import render, redirect
from . models import Car
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . forms import TuningForm

class CarCreate(CreateView):
    model = Car
    fields = '__all__'
    success_url = '/cars/'

class CarUpdate(UpdateView):
    model = Car
    fields = ['model', 'year', 'description', 'age']

class CarDelete(DeleteView):
    model = Car
    success_url = '/cars/'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cars_index(request):
    cars = Car.objects.all()
    return render(request, 'cars/index.html', { 'cars': cars }) 

def cars_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    tuning_form = TuningForm()
    return render(request, 'cars/detail.html', { 'car': car, 'tuning_form': tuning_form })

def add_tuning(request, car_id):
    form = TuningForm(request.POST)
    if form.is_valid():
        new_tuning = form.save(commit=False)
        new_tuning.car_id = car_id
        new_tuning.save()
    return redirect('detail', car_id=car_id)