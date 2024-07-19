
from django.urls import path
from .views import *

urlpatterns = [
    path('', homeView, name='homeView'),
    path('register/', registerView, name='registerView'),
    path('login/', loginView, name='loginView'),
    path('logout/', logoutView, name='logoutView'),
    path('schemas/', schemasView, name='schemasView'),
    path('editSchema/', editSchema, name='editSchema'),
    path('removeSchema/', removeSchema, name='removeSchema'),
    path('saveSchema/', saveSchema, name='saveSchema'),
    path('editTable/', editTable, name='editTable'),
    path('removeTable/', removeTable, name='removeTable'),
    path('saveTable/', saveTable, name='saveTable'),
    path('editField/', editField, name='editField'),
    path('removeField/', removeField, name='removeField'),
    path('saveField/', saveField, name='saveField'),
    path('editAssociation/', editAssociation, name='editAssociation'),
    path('removeAssociation/', removeAssociation, name='removeAssociation'),
    path('saveAssociation/', saveAssociation, name='saveAssociation'),
    path('downloadDatabase/', downloadView, name='downloadDatabase'),
    path('generateDatabase/', generateDatabase, name='generateDatabase'),
]