from rest_framework import serializers
from .models import Customer, Order, OrderTrackingEvent

# Serializer for the Customer model
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer  # Link to Customer model
        fields = ["id", "name", "phone_number"]  # Include these fields in API responses

# Serializer for the Order model
class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)  # Nested read-only representation of customer
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),  # Allow selection of existing customer by ID
        source="customer",  # Map the input customer_id to the customer field
        write_only=True  # Accept this field only in requests, not in responses
    )

    class Meta:
        model = Order  # Link to Order model
        fields = [
            "id",
            "tracking_number",
            "customer",
            "customer_id",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]  # These fields cannot be modified by the client

    # Validate the status field to ensure only allowed values are used
    def validate_status(self, value):
        allowed = dict(Order.STATUS_CHOICES).keys()  # Get all valid status choices
        if value not in allowed:
            raise serializers.ValidationError("Invalid status value")
        return value

# Serializer for the OrderTrackingEvent model
class OrderTrackingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTrackingEvent  # Link to OrderTrackingEvent model
        fields = ["id", "order", "status", "timestamp", "comment"]  # Include these fields in API responses
        read_only_fields = ["id", "timestamp"]  # ID and timestamp are read-only
