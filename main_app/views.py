from django.shortcuts import render, redirect
from . models import Car, Part, Photo
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from . forms import TuningForm
import uuid, boto3

# S3 bucket variables 
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'carcollector-app-storage'

class CarCreate(CreateView):
    model = Car
    fields = ['make', 'model', 'year', 'description', 'age']
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
    # Get parts that car doesn't have
    parts_car_doesnt_have = Part.objects.exclude(id__in = car.parts.all().values_list('id'))
    # instantiate TuningForm to be rendered in template
    tuning_form = TuningForm()
    return render(request, 
        'cars/detail.html', { 
        'car': car, 
        'tuning_form': tuning_form, 
        # Add parts to be displayed
        'parts': parts_car_doesnt_have 
        })

def add_tuning(request, car_id):
    # create ModelForm using the data in request.POST
    form = TuningForm(request.POST)
    # validate form
    if form.is_valid():
        new_tuning = form.save(commit=False)
        new_tuning.car_id = car_id
        new_tuning.save()
    return redirect('detail', car_id=car_id)

class PartList(ListView):
    model = Part

class PartDetail(DetailView):
    model = Part

class PartCreate(CreateView):
    model = Part
    fields = '__all__'

class PartUpdate(UpdateView):
    model = Part
    fields = ['name', 'color']

class PartDelete(DeleteView):
    model = Part
    success_url = '/parts/'

def assoc_part(request, car_id, part_id):
    Car.objects.get(id=car_id).parts.add(part_id)
    return redirect('detail', car_id=car_id)

def add_photo(request, car_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # unique "key" for S3 and image file extension
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # check
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # assign to car_id or car (if car object)
            photo = Photo(url=url, car_id=car_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', car_id=car_id)