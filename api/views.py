from django.http import HttpResponse
from api.wrapper import TWrapper
from django.views.decorators.http import require_http_methods
import json

def __json_response(res):
    try:
        body = res["body"]
        status = res["status"]
        json.loads(res["body"])
        if not isinstance(status, int):
            raise TypeError()
        return HttpResponse(
            body,
            headers={"Content-Type": "application/json"},
            status=status
        )
    except (ValueError, KeyError, TypeError):
        return HttpResponse(
            json.dumps({"message": "Server error: invalid response format"}),
            headers={"Content-Type": "application/json"},
            status=500
        )

@require_http_methods(["GET"])
def display_user(request, user="twitter"):
    return __json_response(TWrapper().fetch_tweets(user=user))

@require_http_methods(["GET"])
def display_hashtag(request, hashtag="twitter"):
    return __json_response(TWrapper().fetch_hashtag(hashtag=hashtag))

@require_http_methods(["GET"])
def display_trends(request, c_id=23424853):
    return __json_response(TWrapper().fetch_trends(c_id))

@require_http_methods(["GET"])
def display_location(request, lat=44.5, lon=11.35, rad=5):
    return __json_response(TWrapper().fetch_location(lat, lon, rad))

@require_http_methods(["GET"])
def display_text(request, text="twitter"):
    return __json_response(TWrapper().fetch_text(text))

@require_http_methods(["GET"])
def display_timeline(request, user="@twitter"):
    return __json_response(TWrapper().fetch_timeline(user))