from django.shortcuts import render
from rest_framework import viewsets
from server.models import Server
from server.serializer import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from server.schema import server_list_docs


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

    @server_list_docs
    def list(self, request):
        """
        Retrieve a list of servers, filtered and annotated based on the provided query parameters.

        This method supports filtering by category name, user membership,
        specific server ID, and the number of members in each server. It also
        allows limiting the number of results returned.

        Args:
        - `category` (str, optional): Filter servers by category name.
        - `by_user` (bool, optional): If true, filters servers by the authenticated user membership.
        - `by_server_id` (int, optional): Filters a specific server by its ID.
        - `with_num_members` (bool, optional): If true, includes a count of members in each server.
        - `qty` (int, optional): Limits the number of servers returned.

        Returns:
        - Response: A JSON response containing a list of serialized server data.

        Raises:
        - AuthenticationFailed: If the user is not authenticated when filtering by user membership.
        - ValidationError: If the provided by_server_id is not a valid integer or the server is not found.

        Example:
        - GET /servers/?category=Games&by_user=true&with_num_members=true&qty=10
        - Returns a list of up to 10 servers in the "Games" category that the authenticated user is a member of, including the number of members in each server.
        """

        category = request.query_params.get("category")
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("by_server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"
        qty = request.query_params.get("qty")

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # A linha if by_user or by_server_id and not request.user.is_authenticated falha porque respeita a ordem de precedência dos operadores lógicos em Python: not > and > or. Assim, ela é avaliada como by_user or (by_server_id and not authenticated), o que pode permitir acesso mesmo com o usuário anônimo. Para corrigir, use parênteses:
        if (by_user or by_server_id) and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if by_server_id:
            try:
                server_id_int = int(by_server_id)
            except ValueError:
                raise ValidationError(
                    detail=f"Server id {by_server_id} must be an integer."
                )

            self.queryset = self.queryset.filter(id=server_id_int)
            if not self.queryset.exists():
                raise ValidationError(
                    detail=f"Server with id {server_id_int} not found."
                )

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if qty:
            self.queryset = self.queryset[: int(qty)]

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
