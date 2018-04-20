"""
views.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  carolynwichers

Expose user models through a REST API.
"""
from rest_framework.serializers import ModelSerializer, UUIDField, SlugRelatedField, SerializerMethodField
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from users.models import DraughtPicksUser
from .models import Beer, BeerRating, RecentBeer, RecommendedBeer


class BeerSerializer(ModelSerializer):
    uuid = UUIDField()

    class Meta:
        model = Beer
        fields = ('uuid', 'name', 'description', 'abv', 'ibu', 'api_id', 'name_of_api', 'created_at',)


class BeerRatingSerializer(ModelSerializer):
    user = SlugRelatedField(slug_field='uuid', queryset=DraughtPicksUser.objects.all())
    beer = SlugRelatedField(slug_field='uuid', queryset=Beer.objects.all())
    uuid = UUIDField(read_only=True)

    class Meta:
        model = BeerRating
        fields = ('uuid', 'user', 'beer', 'rating', 'description', 'created_at',)


class BeerWithRatingSerializer(BeerSerializer):
    """
    Serializer to include the rating by the given user.
    """
    rating = SerializerMethodField()

    def __init__(self, instance, user=None, **kwargs):
        self.user = user
        super().__init__(instance, **kwargs)

    def get_rating(self, obj):
        req = self.context.get('request')
        ratings = []
        if self.user:
            ratings = BeerRating.objects.filter(beer=obj, user=self.user)
        elif req:
            ratings = BeerRating.objects.filter(beer=obj, user=req.user)
        return BeerRatingSerializer(ratings, many=True).data

    class Meta:
        model = Beer
        fields = ('uuid', 'rating', 'name', 'description', 'abv', 'ibu', 'api_id', 'name_of_api', 'created_at',)


class BeerSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BeerWithRatingSerializer
    queryset = Beer.objects.all()
    lookup_field = 'uuid'
    search_fields = ("name", )
    filter_backends = (SearchFilter, )


class BeerRatingSet(CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = BeerRatingSerializer
    queryset = BeerRating.objects.all()
    lookup_field = 'uuid'

    def create(self, request, *args, **kwargs):
        request.data['user'] = str(request.user.uuid)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        return BeerRating.objects.filter(user=self.request.user)


class RecentBeerSerializer(ModelSerializer):
    uuid = UUIDField(read_only=True)
    user = SlugRelatedField(slug_field='uuid', queryset=DraughtPicksUser.objects.all())
    beer = SlugRelatedField(slug_field='uuid', queryset=Beer.objects.all())

    class Meta:
        model = RecentBeer
        fields = ('uuid', 'user', 'beer', 'created_at',)


class BeerWithRecentSerializer(BeerWithRatingSerializer):
    recents = SerializerMethodField()

    def get_recents(self, obj):
        req = self.context.get('request')
        recent = []
        if self.user:
            recents = RecentBeer.objects.filter(beer=obj, user=self.user)
            #self.user.recent_beers.filter()
        elif req:
           recents = RecentBeer.objects.filter(beer=obj, user=req.user)
           # req.user.recent_beers.filter(beer=obj)
        return RecentBeerSerializer(recents, many=True).data

    class Meta:
        model = Beer
        fields = ('uuid', 'rating', 'name', 'description', 'abv', 'ibu', 'api_id', 'name_of_api', 'created_at', 'recents')


class RecentBeerSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = RecentBeerSerializer
    queryset = RecentBeer.objects.all()
    lookup_field = 'uuid'

    def get_queryset(self):
        return RecentBeer.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['user'] = str(request.user.uuid)
        return super().create(request, *args, **kwargs)

    def list(self, request, *arg, **kwargs):
        """
        Override to serialize the beers and not the through table.
        :param request:
        :param arg:
        :param kwargs:
        :return:
        """
        qs = self.request.user.recent_beers.order_by('-created_at')
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = BeerWithRecentSerializer(page, user=request.user, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BeerWithRecentSerializer(qs, user=request.user, many=True)
        return Response(serializer.data)


class RecommendedBeerSet(ListModelMixin, GenericViewSet):
    serializer_class = BeerWithRatingSerializer
    queryset = Beer.objects.all()
    lookup_field = 'uuid'

    def get_queryset(self):
        ids = self.request.user.recommendedbeer_set.values_list('id',flat=True)
        return Beer.objects.filter(name__contains='Bud').order_by('-name') #Beer.objects.filter(pk__in=ids)
