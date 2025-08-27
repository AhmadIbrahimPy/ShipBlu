from django.db import models

# Customer model
class Customer(models.Model):
    name = models.CharField(max_length=255)  # Customer's full name
    phone_number = models.CharField(max_length=20)  # Customer's phone number

    def __str__(self):
        return self.name  # Display customer's name as string representation

# Order model
class Order(models.Model):
    STATUS_CHOICES = [
        ("CREATED", "Created"),
        ("PICKED", "Picked"),
        ("DELIVERED", "Delivered"),
    ]  # Allowed status choices for an order

    tracking_number = models.CharField(max_length=100, unique=True)  # Unique tracking number
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer_order"
    )  # Link to customer; delete orders if customer is deleted
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="CREATED"
    )  # Current status with default
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Auto-update on every save

    def __str__(self):
        return f"{self.tracking_number} - {self.status}"  # Show tracking number and status

# OrderTrackingEvent model
class OrderTrackingEvent(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tracking_events"
    )  # Link to order; delete events if order is deleted
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)  # Status at this event
    comment = models.TextField(blank=True, null=True)  # Optional comment for the event
    timestamp = models.DateTimeField(auto_now_add=True)  # Event creation timestamp

    def __str__(self):
        return f"{self.order.tracking_number} - {self.status} at {self.timestamp}"
        # Show tracking number, status, and timestamp
