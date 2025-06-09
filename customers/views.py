from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from customers.models import Customer
from customers.serializers import CustomerListSerializer, CustomerSerializer

class CustomerListCreateView(generics.ListCreateAPIView):
    """
    HTTP Methods:
    - GET /api/customers/ → list all customers
    - POST /api/customers/ → create new customer
    """
    
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated] 
    
    # DRF Filters
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']     # ?search=john
    ordering_fields = ['created_at', 'name']  # ?ordering=-name
    ordering = ['-created_at']            # Default ordering

    def get_serializer_class(self):
        """
        Dynamic serializer selection:
        - GET requests: Use lighter CustomerListSerializer
        - POST requests: Use full CustomerSerializer
        This is more efficient than always using full serializer
        """
        if self.request.method == 'GET':
            return CustomerListSerializer
        return CustomerSerializer

    def get_queryset(self):
        """
        Override to add custom filtering
        Similar to Django's get_queryset() in views
        """
        queryset = Customer.objects.all()
        
        # Custom search (bonus requirement)
        search = self.request.query_params.get('search', None)
        if search:
            # Q objects for complex queries (OR condition)
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(email__icontains=search)
            )
        
        return queryset

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    HTTP Methods:
    - GET /api/customers/uuid/ → get single customer
    - PUT /api/customers/uuid/ → update customer
    - DELETE /api/customers/uuid/ → delete customer
    """
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  # Use 'id' field instead of default 'pk'

    def destroy(self, request, *args, **kwargs):
        """
        Override delete method to customize response
        Default would return 204 No Content
        We want to return 200 with success message
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Customer deleted successfully"}, 
            status=status.HTTP_200_OK
        )