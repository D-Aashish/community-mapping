import json
from rest_framework import generics
from .serializers import ParkSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import Park, ParkDescription


from rest_framework.decorators import api_view

from django.shortcuts import render

class ParkListCreateAPIView(generics.ListCreateAPIView):
    queryset = Park.objects.all()
    serializer_class = ParkSerializer

    def get_queryset(self):
        return Park.objects.all()

@api_view(['GET'])
def park_locations(request):
    park=Park.objects.values('latitude','longitude')
    context={'park':park}
    return render(request, 'mapping/index.html', context)


def location(request):
    parks = Park.objects.values('name', 'id','latitude', 'longitude')
    point = [
        park for park in parks
        if park['latitude'] is not None and park['longitude'] is not None
        and -90 <= park['latitude'] <= 90
        and -180 <= park['longitude'] <= 180
    ]
    context = {'point': point}
    return render(request, 'mapping/index.html', context)

# @csrf_exempt  # Temporarily disable CSRF for simplicity (use proper CSRF handling in production)
@api_view(['POST'])
def add_park(request):
        try:
            data = request.data
            print("This is the data", data)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            # park = Marker.objects.create(latitude=lat, longitude=lng)

            park = Park.objects.create(
                name=f"Park at {latitude}, {longitude}",
                latitude=latitude,
                longitude=longitude
            )
            description_text = data.get('description', '')
            ParkDescription.objects.create(park=park, description=description_text)
            return JsonResponse({'message': 'Park added successfully', 'id': park.id}, status=201)
        except Exception as e:
            return JsonResponse({'error in add': str(e)}, status=500)

@api_view(['DELETE'])
def delete_park(request, park_id):
    # if request.method == 'DELETE':
        try:
            park = Park.objects.get(id=park_id)
            park.delete()
            return Response({'message': 'Park deleted successfully'}, status=status.HTTP_200_OK)
        except Park.DoesNotExist:
            return Response({'error': 'Park not found'}, status=status.HTTP_404_NOT_FOUND)
    # return JsonResponse({'error': 'Invalid method'}, status=400)

# @csrf_exempt
@api_view(['PUT'])
def edit_park(request, park_id):
    # if request.method == 'PUT':
        try:
            park = Park.objects.get(id=park_id)

            newlatitude = request.data.get('latitude')
            newlongitude = request.data.get('longitude')

            if newlatitude is None or newlongitude is None:
             return Response({'error': 'Missing coordinates'}, status=status.HTTP_400_BAD_REQUEST)

            park.latitude = newlatitude
            park.longitude = newlongitude
            park.save()

            return Response({'park id received'}, status=status.HTTP_200_OK)
        
        except Park.DoesNotExist:
         return Response({'error': 'Park not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"An exception occurred: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
def park_description(request,park_id):
        try: 
            park = Park.objects.get(id=park_id)
            description = ParkDescription.objects.get(Park=park)

            data = {
            'description': description.description,
            'address': description.address,
            'phone': description.phone,
            'email': description.email,
            'image_url': description.image.url if description.image else None
        }
        except ParkDescription.DoesNotExist:
            data = None
  
        # return render(request, 'mapping/indexx.html')
        return JsonResponse({'success': True, 'data': data})


def create_park_description(request, park_id):
    try:
        park = Park.objects.get(id=park_id)
    except Park.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid park ID'}, status=404)

    if ParkDescription.objects.filter(Park=park).exists():
        return JsonResponse({'success': False, 'error': 'Description already exists'}, status=400)

    data = json.loads(request.body)
    desc = ParkDescription.objects.create(
        Park=park,
        description=data.get('description', ''),
        address=data.get('address', ''),
        phone=data.get('phone', ''),
        email=data.get('email', ''),
    )
    return JsonResponse({'success': True, 'message': 'Description added'})

# def signup_view(request):
#     if request.method == "POST":
#         email = request.POST["email"]
#         password = request.POST["password"]

#         user = User.objects.create_user(email=email, password=password)
#         login(request, user)   # auto login after signup

#         return redirect("home")

#     return render(request, "signup.html")
def map(request):
    return render(request, 'mapping/map.html')