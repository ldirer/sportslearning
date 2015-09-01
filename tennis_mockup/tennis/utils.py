from django.contrib.auth.models import User
from tennis.models import Player


def create_villemoisson_player(name):
    """Create a user with the given name and a player associated with it.

    Returns the newly created player instance.
    :param name: name of the user and player created.
    :return:
    """
    name_list = name.split(' ')
    if len(name_list) == 1:
        pw = (name_list[0] + 'v').lower()
    else:
        pw = (name_list[0][0] + name_list[1]).lower()
    print pw
    u = User.objects.create_user(name, email=None, password=pw)
    p = Player(name=name, user=u)
    u.save()
    p.save()
    return p
