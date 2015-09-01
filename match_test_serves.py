import datetime

from tennis.models import Match
from tennis.utils import create_villemoisson_player


name_1 = 'Test_service_1'
name_2 = 'Test_service_2'

p_1 = create_villemoisson_player(name_1)
p_2 = create_villemoisson_player(name_2)

m = Match.objects.create(timestamp=datetime.datetime(year=2014, month=8,
                                                     day=13, hour=16,
                                                     minute=50),
                         name="Test_service",
                         player_one=p_1, player_two=p_2)
m.save()