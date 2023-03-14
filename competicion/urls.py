from django.urls import path

from . import views

urlpatterns = [
    path('<int:comp_id>/', views.tabla, name='tabla'),
    path('', views.index, name='index'),

]