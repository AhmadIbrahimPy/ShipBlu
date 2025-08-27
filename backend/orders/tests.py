from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customer, Order, OrderTrackingEvent

class OrdersAPITests(APITestCase):

    def setUp(self):
        # Create a test customer
        self.customer = Customer.objects.create(
            name="Test Customer", phone_number="123456789"
        )

    # 1. Test creating a new order
    def test_create_order(self):
        data = {
            "tracking_number": "TRACK123",
            "customer_id": self.customer.id,
            "status": "CREATED"
        }
        response = self.client.post("/app/orders/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().tracking_number, "TRACK123")

    # 2. Test updating order with invalid status transition
    def test_invalid_status_transition(self):
        order = Order.objects.create(
            tracking_number="TRACK124", customer=self.customer, status="CREATED"
        )
        data = {"status": "DELIVERED"}  # Skip PICKED
        response = self.client.patch(f"/app/orders/{order.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid status transition", response.data["error"])

    # 3. Test updating order with valid status transition
    def test_valid_status_transition(self):
        order = Order.objects.create(
            tracking_number="TRACK125", customer=self.customer, status="CREATED"
        )
        data = {"status": "PICKED"}
        response = self.client.patch(f"/app/orders/{order.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, "PICKED")
        # Check that tracking event was created
        self.assertEqual(OrderTrackingEvent.objects.count(), 1)
        event = OrderTrackingEvent.objects.first()
        self.assertEqual(event.status, "PICKED")
        self.assertEqual(event.order.id, order.id)

    # 4. Test searching orders by tracking number
    def test_search_order_by_tracking_number(self):
        Order.objects.create(tracking_number="SEARCH123", customer=self.customer)
        response = self.client.get("/app/orders/?search=SEARCH123")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    # 5. Test filtering orders by status
    def test_filter_order_by_status(self):
        Order.objects.create(tracking_number="FILT1", customer=self.customer, status="CREATED")
        Order.objects.create(tracking_number="FILT2", customer=self.customer, status="PICKED")
        response = self.client.get("/app/orders/?status=CREATED")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['tracking_number'], "FILT1")

    # 6. Test deleting an order
    def test_delete_order(self):
        order = Order.objects.create(tracking_number="DEL123", customer=self.customer)
        response = self.client.delete(f"/app/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
