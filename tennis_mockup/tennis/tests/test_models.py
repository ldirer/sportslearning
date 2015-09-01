__author__ = 'laurent'

from tennis_mockup.tennis.models import Match
from tennis_mockup.tennis.models import TennisPoint
from tennis_mockup.tennis.models import TennisShot

"""
Apparently:
Not a good idea to try to mock the database.
Use Factories instead. Or don't write these particular tests.
"""


def test_aces_from_field_and_method():
    """Test if the aces method of the match object gives the same results as
    filtering directly the shots using the serve_status field.
    """
    m = Match.objects.get(id=2)
    m.save()
    points = m.points.all()

    def qs_union(x, y):
        return x | y

    shots = reduce(qs_union, [p.shots.all() for p in points])
    aces_method_ids = set(p.id for p in m.aces())
    aces_attribute = shots.filter(serve_status=TennisShot.ACE)
    aces_attribute_ids = set(s.tennis_point_id for s in aces_attribute)
    assert(aces_method_ids == aces_attribute_ids)


def test_first_serves_from_field_and_method():
    """Test if the aces method of the match object gives the same results as
    filtering directly the shots using the serve_status field.
    """
    m = Match.objects.get(id=2)
    m.save()
    points = m.points.all()

    def qs_union(x, y):
        return x | y

    shots = reduce(qs_union, [p.shots.all() for p in points])

    first_serves_method_ids = set(p.id for p in m.first_serves())
    # The first_serves method gives only points for which the serve went in.
    first_serves_attribute = shots.filter(
        number=1, serve_status__in=[TennisShot.IN,
                                    TennisShot.ACE,
                                    TennisShot.WINNING_SERVE])
    aces_attribute_ids = set(s.tennis_point_id for s in first_serves_attribute)
    assert(first_serves_method_ids == aces_attribute_ids)

