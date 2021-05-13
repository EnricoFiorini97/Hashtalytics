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
    hasherQuery = request.GET.get("hasher")
    tag = None
    hasher = hasherQuery
    try:
        if hasherQuery[:1] in ['@','#','$']:
            tag = hasherQuery[:1]
            hasher = hasherQuery[1:]
    except TypeError:
        # TODO: valutare se sostituire con un redirect alla home
        return render(request, 'details.html', {"error": "Input non valido"}, status=400)

    if tag == "#":
        try:
            url = get_hashtag_url(hasher)
            r = requests.get(url, headers={'Content-Type': 'application/json'})
            res_obj = r.json()
            tweets = res_obj.get("statuses")
            error_code = res_obj.get("error")

            # la risposta deve avere dentro i tweets, oppure un errore se non ha
            # nessuna delle due cose è successo qualcosa di inaspettato e ritorniamo 500
            if not error_code and not tweets:
                raise KeyError("Errore del sistema, contattare il supporto clienti")

            status = r.status_code
            error = error_code # TODO: scrivere un messaggio carino di errore in base all'error_code
            return render(request, 'hashtag-details.html', {"tweets": tweets, "hasher": hasher, "tag": tag, "error": error}, status=status)
        except KeyError as e:
            error = e.args[0]
            return render(request, 'hashtag-details.html', {"error": error, "hasher": hasher, "tag": tag}, status=500)

    if tag == "@":
        url = get_user_url(hasher)
        r = requests.get(url, headers={'Content-Type': 'application/json'})
        tweets = r.json()
        return render(request, 'details.html', {"tweets": tweets, "hasher": hasher, "tag": tag}, status=200)
    elif tag == "$":
        tags = get_map(hasher, request)
        return render(request, 'map.html', tags, status=200)
    else:
        # Se il nome cercato non contiene un tag valido (#,@, o $), allora la ricerca viene eseguita per tutta la
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
    ws = [6.61666667, 35.48333333]
    en = [18.51666667, 47.08333333]

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
    return {'center': json.dumps(center), 'place': place, 'valid': (center is not None),
            'request_url_format': get_location_url("{0}", "{1}", "{2}"),
            'token': env.MAPBOX_PUB_KEY}


@require_http_methods(["GET", "HEAD"])
def graphs(request):
    return render(request, 'graphs.html', {"graphs": _get_graphs()})


def _get_graphs():
    url = get_graphs_url()
    return url
