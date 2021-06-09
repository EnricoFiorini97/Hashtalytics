import env
import geocoder
import json
import requests

from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView

from .endpoints import get_graphs_url, get_hashtag_url, get_text_url, get_trends_url, get_user_url, \
    get_timeline_url
from .forms import MainForm
from .models import UserProfile


@require_http_methods(["GET", "HEAD"])
def home(request):
    try:
        form = MainForm()
        _, lst, _ = _get_trends(10)
        _, trends_cloud, _ = _get_trends(50)

        user_trends = []
        if (user := request.user).is_authenticated:
            func = (lambda t: str(t).lower().replace("#", "").replace("@", ""))

            user_words = [func(w) for w in _user_keywords(user)]
            user_trends = [t for t in trends_cloud if user_words.count(func(t["name"])) > 0][0:10]

        return render(request, 'home.html',
                      {"form": form, "trends": lst, "trends_cloud": trends_cloud, "user_trends": user_trends})
    except TypeError:
        return error_response(request)


def error_response(request, msg="I nostri servizi non sono momentaneamente disponibili ):", status=500):
    return render(request, 'error.html', {"error": msg}, status=status)


@require_http_methods(["GET", "HEAD"])
def details(request):
    hasher_query = request.GET.get("hasher")
    tag = None
    hasher = hasher_query
    try:
        if hasher_query[:1] in ['@', '#', '$']:
            tag = hasher_query[:1]
            hasher = hasher_query[1:]
    except TypeError:
        # TODO: valutare se sostituire con un redirect alla home
        return render(request, 'details.html', {"error": "Input non valido"}, status=400)

    if tag == "#":
        try:
            url = get_hashtag_url(hasher)
            r = requests.get(url, headers={'Content-Type': 'application/json',
                                           'Authorization': f"Bearer {env.MY_BEARER_TOKEN}"})
            res_obj = r.json()
            hashtag_response = res_obj.get("statuses")
            error_code = res_obj.get("error")
            status = r.status_code
            if isinstance(hashtag_response, list) and len(hashtag_response) == 0:
                return render(request, 'details.html',
                              {"error": 'Non ho trovato nessun tweet con questo hashtag', "hasher": hasher, "tag": tag},
                              status=status)
            if error_code == 'INVALID_HASHTAG':
                return render(request, 'details.html', {"error": 'Hashtag non valido', "hasher": hasher, "tag": tag},
                              status=status)
            return render(request, 'details.html',
                          {"tweets": hashtag_response, "hasher": hasher, "tag": tag, "error": error_code},
                          status=status)
        except KeyError as e:
            error = e.args[0]
            return render(request, 'details.html', {"error": error, "hasher": hasher, "tag": tag}, status=500)
    if tag == "@":
        url = get_user_url(hasher)
        r = requests.get(url,
                         headers={'Content-Type': 'application/json', 'Authorization': f"Bearer {env.MY_BEARER_TOKEN}"})
        user_response = r.json()
        status = r.status_code
        if isinstance(user_response, dict) and user_response.get('error'):
            return render(request, 'details.html',
                          {"error": 'Utente non trovato, riprova con un altro nome utente', "hasher": hasher,
                           "tag": tag}, status=status)
        if isinstance(user_response, list) and len(user_response) == 0:
            return render(request, 'details.html',
                          {"error": 'Non ho trovato nessun tweet per questo utente', "hasher": hasher, "tag": tag},
                          status=404)
        t_url = get_timeline_url(hasher)
        timeline = requests.get(t_url, headers={'Content-Type': 'application/json', 'Authorization': f"Bearer {env.MY_BEARER_TOKEN}"})
        return render(request, 'details.html', {"tweets": user_response, "hasher": hasher, "tag": tag, "has_timeline": timeline.status_code == 200 }, status=status)
    elif tag == "$":
        tags = get_map(hasher, request)
        return render(request, 'map.html', tags, status=200)
    else:
        # Se il nome cercato non contiene un tag valido (#,@, o $), allora la ricerca viene eseguita per tutta la
        # lunghezza dell'hasher
        url = get_text_url(hasher)
        r = requests.get(url,
                         headers={'Content-Type': 'application/json', 'Authorization': f"Bearer {env.MY_BEARER_TOKEN}"})
        res_obj = r.json()
        text_response = res_obj.get("statuses")
        error_code = res_obj.get("error")
        status = r.status_code
        if isinstance(text_response, list) and len(text_response) == 0:
            return render(request, 'details.html',
                          {"error": 'Testo non trovato, riprova con un altro testo', "hasher": hasher, "tag": tag},
                          status=status)
        if error_code == 'INVALID_TEXT':
            return render(request, 'details.html',
                          {"error": 'Non ho trovato nessun tweet contenente questo testo', "hasher": hasher,
                           "tag": tag}, status=404)
        return render(request, 'details.html', {"tweets": text_response, "hasher": hasher, "tag": ""}, status=200)


