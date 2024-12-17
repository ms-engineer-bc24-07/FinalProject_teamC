# 飲み会希望条件関連ビュー

from api.models.participation_model import Participation as PartyPreference

# party_preference_controller.py が PartyPreference を必要とする場合、Participation モデルを代用
from api.models.user_profile_model import UserProfile
from django.http import JsonResponse

from ..services.venue_service import VenueService


def suggest_venue(request):
    preferences = PartyPreference.objects.filter(date="2024-12-10")  # 希望日の条件
    user_ids = preferences.values_list("user_id", flat=True)
    users = UserProfile.objects.filter(id__in=user_ids)

    coordinates = []
    for user in users:
        lat, lng = VenueService.get_coordinates(user.nearest_station)
        coordinates.append({"lat": lat, "lng": lng})

    midpoint = VenueService.calculate_midpoint(coordinates)
    venue_preference = preferences.first().venue_preference
    restaurants = VenueService.search_restaurants(midpoint, venue_preference)

    return JsonResponse({"suggested_restaurants": restaurants})
