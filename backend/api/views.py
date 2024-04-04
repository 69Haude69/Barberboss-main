from django.shortcuts import render, get_object_or_404
from api.models import User, Profile , Barbershop,StyleOfCut,Appointment
from .Serializer import UserSerializer, MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer , LoginSerializer,BarbershopSerializer,StyleOfCutSerializer,AppointmentSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status ,permissions , viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class MyTokenObtainedPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == "GET":
        response = f"Hey {request.user}, you are getting a response"
        return Response({'response': response}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        text = request.POST.get("text")
        response = f"Hey {request.user}, your text is {text}"
        return Response({'response': response}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Authenticate the user
            user = authenticate(request, email=email, password=password)

            if user:
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Return tokens
                return Response({'access': access_token}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
 

@api_view(['POST'])
def create_barbershop(request, userId):
    request_data = request.data.copy() 
    request_data['user'] = userId

    serializer = BarbershopSerializer(data=request_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_barbershops(request):
    queryset = Barbershop.objects.all()
    serializer = BarbershopSerializer(queryset, many=True)
    return Response(serializer.data)
@api_view(['PUT'])
def update_barbershop(request, pk):
    barbershop = get_object_or_404(Barbershop, pk=pk)
    serializer = BarbershopSerializer(barbershop, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_barbershop(request, pk):
    barbershop = get_object_or_404(Barbershop, pk=pk)
    barbershop.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_barbershop_by_user(request, user_id):
    try:
        barbershop = Barbershop.objects.filter(user_id=user_id)
        serializer = BarbershopSerializer(barbershop,many=True)
        return Response(serializer.data)
    except Barbershop.DoesNotExist:
        return Response({'error': 'Barbershop not found'}, status=404)
    
class StyleOfCutDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StyleOfCut.objects.all()
    serializer_class = StyleOfCutSerializer

class StyleOfCutCreateView(generics.CreateAPIView):
    queryset = StyleOfCut.objects.all()
    serializer_class = StyleOfCutSerializer

class StyleOfCutListView(generics.ListCreateAPIView):
    serializer_class = StyleOfCutSerializer

    def get_queryset(self):
        # Get the barbershop_id from URL query parameters
        barbershop_id = self.kwargs['barbershop_id']
        # Filter StyleOfCut instances based on barbershop_id
        return StyleOfCut.objects.filter(barbershop_id=barbershop_id)
    
class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
@api_view(['POST'])
def create_default_styles(request, barbershop_id):
    try:
        barbershop = Barbershop.objects.get(id=barbershop_id)
        StyleOfCut.create_default_styles(barbershop)
        return Response({'message': 'Default styles created successfully.'}, status=200)
    except Barbershop.DoesNotExist:
        return Response({'message': 'Barbershop not found.'}, status=404)
    except Exception as e:
        return Response({'message': f'Error creating default styles: {str(e)}'}, status=500)