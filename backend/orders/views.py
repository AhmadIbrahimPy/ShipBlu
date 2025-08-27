from django_filters.rest_framework import DjangoFilterBackend  # Import backend for filtering querysets
from rest_framework.pagination import PageNumberPagination  # Import pagination for splitting list responses into pages
from rest_framework import viewsets, status, \
    filters  # Import viewsets (for CRUD endpoints), HTTP status codes, and filters (Search, Ordering)
from rest_framework.response import Response  # Import Response for custom HTTP responses
from .serializers import *  # Import all serializers for the app models

# Define pagination class specifically for CustomerViewSet
class CustomerPagination(PageNumberPagination):
    page_size = 10  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow clients to set page size via query parameter
    max_page_size = 50  # Maximum number of items allowed per page

# CustomerViewSet provides full CRUD operations for Customer model
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by("-id")  # Fetch all customers, newest first
    serializer_class = CustomerSerializer  # Serializer handles converting model instances to JSON and vice versa

    # Enable filtering, searching, and ordering in list endpoints
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ["id", "name", "phone_number"]  # Fields clients can filter by using ?field=value
    search_fields = ["name", "phone_number"]  # Fields clients can search with ?search=keyword
    ordering_fields = ["id", "name"]  # Fields clients can order results by ?ordering=field
    pagination_class = CustomerPagination  # Apply pagination to this ViewSet so results are returned page by page

# OrderViewSet provides full CRUD operations for Order model
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")  # Get all orders, newest first
    serializer_class = OrderSerializer  # Use OrderSerializer for JSON conversion

    # Enable filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "customer"]  # Allow filtering by order status and customer
    search_fields = ["tracking_number", "customer__name"]  # Allow search by tracking number or customer name
    ordering_fields = ["created_at", "updated_at", "status"]  # Allow ordering by creation/update date or status
    pagination_class = CustomerPagination  # Apply pagination to this ViewSet so results are returned page by page

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)  # Check if it's a partial update (PATCH) or full update (PUT)
        instance = self.get_object()  # Get the order instance being updated
        new_status = request.data.get("status")  # Get the new status from the request

        if new_status:  # If status is provided, validate the transition
            valid_transitions = {
                "CREATED": ["PICKED"],
                "PICKED": ["DELIVERED"],
                "DELIVERED": [],  # No transitions allowed after delivered
            }

            # Return an error if the new status is not a valid transition
            if new_status not in valid_transitions.get(instance.status, []):
                return Response(
                    {"error": f"Invalid status transition from {instance.status} to {new_status}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Log the status change in OrderTrackingEvent
            OrderTrackingEvent.objects.create(
                order=instance,
                status=new_status,
                comment=f"Status changed from {instance.status} to {new_status}"
            )

        # Call the parent update method to save the order changes
        return super().update(request, *args, partial=partial, **kwargs)

# OrderTrackingEventViewSet provides full CRUD operations for OrderTrackingEvent model
class OrderTrackingEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderTrackingEvent.objects.all().order_by("-timestamp")  # Get all tracking events, newest first
    serializer_class = OrderTrackingEventSerializer  # Use serializer to convert data to/from JSON
    pagination_class = CustomerPagination  # Apply pagination to this ViewSet so results are returned page by page
