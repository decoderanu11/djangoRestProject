from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # No authentication required for registration

    def create(self, request, *args, **kwargs):
        """
        Override create to customize response
        Default would just return user data
        We want to include JWT tokens for immediate login
        """
        # Validate and save user 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens - this is the JWT magic
        refresh = RefreshToken.for_user(user)
        
        # Return custom response with tokens
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'tokens': {
                'refresh': str(refresh),           # Long-lived token
                'access': str(refresh.access_token), # Short-lived token
            }
        }, status=status.HTTP_201_CREATED)