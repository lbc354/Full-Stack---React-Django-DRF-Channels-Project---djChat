from django.shortcuts import render
from rest_framework import viewsets
from server.models import Server
from server.serializer import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from server.schema import server_list_docs


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """
        GET /api/server/select/

        Retrieve a list of servers with optional filters and annotations.

        This endpoint supports query parameters to filter servers by category,
        limit the number of results, include member counts, or filter by user/server ID.
        Authentication is required for filters involving user-specific or private data.

        Query Parameters:
            category (str, optional): Filter servers by category name.
                Example: `/api/server/select/?category=Gaming`

            qty (str, optional): Limit the number of returned servers.
                Example: `/api/server/select/?qty=5`

            by_user (str, optional): If "true", return servers where the current user is a member.
                Requires authentication.
                Example: `/api/server/select/?by_user=true`

            by_server_id (str, optional): Filter by a specific server ID.
                Requires authentication.
                Example: `/api/server/select/?by_server_id=42`

            with_num_members (str, optional): If "true", include `num_members` in each server's data.
                Example: `/api/server/select/?with_num_members=true`

        Returns:
            Response: A JSON array of serialized servers. If `with_num_members=true`,
            each server includes a `num_members` field representing the total number of members.

        Raises:
            AuthenticationFailed: If unauthenticated user tries to filter by user or server ID.
            ValidationError: If `by_server_id` is not an integer or does not exist.

        Examples:
            - List all servers:
                GET /api/server/select/

            - Filter by category:
                GET /api/server/select/?category=Education

            - Limit to 5 results:
                GET /api/server/select/?qty=5

            - Servers for the authenticated user:
                GET /api/server/select/?by_user=true

            - Get server by ID:
                GET /api/server/select/?by_server_id=42

            - Include number of members:
                GET /api/server/select/?with_num_members=true
        """
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_server_id = request.query_params.get("by_server_id")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if (by_user or by_server_id) and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if with_num_members:
            self.queryset = self.queryset.annotate(
                num_members=Count("member")
            )  # The annotate() method in Django is used to add aggregate values (such as counts) to each item in the queryset. Unlike aggregate(), it does not group data but adds a new field to each returned object.

        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_server_id} not found."
                    )
            except ValueError:
                raise ValidationError(detail=f"{by_server_id} is not a valid value.")

        if qty:
            self.queryset = self.queryset[
                : int(qty)
            ]  # Limits the number of results returned (similar to SQL's LIMIT clause).

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
