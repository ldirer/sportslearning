from __future__ import division


import datetime as datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase

from tennis_mockup.tennis.models import Match
from tennis_mockup.tennis.models import Player
from tennis_mockup.tennis.models import TennisPoint
from tennis_mockup.tennis.models import TennisShot
from tennis_mockup.tennis.views import get_zones

import numpy as np
import json
from nose.tools import assert_equal
from nose.tools import assert_set_equal
from tennis_mockup.tennis.views import apply_central_symmetry

#
# class TestPieChartData(TestCase):
#
# def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user('Roger', 'roger@rg.com', 'Roger')
#         self.user_2 = User.objects.create_user('Novak', 'novak@rg.com', 'Novak')
#         self.p1 = Player(name='Roger', user=self.user)
#         self.p2 = Player(name='Novak', user=self.user_2)
#         self.user.save()
#         self.user_2.save()
#         self.p1.save()
#         self.p2.save()
#
#
#         self.match = Match.objects.create(timestamp=datetime.datetime(year=2011, month=06,
#                                                                       day=03),
#                                           name="Roger Federer vs Novak Djokovic",
#                                           player_one=self.p1,
#                                           player_two=self.p2)
#         self.match.save()
#


# def test_forehand_backhand_split(self):
#     response = self.client.get(reverse(winners_split, args=[1]))
#     #print response.body
#     #print response.content
#     assert True

#
# class TestCalls(TestCase):
#     def test_call_view_denies_anonymous(self):
#         response = self.client.get('/url/to/view', follow=True)
#         self.assertRedirects(response, '/login/')
#         response = self.client.post('/url/to/view', follow=True)
#         self.assertRedirects(response, '/login/')
#
#     def test_call_view_loads(self):
#         self.client.login(username='user', password='test')  # defined in fixture or with factory in setUp()
#         response = self.client.get('/url/to/view')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'conversation.html')
#
#     def test_call_view_fails_blank(self):
#         self.client.login(username='user', password='test')
#         response = self.client.post('/url/to/view', {})  # blank data dictionary
#         self.assertFormError(response, 'form', 'some_field', 'This field is required.')
#         # etc. ...
#
#     def test_call_view_fails_invalid(self):
#
#     # as above, but with invalid rather than blank data in dictionary
#
#     def test_call_view_fails_invalid(self):
#         # same again, but with valid data, then
#         self.assertRedirects(response, '/contact/1/calls/')
#
#
#
#
#
# class ProcessAllTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#
#     def test_login_required(self):
#         response = self.client.get(reverse('process_all'))
#         self.assertRedirects(response, '/login')
#
#     def test_get_method(self):
#         self.client.login(username='john', password='johnpassword')
#         response = self.client.get(reverse('process_all'))
#         self.assertRedirects(response, '/reports/messages')
#
#         # assert no messages were sent
#
#     def test_post_method(self):
#         self.client.login(username='john', password='johnpassword')
#
#         # add pending messages, mock sms sending?
#
#         response = self.client.post(reverse('process_all'))
#         self.assertRedirects(response, '/reports/messages')


def test_apply_central_symmetry():
    x_grid = np.linspace(0, 10, num=3)
    y_grid = np.linspace(0, 10, num=6)
    zones = {}
    key_gen = ((x, y) for x in range(len(x_grid) + 1)
               for y in range(len(y_grid) + 1))
    for zone_x, zone_y in key_gen:
        zones[(zone_x, zone_y)] = 0

    zones[(1, 5)] = 7
    zones[(2, 1)] = 1
    zones[(1, 4)] = 3
    zones[(2, 2)] = 4
    zones[(1, 3)] = 10
    zones[(2, 3)] = 8

    zones = apply_central_symmetry(zones, x_grid, y_grid)
    half_court_keys = [(zone_x, zone_y)
                       for zone_x in range(len(x_grid) + 1)
                       for zone_y in range(
            int(np.ceil((len(y_grid) + 1) / 2)))]
    # Test that the keys are correct (the right zones have been removed).
    assert_set_equal(set(zones.keys()), set(half_court_keys))
    #Test that the numbers are right.
    assert_equal(zones[(2, 1)], 8)
    assert_equal(zones[(2, 2)], 7)
    assert_equal(zones[(1, 3)], 10)
    assert_equal(zones[(2, 3)], 8)


def test_zones():
    u_1 = User.objects.create(username='Laurent_test')
    p_1 = Player.objects.create(user=u_1, name='Laurent_test')
    u_2 = User.objects.create(username='Laurent_test_2')
    p_2 = Player.objects.create(user=u_2, name='Laurent_test_2')

    start_positions = [(0, 0)]
    end_positions = [(0.25, 0.17)]
    shot_types = ['F']
    special_shots = ['']
    tennis_points_id = [1]
    players = [1]

    Match.objects.create(id=1, player_one=p_1, player_two=p_2,
                         name='Test: Laurent vs Laurent',
                         timestamp=datetime.datetime.now())

    TennisPoint.objects.create(number=1,
                               player_serving=1,
                               player_scoring=1, id=1, match_id=1)
    shots_to_create = [
        TennisShot(
            start_position_x=start_positions[i][0],
            start_position_y=start_positions[i][1],
            end_position_x=end_positions[i][0],
            end_position_y=end_positions[i][1],
            shot_type=shot_types[i],
            special_shot=special_shots[i],
            player=players[i],
            timestamp=datetime.datetime.now(),
            tennis_point_id=tennis_points_id[i]
        )
        for i in range(len(start_positions))]

    TennisShot.objects.bulk_create(shots_to_create)
    zones_impact, zones_position = get_zones(TennisShot.objects.all())
    print zones_impact
    print zones_position
    assert_equal(zones_impact[(2, 1)], 1)


# def test_filter_shots():
#     n_shots = 10
#     start_positions = [(0.4, 0.4) for i in range(n_shots)]
#     end_positions = [(0.8, 0.8) for i in range(n_shots)]
#     shot_types = ['S', 'F', 'F', 'F', 'F', 'F', 'B', 'F', 'S', 'S']
#
#     TennisPoint.objects.create(number=1,
#                                player_serving=1,
#                                player_scoring=1,
#                                )
#
#     TennisShot.objects.bulk_create([
#         TennisShot(
#             start_position_x = start_positions[i][0],
#             start_position_y = start_positions[i][1],
#             end_position_y = end_positions[i][0],
#             end_position_y = end_positions[i][1],
#             shot_type = shot_types[i],
#             special_shot = special_shots[i],
#             player = players[i],
#             tennis_point_id = tennis_points[i]
#     )
#     for i in range(n_shots)])


def test_zone_serves():
    """
    Test that the zones returned for the serve positions are the right ones.
    :return:
    """
    with file('../../assets/own/js/test_service.json') as test_file:
        test_data = test_file.read()

    # SEEMS COMPLICATED TO IMPLEMENT. Next time the views should be better
    # organized so that they rely on functions that are testable instead of
    # putting the logic in a view that takes a request as argument and
    # returns an html response...


if __name__ == '__main__':
    import nose

    nose.runmodule()
