from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('quotes', views.quotes),
    path('myaccount/<int:id_user>', views.edit),
    path('user/<int:id_user>', views.user),
    path('delete/<int:quote_id>', views.delete_quote),
    path('update/<int:quote_id>', views.update_quote),
]