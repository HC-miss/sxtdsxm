# import jsonpickle


def my_user_info(request):
    user = request.session.get('user', None)
    # if s_user:
    #     user = jsonpickle.loads(s_user)
    return {'user': user}
