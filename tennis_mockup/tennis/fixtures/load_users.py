from django.contrib.auth.models import User

from tennis.models import Player


def create_basic_user_and_player(name):
    """Create and save a user with a name (no email or pw) and the associated
    player.
    """
    u = User.objects.create_user(name, email=None, password=name)
    p = Player(name=name, user=u)
    u.save()
    p.save()


create_basic_user_and_player('Foo')
create_basic_user_and_player('Bar')
create_basic_user_and_player('Roger')
create_basic_user_and_player('Novak')

su = User.objects.create_superuser('SU', email=None, password=None)
sp = Player(name='SU', user=su)
