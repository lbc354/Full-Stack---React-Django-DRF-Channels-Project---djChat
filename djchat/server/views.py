from django.shortcuts import render
from rest_framework import viewsets
from server.models import Server
from server.serializer import ServerSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
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
            )  # O método annotate() no Django é usado para adicionar valores agregados (cálculos) a cada item individual do queryset. Ele não agrupa os dados como o aggregate() faz — ele apenas anexa um novo campo a cada objeto retornado.

        if qty:
            self.queryset = self.queryset[
                : int(qty)
            ]  # Limita o número de resultados retornados (como LIMIT no SQL).

        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_server_id} not found."
                    )
            except ValueError:
                raise ValidationError(detail=f"{by_server_id} is not a valid value.")

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
