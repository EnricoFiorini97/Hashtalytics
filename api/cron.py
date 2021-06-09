import json
import sqlite3
from api.wrapper import TWrapper
from api.models import HashtagTrends, Tweet
from django.utils import timezone as tz
from django.db.utils import IntegrityError
from dateutil.parser import parse


def crono_trends() -> None: 
    try:
        tmp = json.loads(TWrapper().fetch_trends()['body'])
        for i in range(len(tmp[0]['trends'])):
            trends_hashtag = HashtagTrends(
                import_time=str(tz.now())[:13], 
                hashtag=tmp[0]['trends'][i]['name'], 
                url=tmp[0]['trends'][i]['url'], 
                tweet_volume=tmp[0]['trends'][i]['tweet_volume'])
            trends_hashtag.save()
            print(f"Progress: {i+1}/{len(tmp[0]['trends'])}")
            hashtags_warehouse(tmp[0]['trends'][i]['name'])
    except sqlite3.OperationalError:
        print("[WARNING] DB Locked. Data Fetching failed.")
    except IntegrityError:
        pass
    

def hashtags_warehouse(hashtag="#twitter") -> None:
        try:
            response = json.loads(TWrapper().fetch_hashtag(hashtag)['body'])
            for i in range(len(response['statuses'])):
                item = Tweet(
                    created_at=date_converter(response['statuses'][i]['created_at']),
                    text=response['statuses'][i]['text'].lower(),
                    id_hash=response['statuses'][i]['id'],
                    id_str=response['statuses'][i]['id_str'],
                    truncated=response['statuses'][i]['truncated'],
                    ent_hashtags=None,  #"".join((str(item['text']) + '\n') for item in response['statuses'][i]['entities']['hashtags']),
                    ent_symbols=if_exist(response['statuses'][i]['entities'],'symbols'),
                    ent_urls=if_exist(response['statuses'][i]['entities'],'urls'),
                    ent_media=if_exist(response['statuses'][i]['entities'],"media"),
                    metadata_iso_language_code=response['statuses'][i]['metadata']['iso_language_code'],
                    metadata_result_type=response['statuses'][i]['metadata']['result_type'],
                    source=response['statuses'][i]['source'],
                    in_reply_to_status_id=response['statuses'][i]['in_reply_to_status_id'],
                    in_reply_to_status_id_str=response['statuses'][i]['in_reply_to_status_id_str'],
                    in_reply_to_user_id=response['statuses'][i]['in_reply_to_user_id'],
                    in_reply_to_user_id_str=response['statuses'][i]['in_reply_to_user_id_str'],
                    in_reply_to_screen_name=response['statuses'][i]['in_reply_to_screen_name'],
                    user_id=response['statuses'][i]['user']['id'],
                    user_id_str=response['statuses'][i]['user']['id_str'],
                    user_name=response['statuses'][i]['user']['name'],
                    user_screen_name=response['statuses'][i]['user']['screen_name'].lower(),
                    user_location=response['statuses'][i]['user']['location'],
                    user_description=response['statuses'][i]['user']['description'],
                    user_url=response['statuses'][i]['user']['url'],
                    user_protected=response['statuses'][i]['user']['protected'],
                    user_followers_count=response['statuses'][i]['user']['followers_count'],
                    user_friends_count=response['statuses'][i]['user']['friends_count'],
                    user_listed_count=response['statuses'][i]['user']['listed_count'],
                    user_created_at=response['statuses'][i]['user']['created_at'],
                    user_favourites_count=response['statuses'][i]['user']['favourites_count'],
                    user_utc_offset=response['statuses'][i]['user']['utc_offset'],
                    user_time_zone=response['statuses'][i]['user']['time_zone'],
                    user_geo_enabled=response['statuses'][i]['user']['geo_enabled'],
                    user_verified=response['statuses'][i]['user']['verified'],
                    user_statuses_count=response['statuses'][i]['user']['statuses_count'],
                    user_lang=response['statuses'][i]['user']['lang'],
                    user_contributors_enabled=response['statuses'][i]['user']['contributors_enabled'],
                    user_is_translator=response['statuses'][i]['user']['is_translator'],
                    user_is_translation_enabled=response['statuses'][i]['user']['is_translation_enabled'],
                    user_profile_background_color=response['statuses'][i]['user']['profile_background_color'],
                    user_profile_background_image_url=response['statuses'][i]['user']['profile_background_image_url'],
                    user_profile_background_image_url_https=response['statuses'][i]['user']['profile_background_image_url_https'],
                    user_profile_background_tile=response['statuses'][i]['user']['profile_background_tile'],
                    user_profile_image_url=response['statuses'][i]['user']['profile_image_url'],
                    user_profile_image_url_https=response['statuses'][i]['user']['profile_image_url_https'],
                    user_profile_link_color=response['statuses'][i]['user']['profile_link_color'],
                    user_profile_sidebar_border_color=response['statuses'][i]['user']['profile_sidebar_border_color'],
                    user_profile_sidebar_fill_color=response['statuses'][i]['user']['profile_sidebar_fill_color'],
                    user_profile_text_color=response['statuses'][i]['user']['profile_text_color'],
                    user_profile_use_background_image=response['statuses'][i]['user']['profile_use_background_image'],
                    user_has_extended_profile=response['statuses'][i]['user']['has_extended_profile'],
                    user_default_profile=response['statuses'][i]['user']['default_profile'],
                    user_default_profile_image=response['statuses'][i]['user']['default_profile_image'],
                    user_following=response['statuses'][i]['user']['following'],
                    user_follow_request_sent=response['statuses'][i]['user']['follow_request_sent'],
                    user_notifications=response['statuses'][i]['user']['notifications'],
                    user_translator_type=response['statuses'][i]['user']['translator_type'],
                    user_withheld_in_countries=response['statuses'][i]['user']['withheld_in_countries'],
                    geo=response['statuses'][i]['geo'],
                    coordinates=response['statuses'][i]['coordinates'],
                    place=response['statuses'][i]['place'],
                    is_quote_status=response['statuses'][i]['is_quote_status'],
                    retweet_count=response['statuses'][i]['retweet_count'],
                    favorite_count=response['statuses'][i]['favorite_count'],
                    favorited=response['statuses'][i]['favorited'],
                    retweeted=response['statuses'][i]['retweeted'],
                    lang=response['statuses'][i]['lang'],
                )           
                item.save()
        except sqlite3.OperationalError:
            print("[WARNING] DB Locked. Data Fetching failed.")
        except IntegrityError:
            pass
        

