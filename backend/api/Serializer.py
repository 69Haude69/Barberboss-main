from api.models import User, Profile , Barbershop,StyleOfCut,Appointment
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'address', 'role']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'image', 'verified']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        profile = user.profile
        token['full_name'] = profile.full_name
        token['username'] = user.username
        token['id'] = user.id
        token['email'] = user.email
        token['bio'] = profile.bio
        token['image'] = str(profile.image)
        token['verified'] = profile.verified
        token['role'] = user.role
        token['address'] = user.address 
        token['phone'] = user.phone 
        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True, required=True
    )
    phone = serializers.CharField(max_length=15, required=True)
    address = serializers.CharField(max_length=255, required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'phone', 'address', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # Remove 'password2' from validated_data
        user = User.objects.create_user(**validated_data)  # Create user with create_user method
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


# BarberShop
class BarbershopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barbershop
        fields = ['id', 'user_id', 'name', 'address'] 

class StyleOfCutSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleOfCut
        fields = ['id', 'barbershop', 'name', 'price']

class AppointmentSerializer(serializers.ModelSerializer):
    style_of_cut = StyleOfCutSerializer()  # Serializer for nested style_of_cut field

    class Meta:
        model = Appointment
        fields = ['id', 'barbershop', 'barber', 'customer', 'style_of_cut', 'date_time']
