from rest_framework import serializers
from django.contrib.auth.models import User
from order_app.models import Order
from offer_app.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for order objects.

    Args:
        id (int): Order ID
        customer_user (User): Customer user
        business_user (User): Business user
        title (str): Order title
        revisions (int): Number of revisions
        delivery_time_in_days (int): Delivery time in days
        price (Decimal): Order price
        features (list): List of features
        offer_type (str): Offer type
        status (str): Order status
        created_at (datetime): Creation timestamp
        updated_at (datetime): Update timestamp

    Returns:
        Order: Serialized order data

    Raises:
        None
    """

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'created_at',
            'updated_at'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating orders from offer details.

    Args:
        offer_detail_id (int): ID of the offer detail to create order from

    Returns:
        Order: Created order instance

    Raises:
        ValidationError: If offer detail not found or invalid
    """

    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'offer_detail_id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'created_at',
            'updated_at'
        ]

    def validate_offer_detail_id(self, value):
        """
        Validate offer detail exists.

        Args:
            value (int): Offer detail ID

        Returns:
            int: Validated offer detail ID

        Raises:
            ValidationError: If offer detail not found
        """
        try:
            OfferDetail.objects.get(id=value)
        except OfferDetail.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound("Offer detail not found.")
        return value

    def create(self, validated_data):
        """
        Create order from offer detail.

        Args:
            validated_data (dict): Validated data containing offer_detail_id

        Returns:
            Order: Created order instance

        Raises:
            None
        """
        offer_detail_id = validated_data.pop('offer_detail_id')
        offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        order = self._create_order_from_detail(offer_detail, self.context['request'].user)
        return order

    def _create_order_from_detail(self, offer_detail, customer_user):
        """
        Create order instance from offer detail.

        Args:
            offer_detail (OfferDetail): Offer detail instance
            customer_user (User): Customer user

        Returns:
            Order: Created order instance

        Raises:
            None
        """
        return Order.objects.create(
            customer_user=customer_user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type
        )


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating order status.

    Args:
        status (str): New order status

    Returns:
        Order: Updated order instance

    Raises:
        ValidationError: If status is invalid
    """

    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        """
        Validate status value.

        Args:
            value (str): Status value to validate

        Returns:
            str: Validated status value

        Raises:
            ValidationError: If status is invalid
        """
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Choose from: {valid_statuses}")
        return value


class OrderCountSerializer(serializers.Serializer):
    """
    Serializer for order count responses.

    Args:
        order_count (int): Number of orders

    Returns:
        dict: Order count data

    Raises:
        None
    """

    order_count = serializers.IntegerField()


class CompletedOrderCountSerializer(serializers.Serializer):
    """
    Serializer for completed order count responses.

    Args:
        completed_order_count (int): Number of completed orders

    Returns:
        dict: Completed order count data

    Raises:
        None
    """

    completed_order_count = serializers.IntegerField()