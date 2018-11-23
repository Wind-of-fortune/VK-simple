import os

import requests as rq


def get_token(code):
    id = 6758982
    secret_key = os.environ.get('VkFriendsKey')
    redirect_url = 'http://127.0.0.1:8000/friends'

    url = 'https://oauth.vk.com/access_token?client_id={}&client_secret={}&redirect_uri={}&code={}' \
        .format(id, secret_key, redirect_url, code)
    r = rq.get(url)
    data = r.json()

    try:
        if data['error']:
            return [False, False, False]
    except Exception:
        pass

    token = str(data['access_token'])
    user_id = int(data['user_id'])
    token_lifetime = int(data['expires_in'])

    return token, user_id, token_lifetime


def get_user_info(token, user_id):
    url_user_info = "https://api.vk.com/method/users.get?uid={}&access_token={}&fields=first_name,last_name&v=5.92" \
        .format(user_id, token)

    r = rq.get(url_user_info)
    user_data = r.json()['response'][0]
    user_first_name = user_data['first_name']
    user_last_name = user_data['last_name']

    return user_first_name, user_last_name


def get_user_friends(token, user_id):
    def get_friends(token, user_id):
        url_user_friends = "https://api.vk.com/method/friends.get?uid={}&access_token={}" \
                           "&order=random&count=5&fields=first_name,last_name,last_seen&v=5.92"\
                         .format(user_id, token)

        r = rq.get(url_user_friends)
        all_friends = r.json()['response']['count']
        friends_list = r.json()['response']['items']
        user_friends = []
        for d in friends_list:
            friend_full_name = ''
            for key, val in d.items():
                if key == 'first_name':
                    friend_full_name += val + ' '
                if key == 'last_name':
                    friend_full_name += val + ' '
            friend_full_name = friend_full_name.strip()
            user_friends.append(friend_full_name)
        return user_friends, all_friends

    user_friends, all_friends = get_friends(token, user_id)
    user_friends = [i for i in user_friends if i != 'DELETED']  # checking for DELETED accounts
    counter = 0

    if all_friends > 5:
        while len(user_friends) < 5 and counter < 5:
            new_user_friends, _ = get_friends(token, user_id)
            for i in new_user_friends:
                if i != 'DELETED':
                    user_friends.append(i)
            print(user_friends)
            user_friends = set(user_friends)
            user_friends = list(user_friends)
            counter += 1
            while len(user_friends) > 5:
                user_friends.pop()

    return user_friends
