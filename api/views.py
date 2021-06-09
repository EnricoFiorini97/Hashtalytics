import json
import env
from . import cron
from django.http import HttpResponse
from api.wrapper import TWrapper
from http import HTTPStatus
from api.errors import UnauthorizedUserRequestError
from django.views.decorators.http import require_http_methods


def __json_response(res, request):
    try:
        if "Authorization" not in request.headers or request.headers['Authorization'] != f"Bearer {env.MY_BEARER_TOKEN}":
            raise UnauthorizedUserRequestError()
        body = json.loads(res["body"])
        status = res["status"]
        if not isinstance(status, int):
            raise TypeError()
        return HttpResponse(
            json.dumps(body),
            headers={"Content-Type": "application/json"},
            status=status
        )
    except (ValueError, KeyError, TypeError):
        return HttpResponse(
            json.dumps({"message": "Server error: invalid response format"}),
            headers={"Content-Type": "application/json"},
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    except UnauthorizedUserRequestError as bad_auth:
         return HttpResponse(
            json.dumps({"message": f"Forbidden: {str(bad_auth)}"}),
            headers={"Content-Type": "application/json"},
            status=HTTPStatus.FORBIDDEN
        )

@require_http_methods(["GET"])
def display_user(request, user="twitter"):
    cron.tweets_warehouse(user)
    return __json_response(TWrapper().fetch_tweets(user=user), request)

@require_http_methods(["GET"])
def display_hashtag(request, hashtag="twitter"):
    cron.hashtags_warehouse(hashtag)
    return __json_response(TWrapper().fetch_hashtag(hashtag=hashtag), request)

@require_http_methods(["GET"])
def display_trends(request, c_id=23424853):
    return __json_response(TWrapper().fetch_trends(c_id), request)

@require_http_methods(["GET"])
def display_location(request, lat=44.5, lon=11.35, rad=5):
    return __json_response(TWrapper().fetch_location(lat, lon, rad), request)

@require_http_methods(["GET"])
def display_text(request, text="twitter"):
    return __json_response(TWrapper().fetch_text(text), request)

@require_http_methods(["GET"])
def display_timeline(request, user="@twitter"):
    return __json_response(TWrapper().fetch_timeline(user), request)