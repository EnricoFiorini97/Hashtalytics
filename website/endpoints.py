import env


base_url = f"http://localhost:8000/twapi"


def get_location_url(lat, lng, rad):
    return f"{base_url}/location/{lat}/{lng}/{rad}"


def get_hashtag_url(hshtg):
    return f"{base_url}/hashtag/{hshtg}"


def get_user_url(usr):
    return f"{base_url}/user/{usr}"


def get_text_url(text):
    return f"{base_url}/text/{text}"


def get_trends_url():
    return f"{base_url}/trends"


def get_graphs_url():
    return f"{get_trends_url()}/graphics"

def get_timeline_url(usr):
    return f"{base_url}/timeline/{usr}"