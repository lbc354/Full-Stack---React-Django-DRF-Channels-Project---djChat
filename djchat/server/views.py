from django.shortcuts import render
from rest_framework import viewsets
from server.models import Server
from server.serializer import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count


class ServerListViewSet(viewsets.ViewSet):
    """
    A viewset that provides the list of servers with optional filtering and
    additional information. Supports filtering by category, user membership,
    server ID, and adding member counts. Optionally limits the number of results.

    Methods:
        list(request):
            Handles GET requests to retrieve a list of servers based on various filters.
    """

    queryset = Server.objects.all()

    def list(self, request):
        """
        Retrieve a list of servers, filtered and annotated based on the provided query parameters.

        This method supports filtering by category name, user membership,
        specific server ID, and the number of members in each server. It also
        allows limiting the number of results returned.

        Args:
            request (Request): The HTTP request object containing query parameters.
                - `category` (str, optional): Filter servers by category name.
                - `by_user` (bool, optional): If true, filters servers by the authenticated user membership.
                - `by_server_id` (int, optional): Filters a specific server by its ID.
                - `with_num_members` (bool, optional): If true, includes a count of members in each server.
                - `qty` (int, optional): Limits the number of servers returned.

        Returns:
            Response: A JSON response containing a list of serialized server data.

        Raises:
            AuthenticationFailed: If the user is not authenticated when filtering by user membership.
            ValidationError: If the provided `by_server_id` is not a valid integer or the server is not found.

        Example:
            GET /servers/?category=Games&by_user=true&with_num_members=true&qty=10
            Returns a list of up to 10 servers in the "Games" category that the authenticated user is a member of,
            including the number of members in each server.
        """

        category = request.query_params.get("category")
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("by_server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"
        qty = request.query_params.get("qty")

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed()

        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_server_id} not found."
                    )
            except ValueError:
                raise ValidationError(
                    detail=f"Server id {by_server_id} must be an integer."
                )

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if qty:
            self.queryset = self.queryset[: int(qty)]

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
