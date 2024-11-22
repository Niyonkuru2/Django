from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Property,Tenant,Lease,Unit

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta: 
        model=User
        fields=['id','first_name','last_name','username','email','password']
    
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model=Property
        fields=['id','name','address','property_type','description','number_of_unit','owner']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model=Unit
        fields=['id','property','unit_number','bedroom','bathromm','rent']

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tenant
        fields=['id','user_id','phone_number']

class LeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lease
        fields=['id','tenant','unit','start_date','end_date','rent_Ammount']
    