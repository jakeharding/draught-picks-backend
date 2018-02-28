"""
views.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  carolynwichers

Expose user models through a REST API.
"""

from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny

from .models import Beer, BeerRating, RecentBeer


class BeerSerializer(ModelSerializer):
    class Meta:
        model = Beer
        fields = ('uuid', 'name', 'description', 'abv', 'ibu', 'api_id', 'name_of_api', 'created_at',)


class BeerSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
    lookup_field = 'uuid'
    permission_classes = (AllowAny, )


class BeerRatingSerializer(ModelSerializer):
    class Meta:
        model = BeerRating
        fields = ('uuid', 'user', 'beer', 'rating', 'description', 'created_at',)


class BeerRatingSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BeerRatingSerializer
    queryset = BeerRating.objects.all()
    lookup_field = 'uuid'
    permission_classes = (AllowAny, )


class RecentBeerSerializer(ModelSerializer):
    class Meta:
        model = RecentBeer
        fields = ('uuid', 'user', 'beer', 'created_at',)


class RecentBeerSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = RecentBeerSerializer
    queryset = RecentBeer.objects.all()
    lookup_field = 'uuid'
    permission_classes = (AllowAny, )
