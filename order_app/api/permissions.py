from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """
    Permission class for allowing only customer users to create orders.

    Methods:
        has_permission(request, view): Checks if user is authenticated and has customer profile.

    Args:
        request: HTTP request object
        view: View being accessed

    Returns:
        bool: True if user is customer type, False otherwise

    Raises:
        None
    """

    def has_permission(self, request, view):
        """
        Check if user has customer profile type.

        Args:
            request: HTTP request object
            view: View being accessed

        Returns:
            bool: True if user is authenticated and has customer profile

        Raises:
            None
        """
        if not request.user.is_authenticated:
            return False
        return self._is_customer(request.user)

    def _is_customer(self, user):
        """
        Check if user profile type is customer.

        Args:
            user: User object

        Returns:
            bool: True if user is customer

        Raises:
            None
        """
        try:
            return user.profile.type == 'customer'
        except AttributeError:
            return False


class IsBusinessUserForOrder(BasePermission):
    """
    Permission class for allowing only business users to update order status.

    Methods:
        has_object_permission(request, view, obj): Checks if user is business and owns the order.

    Args:
        request: HTTP request object
        view: View being accessed
        obj: Order object being accessed

    Returns:
        bool: True if user is business type and owns the order, False otherwise

    Raises:
        None
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if user is business user for the order.

        Args:
            request: HTTP request object
            view: View being accessed
            obj: Order object being accessed

        Returns:
            bool: True if user is business user for this order

        Raises:
            None
        """
        return self._is_business_and_owner(request.user, obj)

    def _is_business_and_owner(self, user, obj):
        """
        Check if user is business and is the business_user for the order.

        Args:
            user: User object
            obj: Order object

        Returns:
            bool: True if user is business and owns the order

        Raises:
            None
        """
        try:
            return user.profile.type == 'business' and obj.business_user == user
        except AttributeError:
            return False


class IsOrderParticipant(BasePermission):
    """
    Permission class for allowing only order participants to view orders.

    Methods:
        has_object_permission(request, view, obj): Checks if user is participant in the order.

    Args:
        request: HTTP request object
        view: View being accessed
        obj: Order object being accessed

    Returns:
        bool: True if user is participant in order, False otherwise

    Raises:
        None
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if user is customer or business user for the order.

        Args:
            request: HTTP request object
            view: View being accessed
            obj: Order object being accessed

        Returns:
            bool: True if user is part of this order

        Raises:
            None
        """
        return self._is_participant(request.user, obj)

    def _is_participant(self, user, obj):
        """
        Check if user is customer or business user for the order.

        Args:
            user: User object
            obj: Order object

        Returns:
            bool: True if user is part of this order

        Raises:
            None
        """
        return obj.customer_user == user or obj.business_user == user