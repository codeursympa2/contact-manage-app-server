from django.urls import path,include
from .views import updateContact,addContact,deleteContact,getContacts,getContactById,search_contact
from rest_framework import routers



urlpatterns = [
    path("", getContacts),
    path("add", addContact),
    path("delete/<int:pk>", deleteContact),
    path("update/<int:pk>", updateContact),
    path("<int:pk>/detail", getContactById),
    path("search", search_contact),
]