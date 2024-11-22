from django.urls import path
from . import views

urlpatterns = [
path('user/registering',views.register,name='register'),
path('user/login',views.login,name='login'),

path('property/adding',views.adding_propety,name='adding_propety'),
path('property/get_all',views.get_allprop,name='get_allprop'),
path('property/single/<int:pk>',views.get_one_property,name='get_one_property'),
path('property/<int:pk>',views.single_property,name='single_property'),

path('unit/adding',views.adding_unit,name='adding_unit'),
path('unit/get_all',views.get_allunits,name='get_allunits'),
path('unit/single/<int:pk>',views.get_one_unit,name='get_one_unit'),
path('unit/<int:pk>',views.single_unit,name='single_unit'),

path('lease/adding',views.adding_lease,name='adding_lease'),
path('lease/get_all',views.get_leases_for_client,name='get_leases_for_client'),
path('lease/<int:pk>',views.lease_edit_or_delete,name='lease_edit_or_delete')

]
