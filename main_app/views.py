from django.shortcuts import render, redirect
from . models import Car, Part, Photo
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from . forms import TuningForm
import uuid, boto3
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# S3 bucket variables 
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'carcollector-app-storage'

class CarCreate(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['make', 'model', 'year', 'description', 'age']
    success_url = '/cars/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CarUpdate(LoginRequiredMixin, UpdateView):
    model = Car
    fields = ['model', 'year', 'description', 'age']

class CarDelete(LoginRequiredMixin, DeleteView):
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

@login_required
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

class PartCreate(LoginRequiredMixin, CreateView):
    model = Part
    fields = '__all__'

class PartUpdate(LoginRequiredMixin, UpdateView):
    model = Part
    fields = ['name', 'color']

class PartDelete(LoginRequiredMixin, DeleteView):
    model = Part
    success_url = '/parts/'

@login_required
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

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)