@require_http_methods(["GET", "HEAD"])
def trends(request):
    try:
        _trnds, lst, count = _get_trends()
        return render(request, 'trends.html', {"trends": _trnds, "trends_list": lst, "trends_count": count})
    except TypeError:
        return error_response(request)


def _get_trends(limit=50):
    try:
        url = get_trends_url()
        r = requests.get(url,
                         headers={'Content-Type': 'application/json', 'Authorization': f"Bearer {env.MY_BEARER_TOKEN}"})
        jsondata = r.json()
        if isinstance(jsondata, dict) and jsondata.get('error'):
            raise TypeError()
        jsondata = jsondata[0]
        jsondata.pop("locations", None)

        output = {
            'data': jsondata.get("trends")[:limit]
        }

        return json.dumps(output), output["data"], limit
    except ValueError:
        print("Decoding JSON has failed")


@require_http_methods(["GET", "HEAD"])
def check_word_trending(request, word):
    _, lst, _ = _get_trends()

    if _word_trending(word, lst):
        return HttpResponse("Yes", status=200)
    else:
        return HttpResponse("No", status=404)


def _word_trending(word, trnds):
    func = (lambda t: str(t).lower().replace("#", "").replace("@", ""))
    word = func(word)

    return [func(t["name"]) for t in trnds].count(word) > 0


def geocoding(place):
    result = geocoder.mapbox(place, key=env.MAPBOX_PUB_KEY)
    coords = result.latlng

    if coords is None:
        return None
    else:
        if result.country == "Italy":
            return list(reversed(coords))
        else:
            return None


def get_map(place, request):
    center = geocoding(place)
    return {'center': json.dumps(center), 'place': place, 'valid': (center is not None),
            'auth': f"Bearer {env.MY_BEARER_TOKEN}", 'token': env.MAPBOX_PUB_KEY}


@require_http_methods(["GET", "HEAD"])
def profile(request):
    if (user := request.user).is_anonymous:
        return error_response(request, msg="Accesso non consentito", status=403)

    words = _user_keywords(user)

    trending = []
    if len(words) > 0:
        _, lst, _ = _get_trends()
        trending = [l['name'] for l in lst if words.count(l['name']) > 0]

    return render(request, 'profile.html', {"words": json.dumps(words), "trending": json.dumps(trending)}, status=200)


def _user_keywords(user_obj):
    words = []

    try:
        words = user_obj.userprofile.keywords
    except Exception:
        UserProfile.objects.create(user=user_obj, keywords=[])

    return words


@require_http_methods(["POST"])
def set_keywords(request):
    if (user := request.user).is_anonymous:
        return error_response(request, msg="Accesso non consentito", status=403)

    body = json.loads(request.body.decode("UTF-8"))

    try:
        UserProfile.objects.filter(user=user).update(keywords=body)
    except Exception:
        return error_response(request)

    return HttpResponse(status=200)


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/user_create.html'
    success_url = reverse_lazy('website-home')


@require_http_methods(["GET", "HEAD"])
def timeline(request, user):
    url = get_timeline_url(user)
    r = requests.get(url,
                     headers={'Content-Type': 'application/json', 'Authorization': f"Bearer {env.MY_BEARER_TOKEN}"})
    user_response = r.json()
    return render(request, 'timeline.html', {"tweets": user_response, "hasher": user})
