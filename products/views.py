from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.cache import cache
import time
import logging

logger = logging.getLogger(__name__)


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
        import json

        cache_key = "products_all"

        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info("CACHE HIT")
            print("FROM CACHE")

            return Product.objects.filter(id__in=cached_data).order_by('-created_at')

        logger.info("DB HIT")
        print("FROM DB")

        queryset = super().get_queryset()

        # apply filters
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # IMPORTANT: store IDs only
        ids = list(queryset.values_list('id', flat=True))

        cache.set(cache_key, ids, timeout=60)

        return queryset