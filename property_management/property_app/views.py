from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import UserSerializer,PropertySerializer,UnitSerializer,LeaseSerializer
from .models import Property,Unit,Lease,Tenant

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        # generating JWT Token for authenticate user
        refresh= RefreshToken.for_user(user)
        return Response({
            'user':serializer.data,
            'refresh':str(refresh),
            'access':str(refresh.access_token),

        },status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# API to login user

@api_view(['POST'])
def login(request):
     user = get_object_or_404(User,username = request.data['username'])
     if not user.check_password(request.data['password']):
         return Response({"detail":"Not Found"},status=status.HTTP_404_NOT_FOUND)
     refresh= RefreshToken.for_user(user)
     return Response({
            'refresh':str(refresh),
            'access':str(refresh.access_token),

        },status=status.HTTP_200_OK)

#Api to interact with property model
# get all
@api_view(['GET'])
def get_allprop(request):
    users = Property.objects.all()
    serializer = PropertySerializer(users,many=True)
    return Response(serializer.data)

# add property
@api_view(['POST'])
def adding_propety(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    data=request.data
    data['owner'] = request.user.id 
    
    serializer = PropertySerializer(data=data)
    if serializer.is_valid():
        property = serializer.save()
        
        return Response({
            'message': 'Property added successfully',
            'property': PropertySerializer(property).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# single property
@api_view(['GET'])
def get_one_property(request, pk):
    try:
        property = Property.objects.get(pk=pk)
        serializer = PropertySerializer(property)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Property.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

# edit or delete     
@api_view(['PUT','DELETE'])
@permission_classes([IsAuthenticated])
def single_property(request, pk):
    try:
        property = Property.objects.get(pk=pk)
        if property.owner != request.user:
            return Response({"detail": "You are not the owner of this property"}
            , status=status.HTTP_401_UNAUTHORIZED)
    except Property.DoesNotExist:
        return Response({"detail": "Property not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = PropertySerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
         property.delete()
         return Response({"detail": "Property deleted."}, status=status.HTTP_204_NO_CONTENT)

# API Interact with Unity model

# get units api
@api_view(['GET'])
def get_allunits(request):
    units = Unit.objects.all()
    serializer = UnitSerializer(units,many=True)
    return Response(serializer.data)

# api to add unit
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adding_unit(request):
    serializer = UnitSerializer(data=request.data)
    if serializer.is_valid():
        property = serializer.validated_data.get('property')

        # Check if the authenticated user is the owner of the property
        if property.owner == request.user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"detail": "You are not authorized to add units to this property."},
                status=status.HTTP_403_FORBIDDEN
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 # get unit   
@api_view(['GET'])  
def get_one_unit(request, pk):
    try:
        unit = Unit.objects.get(pk=pk)
        serializer = UnitSerializer(unit)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Unit.DoesNotExist:
        return Response({"detail": "Unit not found."}, status=status.HTTP_404_NOT_FOUND)

# edit oe delete
@api_view(['PUT','DELETE'])
@permission_classes([IsAuthenticated])
def single_unit(request, pk):
    try:
        unit = Unit.objects.get(pk=pk)
        if unit.property.owner != request.user:
            return Response({"detail": "You are not allowed to access this Unit"}
            , status=status.HTTP_401_UNAUTHORIZED)
    except Unit.DoesNotExist:
        return Response({"detail": "Unit not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = UnitSerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
         unit.delete()
         return Response({"detail": "Unit deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# api interact with lease model
# get lease associated with tenant
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_leases_for_client(request):
    try:
        tenant = request.user
        leases = Lease.objects.filter(tenant=tenant)
        if not leases.exists():
            return Response({"detail": "No leases found for this client."}, status=status.HTTP_404_NOT_FOUND)
        serializer = LeaseSerializer(leases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Tenant.DoesNotExist:
        return Response({"detail": "Tenant not found."}, status=status.HTTP_404_NOT_FOUND)

#API To add lease 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adding_lease(request):
    data = request.data
    data['tenant'] = request.user.id 
    serializer = LeaseSerializer(data=data)

    if serializer.is_valid():
        try:
            
            unit_id = data['unit']
            unit = Unit.objects.get(id=unit_id)
            if unit.property.owner != request.user:
                return Response(
                    {"detail": "You are not the owner of this unit, so you cannot create a lease."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Save the lease if everything is valid
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Unit.DoesNotExist:
            return Response(
                {"detail": "The specified unit does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#API To edit or delete lease
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def lease_edit_or_delete(request, pk):
    try:
        lease = Lease.objects.get(pk=pk)
        unit = lease.unit
        if unit.property.owner != request.user:
            return Response({"detail": "You are not the owner of this unit, so you cannot modify or delete the lease."},
                            status=status.HTTP_403_FORBIDDEN)
        if request.method == 'PUT':
            serializer = LeaseSerializer(lease, data=request.data)
            if serializer.is_valid():
                serializer.save()  
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            lease.delete()
            return Response({"detail": "Lease deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    except Lease.DoesNotExist:
        return Response({"detail": "Lease not found."}, status=status.HTTP_404_NOT_FOUND)

