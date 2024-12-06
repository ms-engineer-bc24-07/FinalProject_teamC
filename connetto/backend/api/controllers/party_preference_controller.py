# 飲み会希望条件関連ビュー

from api.models.party_preference_model import PartyPreference
from api.models.user_model import User
from django.http import JsonResponse

from ..services.venue_service import VenueService


def suggest_venue(request):
    preferences = PartyPreference.objects.filter(date="2024-12-10")  # 希望日の条件
    user_ids = preferences.values_list("user_id", flat=True)
    users = User.objects.filter(id__in=user_ids)

    coordinates = []
    for user in users:
        lat, lng = VenueService.get_coordinates(user.nearest_station)
        coordinates.append({"lat": lat, "lng": lng})

    midpoint = VenueService.calculate_midpoint(coordinates)
    venue_preference = preferences.first().venue_preference
    restaurants = VenueService.search_restaurants(midpoint, venue_preference)

    return JsonResponse({"suggested_restaurants": restaurants})
