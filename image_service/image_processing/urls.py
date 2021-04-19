from django.urls import path

from . import views


app_name = 'processing'

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('resize_image/<int:image_id>/', views.resize_image, name='resize_image'),
]

