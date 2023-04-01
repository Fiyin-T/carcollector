from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # Cars URLs
    path('cars/', views.cars_index, name='index'),
    path('cars/<int:car_id>/', views.cars_detail, name='detail'),
    path('cars/create/', views.CarCreate.as_view(), name='cars_create'),
    path('cars/<int:pk>/update/', views.CarUpdate.as_view(), name='cars_update'),
    path('cars/<int:pk>/delete/', views.CarDelete.as_view(), name='cars_delete'),
    # Tuning URLs
    path('cars/<int:car_id>/add_tuning/', views.add_tuning, name='add_tuning'),
    # Parts URLs
    path('parts/', views.PartList.as_view(), name='parts_index'),
    path('parts/<int:pk>/', views.PartDetail.as_view(), name='parts_detail'),
    path('parts/create/', views.PartCreate.as_view(), name='parts_create'),
    path('parts/<int:pk>/update/', views.PartUpdate.as_view(), name='parts_update'),
    path('parts/<int:pk>/delete/', views.PartDelete.as_view(), name='parts_delete'),
    # associate a part with a car (M:M)
    path('cars/<int:car_id>/assoc_part/<int:part_id>/', views.assoc_part, name='assoc_part'),
    # Car Photo URL
    path('cars/<int:car_id>/add_photo/', views.add_photo, name='add_photo')
]