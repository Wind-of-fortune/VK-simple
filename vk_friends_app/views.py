from django.shortcuts import render, redirect

from vk_friends_app.extra_functions import *


def first_view(request):
    if str((request.get_full_path())).find('logout') != -1:
        try:
            request.session.delete_test_cookie()
        except KeyError:
            print('Already logout')

    if request.session.test_cookie_worked():
        return redirect('https://oauth.vk.com/authorize?client_id=6758982&display=page&'
                        'redirect_uri=http://127.0.0.1:8000/friends&'
                        'scope=friends&response_type=code&v=5.92')
    else:
        return render(request, 'vk_friends_app/button.html')


def friends_list(request):
    code = str(request.get_full_path()).split('?code=')[-1] # get code for token

    token, user_id, token_lifetime = get_token(code)
    if not token:
        return redirect('/')

    user_first_name, user_last_name = get_user_info(token, user_id)
    username = user_first_name + ' ' + user_last_name
    f_list = get_user_friends(token, user_id)

    request.session.set_test_cookie()

    data = {'user': username,
            'friends': f_list}

    return render(request,'vk_friends_app/friends.html', data)
