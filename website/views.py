from django.shortcuts import render
from .forms import MainForm
from django.views.decorators.http import require_http_methods
from website.endpoints import *

import requests
import json
import geocoder
import env


@require_http_methods(["GET", "HEAD"])
def home(request):
    form = MainForm()
    _, lst, _ = _get_trends(10)
    return render(request, 'home.html', {"form": form, "trends": lst})


@require_http_methods(["GET", "HEAD"])
def details(request):
    try:
        if (request.GET.get("hasher")[:1] == '@' or request.GET.get("hasher")[:1] == '#' or request.GET.get("hasher")[
                                                                                            :1] == '$'):
            tag = request.GET.get("hasher")[:1]
            hasher = request.GET.get("hasher")[1:]
        else:
            tag = None
            hasher = request.GET.get("hasher")
    except TypeError as e:
        # return _handleError(Error.INVALID_INPUT)
        return render(request, 'hashtag-details.html', {"error": "Invalid input"}, status=400)

    if tag == "#":
        url = get_hashtag_url(hasher)
        r = requests.get(url, headers={'Content-Type': 'application/json'})
        tweets = r.json().get("statuses")
        return render(request, 'hashtag-details.html', {"tweets": tweets, "hasher": hasher, "tag": tag}, status=200)

    if tag == "@":
        url = get_user_url(hasher)
        r = requests.get(url, headers={'Content-Type': 'application/json'})
        tweets = r.json()
        return render(request, 'details.html', {"tweets": tweets, "hasher": hasher, "tag": tag}, status=200)

    if tag == "$":
        return get_map(hasher, request)

    # Se il nome cercato non contiene ne una @ ne un #, oppure $, allora la ricerca viene eseguita per tutta la
    # lunghezza dell'hasher
    url = get_text_url(hasher)
    r = requests.get(url, headers={'Content-Type': 'application/json'})
    tweets = r.json().get("statuses")
    return render(request, 'text-details.html', {"tweets": tweets, "hasher": hasher, "tag": tag}, status=200)

    # errors = []

    # url = ""
    # if tag == "@":
    #     url = f'{api_url}/user/{hasher}/'
    # elif tag == "#":
    #     url = f'{api_url}/hashtag/{hasher}/'
    # else:
    #     errors.append({
    #         "message": "Input non valido, il primo carattere dovrebbe essere @ o #"
    #     })

    # tweets = {}
    # if len(url):
    #     try:
    #         r = requests.get(url, headers={'Content-Type': 'application/json'})

    #         tweets = r.json()
    #         if type(tweets) is dict and tweets.get("statuses"):
    #             tweets = tweets.get("statuses")
    #     except ValueError as e:
    #         errors.append({
    #             "message": "Richiesta non valida"
    #         })
    #     except requests.exceptions.RequestException:
    #         errors.append({
    #             "message": "Errore di connessione al server, riporvare più tardi"
    #         })
    # return render(request, 'details.html', {"tweets": tweets, "hasher": hasher, "tag": tag, "errors": errors})


@require_http_methods(["GET", "HEAD"])
def trends(request):
    _trnds, lst, count = _get_trends()
    return render(request, 'trends.html', {"trends": _trnds, "trends_list": lst, "trends_count": count})


def _get_trends(limit=50):
    try:
        url = get_trends_url()
        r = requests.get(url, headers={'Content-Type': 'application/json'})
        jsondata = r.json()
        jsondata = jsondata[0]
        jsondata.pop("locations", None)

        output = {
            'data': jsondata.get("trends")[:limit]
        }

        return json.dumps(output), output["data"], limit
    except ValueError:
        print("Decoding JSON has failed")


def geocoding(place):
    coords = geocoder.mapbox(place, key=env.MAPBOX_PUB_KEY).latlng
    # Più o meno gli angoli del quadrato di coordinate contenente l'Italia
    # Servono a filtrare posti chiaramente NON in Italia (e.g. Pechino)
    ws = [5.034216244956292, 35.940935243542505]
    en = [20.03421624495629, 47.5409352435425]

    if coords is None:
        return None
    else:
        coords = list(reversed(coords))
        if (en[0] >= coords[0] >= ws[0]) and (en[1] >= coords[1] >= ws[1]):
            return coords
        else:
            return None


def get_map(place, request):
    center = geocoding(place)
    return render(request, 'map.html',
                  {'center': json.dumps(center), 'valid': (center is not None),
                   'request_url_format': get_location_url("{0}", "{1}", "{2}"),
                   'token': env.MAPBOX_PUB_KEY}, status=200)


@require_http_methods(["GET", "HEAD"])
def graphics(request):
    return render(request, 'graphics.html', {"graphics": _get_graphics()})


def _get_graphics():
    url = get_graphics_url()
    return url
