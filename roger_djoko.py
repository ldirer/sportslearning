__author__ = 'laurent'

import datetime

from tennis.models import Match, Player
from django.contrib.auth.models import User

name_1 = 'Roger'
name_2 = 'Djoko'

u_1 = User.objects.create_user(name_1, email=None, password=name_1)
p_1 = Player(name=name_1, user=u_1)

u_2 = User.objects.create_user(name_2, email=None, password=name_2)
p_2 = Player(name=name_2, user=u_2)
u_1.save()
p_1.save()

u_2.save()
p_2.save()

m = Match.objects.create(timestamp=datetime.datetime(year=2011, month=6,
                                                     day=3, hour=16,
                                                     minute=00),
                         name="Roland Garros 2011 - " + name_1 + " contre " + name_2,
                         player_one=p_1, player_two=p_2)
m.save()