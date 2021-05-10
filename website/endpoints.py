base_url = "http://127.0.0.1:8000/twapi"


def get_location_url(lat, lng, rad):
    return base_url + f"/location/{lat}/{lng}/{rad}"


def get_hashtag_url(hshtg):
    return base_url + f"/hashtag/{hshtg}"


def get_user_url(usr):
    return base_url + f"/user/{usr}"


def get_text_url(text):
    return base_url + f"/text/{text}"


def get_trends_url():
    return base_url + "/trends"


def get_graphics_url():
    return get_trends_url() + "/graphics"