def tweets_warehouse(user="@fedez") -> None:
    try:
        response = json.loads(TWrapper().fetch_tweets(user)['body'])
        for i in range(len(response[0])):
            item = Tweet(
                created_at=date_converter(response[i]['created_at']),
                text=response[i]['text'].lower(),
                id_hash=response[i]['id'],
                id_str=response[i]['id_str'],
                truncated=response[i]['truncated'],
                ent_hashtags="".join((str(item['text']) + '\n') for item in response[i]['entities']['hashtags']),
                ent_symbols=response[i]['entities']['symbols'],
                ent_urls=response[i]['entities']['urls'],
                ent_media=if_exist(response[i]['entities'],"media"),
                source=response[i]['source'],
                in_reply_to_status_id=response[i]['in_reply_to_status_id'],
                in_reply_to_status_id_str=response[i]['in_reply_to_status_id_str'],
                in_reply_to_user_id=response[i]['in_reply_to_user_id'],
                in_reply_to_user_id_str=response[i]['in_reply_to_user_id_str'],
                in_reply_to_screen_name=response[i]['in_reply_to_screen_name'],
                user_id=response[i]['user']['id'],
                user_id_str=response[i]['user']['id_str'],
                user_name=response[i]['user']['name'],
                user_screen_name=response[i]['user']['screen_name'].lower(),
                user_location=response[i]['user']['location'],
                user_description=response[i]['user']['description'],
                user_url=response[i]['user']['url'],
                user_protected=response[i]['user']['protected'],
                user_followers_count=response[i]['user']['followers_count'],
                user_friends_count=response[i]['user']['friends_count'],
                user_listed_count=response[i]['user']['listed_count'],
                user_created_at=response[i]['user']['created_at'],
                user_favourites_count=response[i]['user']['favourites_count'],
                user_utc_offset=response[i]['user']['utc_offset'],
                user_time_zone=response[i]['user']['time_zone'],
                user_geo_enabled=response[i]['user']['geo_enabled'],
                user_verified=response[i]['user']['verified'],
                user_statuses_count=response[i]['user']['statuses_count'],
                user_lang=response[i]['user']['lang'],
                user_contributors_enabled=response[i]['user']['contributors_enabled'],
                user_is_translator=response[i]['user']['is_translator'],
                user_is_translation_enabled=response[i]['user']['is_translation_enabled'],
                user_profile_background_color=response[i]['user']['profile_background_color'],
                user_profile_background_image_url=response[i]['user']['profile_background_image_url'],
                user_profile_background_image_url_https=response[i]['user']['profile_background_image_url_https'],
                user_profile_background_tile=response[i]['user']['profile_background_tile'],
                user_profile_image_url=response[i]['user']['profile_image_url'],
                user_profile_image_url_https=response[i]['user']['profile_image_url_https'],
                user_profile_link_color=response[i]['user']['profile_link_color'],
                user_profile_sidebar_border_color=response[i]['user']['profile_sidebar_border_color'],
                user_profile_sidebar_fill_color=response[i]['user']['profile_sidebar_fill_color'],
                user_profile_text_color=response[i]['user']['profile_text_color'],
                user_profile_use_background_image=response[i]['user']['profile_use_background_image'],
                user_has_extended_profile=response[i]['user']['has_extended_profile'],
                user_default_profile=response[i]['user']['default_profile'],
                user_default_profile_image=response[i]['user']['default_profile_image'],
                user_following=response[i]['user']['following'],
                user_follow_request_sent=response[i]['user']['follow_request_sent'],
                user_notifications=response[i]['user']['notifications'],
                user_translator_type=response[i]['user']['translator_type'],
                user_withheld_in_countries=response[i]['user']['withheld_in_countries'],
                geo=response[i]['geo'],
                coordinates=response[i]['coordinates'],
                place=response[i]['place'],
                is_quote_status=response[i]['is_quote_status'],
                retweet_count=response[i]['retweet_count'],
                favorite_count=response[i]['favorite_count'],
                favorited=response[i]['favorited'],
                retweeted=response[i]['retweeted'],
                lang=response[i]['lang'],
            )      
            item.save()     
    except sqlite3.OperationalError:
        print("[WARNING] DB Locked. Data Fetching failed.")
    except IntegrityError:
        pass
    except KeyError:
        print("[WARNING] Key Error, this should be dispaly when you search a protected user or inexistent user.")

def if_exist(attribute, field) -> str:
    try:
        return attribute[field]
    except Exception:
        return ""


def date_converter(str_date="Tue Jun 23 13:08:52 +0000 2020"):
    try:
        dt = parse(str_date)
        month = dt.month
        if month < 10:
            month = f"0{dt.month}"
        s = f"{dt.year}-{month}-{dt.day} {dt.time()}"
        return s
    except ValueError:
        return None
