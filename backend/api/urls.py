from django.urls import path, include  # Include the include function
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from api import views

urlpatterns = [
    path("token/", views.MyTokenObtainedPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", views.RegisterView.as_view()),
    path("dashboard/", views.dashboard),
    path("login/", views.LoginAPIView.as_view()),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('barbershops/', views.list_barbershops, name='barbershop-list'),
    path('barbershops/create/<int:userId>/', views.create_barbershop, name='create_barbershop'),
    path('barbershops/<int:pk>/update/', views.update_barbershop, name='barbershop-update'),
    path('barbershops/<int:pk>/delete/', views.delete_barbershop, name='barbershop-delete'),
    path('barbershops/user/<int:user_id>/', views.get_barbershop_by_user, name='list_barbershops_by_user'),
    path('style-of-cut/<int:pk>/', views.StyleOfCutDetailView.as_view(), name='style-of-cut-detail'),
    path('<int:barbershop_id>/style-of-cut/create/', views.StyleOfCutCreateView.as_view(), name='style-of-cut-create'),
    path('barbershops/<int:barbershop_id>/style-of-cuts/', views.StyleOfCutListView.as_view(), name='style-of-cut-list'),
    path('appointment/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointment/create/', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('barbershops/<int:barbershop_id>/style-of-cuts/create-default-styles/', views.create_default_styles, name='create_default_styles'),

    
]