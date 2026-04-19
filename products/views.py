from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    # Only allow GET for now (safe practice)
    http_method_names = ['get']

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']

    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset