# -*- coding: utf-8 -*-
from __future__ import division

import numpy as np

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db.models import Q

from models import Match, StatsBoard
from django.forms.models import model_to_dict
from api import PointsFiltered, ShotsFiltered
import json
# Create your views here.


from functools import wraps
import jsonpickle

from django.shortcuts import get_object_or_404, resolve_url
from django.shortcuts import redirect
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from models import Match, Player, TennisPoint, TennisShot

from api import ShotsFiltered, PointsFiltered


def user_can_see_match(user, match):
    player = get_object_or_404(Player, user=user)
    return player in [match.player_one, match.player_two]


def forehand_backhand_split(qs):
    """Return a list of 2 dicts that can be dumped into json to create
    pie_chart graphs.

    Takes a queryset of points as input.
    """
    misrecorded = qs.annotate(
        n_shot_types=Count('shots__shot_type', distinct=True)).filter(
        n_shot_types=0)

    qs = qs.exclude(pk__in=misrecorded)
    shot_type_count = [
        {
            'key': 'Coups Droits',
            'y': sum([point.shots.last().shot_type == 'F'
                      for point in qs])
        },
        {
            'key': 'Revers',
            'y': sum([point.shots.last().shot_type == 'B'
                      for point in qs])
        }
    ]
    return shot_type_count


class ListMatchesByUser(ListView):
    model = Match

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListMatchesByUser, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        # Overwrite the method from views.generic.list.MultipleObjectMixin
        user = self.request.user
        player = get_object_or_404(Player, user=user)
        qs = (self.model.objects.filter(player_one=player) |
              self.model.objects.filter(player_two=player))

        return qs


@login_required
def dashboard(request, match_id):
    """
    Display graphs about the match, all data is related to the user only.
    First version includes 4 graphs:
      - Winners split between forehand/backhand
      - Unforced split between forehand/backhand
      - 1st serve split between returned/errors/not returned
      - 2nd serve split between returned/errors/not returned
    :param request:
    :param match_id:
    :return:
    """
    match = Match.objects.get(id=match_id)
    request.user.nav_state = "dashboard"
    return render(request, 'tennis/dashboard.html', locals())


@login_required
def winners_split(request, match_id):
    # TODO: add serves returned/out/not returned for 1st and 2nd serve.
    match = get_object_or_404(Match, id=match_id)
    if user_can_see_match(request.user, match):
        # Since there won't be any filtering in the graphs, we can process
        # the data here and not in js.
        user_player_bool = (match.player_one == get_object_or_404(
            Player, user=request.user))
        points = match.points.all()

        # TODO: write tests??

        winners_and_aces = points.filter(conclusion='W',
                                         player_scoring=user_player_bool)
        # aces = match.aces()
        # winners = winners_and_aces.exclude(pk__in=aces)

        winners_shot_type_count = forehand_backhand_split(winners_and_aces)
        return HttpResponse(json.dumps(winners_shot_type_count))


@login_required
def unforced_split(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if user_can_see_match(request.user, match):
        # Since there won't be any filtering in the graphs, we can process
        # the data here and not in js.
        user_player_bool = (match.player_one == get_object_or_404(
            Player, user=request.user))
        points = match.points.all()

        unforced_and_doubles = points.filter(
            conclusion='U', player_scoring=not user_player_bool)
        unforced_shot_type_count = forehand_backhand_split(
            unforced_and_doubles)
        return HttpResponse(json.dumps(unforced_shot_type_count))


@login_required
def first_serve_split(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if user_can_see_match(request.user, match):
        # Since there won't be any filtering in the graphs, we can process
        # the data here and not in js.
        user_player_bool = (match.player_one == get_object_or_404(
            Player, user=request.user))

        first_serves_in = match.first_serves().filter(
            player_serving=user_player_bool)

        # The serve is a winning one if it is an ace or if the opposite player
        # makes an error on the return. That means a winning 1st serve is a
        # point that is won by the player with less than 2 shots.
        # WARNING: We cannot annotate again the queryset, this is an
        # official Django bug (https://code.djangoproject.com/ticket/10060).
        # The following gives wrong results:
        # n_first_winning = match.first_serves().filter(
        # player_serving=user_player_bool,
        # player_scoring=user_player_bool,
        # ).annotate(n_shots=Count('shots__shot_type', distinct=False)).filter(
        # n_shots__lte=2).count()

        n_first_winning = sum([point.shots.count() < 3
                               for point in match.first_serves().filter(
                player_serving=user_player_bool,
                player_scoring=user_player_bool)
        ])

        # The number of first serves out is the number of 2nd serves played.
        n_first_out = match.second_serves().filter(
            player_serving=user_player_bool).count()
        first_serve_split_json = [
            {
                'key': 'Services gagnants',
                'y': n_first_winning
            },
            {
                'key': 'Fautes',
                'y': n_first_out
            },
            {
                'key': u'Services retournés',
                'y': first_serves_in.count() - n_first_winning
            }
        ]
        return HttpResponse(json.dumps(first_serve_split_json))


@login_required
def second_serve_split(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if user_can_see_match(request.user, match):
        # Since there won't be any filtering in the graphs, we can process
        # the data here and not in js.
        user_player_bool = (match.player_one == get_object_or_404(
            Player, user=request.user))

        second_serves = match.second_serves().filter(
            player_serving=user_player_bool)

        n_doubles = match.doubles().filter(
            player_serving=user_player_bool).count()

        # WARNING: We cannot annotate again the queryset, this is an
        # official Django bug (https://code.djangoproject.com/ticket/10060).
        # Following gives wrong results:
        # n_second_winning = second_serves.filter(
        # player_scoring=user_player_bool
        # ).annotate(n_shots=Count('shots', distinct=False)).filter(
        # n_shots__lte=3).count()

        n_second_winning = sum([point.shots.count() < 4
                                for point in match.second_serves().filter(
                player_serving=user_player_bool,
                player_scoring=user_player_bool)
        ])

        second_serve_split_json = [
            {
                'key': 'Services gagnants',
                'y': n_second_winning
            },
            {
                'key': 'Doubles Fautes',
                'y': n_doubles
            },
            {
                'key': u'Services retournés',
                'y': second_serves.count() - n_second_winning - n_doubles
            }
        ]
        return HttpResponse(json.dumps(second_serve_split_json))


@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if user_can_see_match(request.user, match):
        try:
            player_one_global_stats = get_object_or_404(
                StatsBoard, id=match.player_one_global_stats.id)
            player_two_global_stats = get_object_or_404(
                StatsBoard, id=match.player_two_global_stats.id)
        except AttributeError:
            match.save()
            player_one_global_stats = get_object_or_404(
                StatsBoard, id=match.player_one_global_stats.id)
            player_two_global_stats = get_object_or_404(
                StatsBoard, id=match.player_two_global_stats.id)

        (int_board_key_values_list,
         float_board_key_values_list) = player_one_global_stats.sorted_board_two_players(
            player_two_global_stats)
        # fields_names = model_to_dict(player_one_global_stats)
        shot_type_verbose_names = json.dumps(
            dict(TennisShot.SHOT_TYPE_CHOICES))
    else:
        return redirect(to='../')
    request.user.nav_state = "stats"
    context_dict = {
        'user': request.user,
        'match': match,
        'int_board_key_values_list': int_board_key_values_list,
        'float_board_key_values_list': float_board_key_values_list,
        'SHOT_TYPE_CHOICES': TennisShot.SHOT_TYPE_CHOICES,
        'shot_type_verbose_names': shot_type_verbose_names
    }
    return render(request, 'tennis/pie_chart.html', context_dict)


@login_required
def shot_type_count(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    points = match.points.all()
    shots = [shot for p in points.all() for shot in p.shots.all()]
    shot_types = [shot.shot_type for shot in shots]
    response_shot_type_count = {}
    for shot_type, pretty_shot_type in TennisShot.SHOT_TYPE_CHOICES:
        response_shot_type_count[pretty_shot_type] = shot_types.count(
            shot_type)
    return HttpResponse(json.dumps(response_shot_type_count))


@login_required
def forehands(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    points = match.points.all()
    shots = [shot for p in points.all() for shot in p.shots.all()]
    shot_types = [shot.shot_type for shot in shots]
    response_shot_type_count = {}
    for shot_type, pretty_shot_type in TennisShot.SHOT_TYPE_CHOICES:
        response_shot_type_count[pretty_shot_type] = shot_types.count(
            shot_type)
    return HttpResponse(json.dumps(response_shot_type_count))


def position_grid(grid, y):
    try:
        y_zone = [(y - y_ref) < 0 for y_ref in grid].index(True)
    except ValueError:
        y_zone = len(grid)
    return y_zone


def zones_from_grid(x_grid, y_grid, shots_coordinates):
    """
    Returns a dict with tuples as key representing the zones ((0, 0) is bottom
    left zone) and number of shots in the zone as values.
    Central symmetry is applied so that only keys referring to half-a-court
    remain.

    :param x_grid:
    :param y_grid:
    :param shots_coordinates:
    :return:
    """
    zones = dict()
    key_gen = ((x, y) for x in range(len(x_grid) + 1)
               for y in range(len(y_grid) + 1))
    for zone_x, zone_y in key_gen:
        zones[(zone_x, zone_y)] = 0

    for x, y in shots_coordinates:
        zones[(position_grid(x_grid, x),
               position_grid(y_grid, y))] += 1

    zones = apply_central_symmetry(zones, x_grid, y_grid)
    return zones


class CourtUsedInRecording:
    """
    Notes: we took the same padding for the court drawn on the site and in
    the tennis_logger.
    `width` is the width of the court ALONE. The width of the image used is
    thus `width + 2 * padx`.
    """

    def __init__(self):
        self.cw = 36
        self.ch = 78
        self.width = 200
        self.height = self.width * (self.ch / self.cw)
        # padding was 30 - 45 in the app.
        self.padx = 0.15 * self.width
        self.pady = 0.225 * self.width
        self.container_width = self.width + 2 * self.padx

    def scale_x(self, x):
        return x * (self.width + 2 * self.padx)

    def unscale_x(self, x):
        return float(x) / self.container_width

    def scale_y(self, y):
        return y * (self.height + 2 * self.pady)

    def unscale_y(self, y):
        return float(y) / (self.height + 2 * self.pady)

    def x_grid_inplay(self):
        """
        Return the grid along the x axis for the zones we want to display for
        regular shots (inplay = not serves).
        Includes a tolerance on the line position that is due to the mark of
        the ball not being a single point: if the ball touches the border of
        a line it is still in.
        The tolerance depends on parameters used in tennis_logger: the ball
        shape there was elliptic (10, 8) and included a 2px-wide border that
        is considered out.
        Dimensions of the court were (553, 292).
        """
        x_tolerance = 5.0 / 553
        x_left = self.unscale_x(self.padx + (4.5 / 36) * self.width)
        x_mid = 0.5
        x_right = self.unscale_x(self.width + self.padx - (4.5 / 36) * 200)
        x_grid = [x_left - x_tolerance, x_mid, x_right + x_tolerance]
        return x_grid

    def y_grid_inplay(self):
        """Return the grid along the y-axis for the zones we want to display.

        See `x_grid_inplay` for more details.
        """
        y_tolerance = 3. / 292
        y_bottom = self.unscale_y(self.pady)
        y_serve_bottom = self.unscale_y(
            self.pady + (self.ch / 2 - 21) * self.height / self.ch)
        y_close_net_down = 0.48
        y_close_net_up = 0.52
        y_serve_top = 0.5 + self.unscale_y((21 / self.ch) * self.height)
        y_top = 1 - self.pady / self.height

        y_grid = [y_bottom - y_tolerance, y_serve_bottom - y_tolerance,
                  y_close_net_down,
                  y_close_net_up,
                  y_serve_top + y_tolerance, y_top + y_tolerance]
        return y_grid

    def x_grid_serve(self):
        """Return the grid along the x-axis for the zones we want to display
        for serves.
        """
        x_tolerance = 5.0 / 553
        x_left = (self.padx / self.container_width +
                  (4.5 / 36) * self.width / self.container_width)
        x_mid = 0.5
        # x_right: 1 is the whole width, that is twice the padding and the two
        # alleys. We want only one padding and one alley. Hence:
        x_right = (1 - self.padx / self.container_width -
                   (4.5 / 36) * self.width / self.container_width)
        # We further split the serve zones in 3:
        serve_zone_ratio = 0.2
        x_zone_left_left = x_left + (x_mid - x_left) * serve_zone_ratio
        x_zone_left_right = x_left + (x_mid - x_left) * (1 - serve_zone_ratio)
        x_zone_right_left = x_right + (x_mid - x_right) * serve_zone_ratio
        x_zone_right_right = (x_right +
                              (x_mid - x_right) * (1 - serve_zone_ratio))

        x_grid = [x_left - x_tolerance,
                  x_zone_left_left,
                  x_zone_left_right,
                  x_mid - x_tolerance,
                  x_mid + x_tolerance,
                  x_zone_right_left,
                  x_zone_right_right,
                  x_right + x_tolerance]
        return x_grid

    def y_grid_serve(self):
        """Return the grid along the y-axis for the zones we want to display
        for serves.
        """
        y_tolerance = 3. / 292
        y_serve_bottom = self.unscale_y(
            self.pady + (self.ch / 2 - 21) * self.height / self.ch)
        y_close_net_down = 0.48
        y_close_net_up = 0.52
        y_serve_top = 0.5 + self.unscale_y(
            (21 / self.ch) * self.height)

        y_grid = [y_serve_bottom - y_tolerance,
                  y_close_net_down,
                  y_close_net_up,
                  y_serve_top + y_tolerance]
        return y_grid


def get_zones(shots):
    court = CourtUsedInRecording()
    x_grid = court.x_grid_inplay()
    y_grid = court.y_grid_inplay()

    impact_positions = [(shot.end_position_x, 1 - shot.end_position_y)
                        for shot in shots]

    placement_positions = [(shot.start_position_x, 1 - shot.start_position_y)
                           for shot in shots]

    zones_impact = zones_from_grid(x_grid, y_grid, impact_positions)
    zones_position = zones_from_grid(x_grid, y_grid, placement_positions)

    return zones_impact, zones_position


def get_zones_serve(serves):
    court = CourtUsedInRecording()
    x_grid = court.x_grid_serve()
    y_grid = court.y_grid_serve()

    impact_positions = [(serve.end_position_x, 1 - serve.end_position_y)
                        for serve in serves]

    zones_impact = zones_from_grid(x_grid, y_grid, impact_positions)
    return zones_impact


def apply_central_symmetry(zones, x_grid, y_grid):
    """Apply central symmetry to a zones dictionary.

    Remove tuple keys that represent zones on the upper half of the court and
    make sure that the values are added to the associated zone in the lower
    half of the court.
    """
    central_symmetry = lambda (a, b): (
        len(x_grid) / 2 - (a - len(x_grid) / 2),
        len(y_grid) / 2 - (b - len(y_grid) / 2))

    key_to_delete_gen = ((x, y) for x in range(len(x_grid) + 1)
                         for y in range(
        int(np.ceil((len(y_grid) + 1) / 2)), len(y_grid) + 1))
    for i, j in key_to_delete_gen:
        zone_count = zones.pop((i, j), None)
        if zone_count is None:
            raise KeyError("The zone that should be removed does not exist.")
        zones[central_symmetry((i, j))] += zone_count
    return zones


def filter_shots(request, match_id):
    """
    Basically does the same thing as the serializer class should.
    We probably could have used the get_queryset method of a custom
    serializer class but I could not get it to work.
    :param request:
    :param match_id:
    :return:
    """
    match = get_object_or_404(Match, id=match_id)
    shot_type = request.GET.getlist('shot_type')
    special_shot = request.GET.getlist('special_shot')
    player = request.GET.get('player')
    conclusion = request.GET.getlist('conclusion')
    player_scoring = request.GET.getlist('player_scoring')

    queryset = TennisShot.objects.all()

    if player is None:
        player = (match.player_one == get_object_or_404(
            Player, user=request.user))

    queryset = queryset.filter(player=player)

    if match_id is not None:
        queryset = queryset.filter(tennis_point__match_id=match_id)

        queryset = queryset.filter(
            tennis_point__player_scoring__in=[bool(int(p))
                                              for p in player_scoring])

    if 'All' not in conclusion:
        # Otherwise we show all the shots.
        queryset = queryset.filter(tennis_point__conclusion__in=conclusion,
                                   is_final_shot=True)

    queryset = queryset.filter(shot_type__in=shot_type)

    if 'R' in special_shot:
        special_shot.remove('R')
        queryset = queryset.filter(Q(serve_status='R') |
                                   Q(special_shot__in=special_shot))

    else:
        queryset = queryset.filter(Q(serve_status=None) &
                                   Q(special_shot__in=special_shot))

    return queryset


@login_required
def zone_data(request, match_id):
    shots = filter_shots(request, match_id)

    zones_impact, zones_position = get_zones(shots)

    # We 'collapse' some zones together:
    x_grid_range = set(a for a, b in zones_impact.keys())
    zones_impact[(4, 3)] = sum([zones_impact.pop((i, 3))
                                for i in x_grid_range])
    # Convention used: a coordinate of 4 indicates the percentage should be
    # placed in the middle.
    zones_impact[(4, 0)] = sum([zones_impact.pop((i, 0))
                                for i in x_grid_range])

    y_grid_range = set(b for a, b in zones_impact.keys() if a != 4)

    zones_impact[(0, 4)] = sum([zones_impact.pop((0, j))
                                for j in y_grid_range])
    zones_impact[(3, 4)] = sum([zones_impact.pop((3, j))
                                for j in y_grid_range])

    # We group zones differently for the placement.
    x_grid_range = set(a for a, b in zones_position.keys())

    # zones_position[(4, 2)] = sum([zones_position.pop((i, 2))
    # for i in x_grid_range])
    zones_position[(1, 2)] += (zones_position.pop((0, 2)) +
                               zones_position.pop((0, 3)) +
                               zones_position.pop((1, 3)))
    zones_position[(2, 2)] += (zones_position.pop((3, 2)) +
                               zones_position.pop((2, 3)) +
                               zones_position.pop((3, 3)))
    zones_position[(1, 0)] += zones_position.pop((0, 0))
    zones_position[(1, 1)] += zones_position.pop((0, 1))
    zones_position[(2, 0)] += zones_position.pop((3, 0))
    zones_position[(2, 1)] += zones_position.pop((3, 1))

    # Dictionaries must have string keys to be dumped to json.
    # Plus it is convenient to have a `nvd3` format to access data in js.
    n_shots = len(shots)
    zones_impact = transform_zones_json(zones_impact, n_shots)
    zones_position = transform_zones_json(zones_position, n_shots)

    data_dict = {
        'zones_impact': zones_impact,
        'zones_position': zones_position
    }
    return HttpResponse(json.dumps(data_dict))


def get_match_info(request, match):
    """
    Helper function: Return a dict with context data about the relevant match.
    :param request:
    :param match_id:
    :return:
    """
    FOREHAND = 'F'
    BACKHAND = 'B'
    SHOT_TYPE_CHOICES = (
        (FOREHAND, 'Coup Droit'),
        (BACKHAND, 'Revers'),
    )

    shot_type_verbose_names = json.dumps(dict(
        TennisShot.SHOT_TYPE_CHOICES))
    special_shot_verbose_names = json.dumps(dict(
        TennisShot.SPECIAL_SHOT_CHOICES))
    user_player_bool = (match.player_one == get_object_or_404(
        Player, user=request.user))
    score_set_games = list(set((p.sets_player_one, p.sets_player_two,
                                p.games_player_one, p.games_player_two)
                               for p in match.points.all()))

    score_set_games = [s for s in score_set_games if None not in s]

    score_set_games.sort(key=lambda x: x[2] + x[3])
    score_set_games.sort(key=lambda x: x[0] + x[1])
    context_dict = {
        'user': request.user,
        'user_player_bool': user_player_bool,
        'match': match,
        'SHOT_TYPE_CHOICES': SHOT_TYPE_CHOICES,
        'SPECIAL_SHOT_CHOICES': TennisShot.SPECIAL_SHOT_CHOICES,
        'shot_type_verbose_names': shot_type_verbose_names,
        'special_shot_verbose_names': special_shot_verbose_names,
        'score_set_games': score_set_games
    }
    return context_dict


@login_required
def courts_with_zone_data(request, match_id):
    """
    Transmit general data about the match to the template.
    :param request:
    :param match_id:
    :return:
    """
    match = get_object_or_404(Match, id=match_id)
    if user_can_see_match(request.user, match):
        request.user.nav_state = "zones"
        context_dict = get_match_info(request, match)
    else:
        return redirect(to='../')

    return render(request, 'tennis/courts_with_zone_data.html', context_dict)


@login_required
def court_with_zone_data_serve(request, match_id):
    """
    Transmit general data about the match to the template.
    :param request:
    :param match_id:
    :return:
    """
    match = get_object_or_404(Match, id=match_id)
    if user_can_see_match(request.user, match):
        request.user.nav_state = "zones"
        context_dict = get_match_info(request, match)
    else:
        return redirect(to='../')

    return render(request, 'tennis/courts_serve.html', context_dict)


@login_required
def ellipses(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if user_can_see_match(request.user, match):
        try:
            player_one_global_stats = get_object_or_404(
                StatsBoard, id=match.player_one_global_stats.id)
            player_two_global_stats = get_object_or_404(
                StatsBoard, id=match.player_two_global_stats.id)
        except AttributeError:
            match.save()
            player_one_global_stats = get_object_or_404(
                StatsBoard, id=match.player_one_global_stats.id)
            player_two_global_stats = get_object_or_404(
                StatsBoard, id=match.player_two_global_stats.id)

        (int_board_key_values_list,
         float_board_key_values_list) = player_one_global_stats.sorted_board_two_players(
            player_two_global_stats)
        # fields_names = model_to_dict(player_one_global_stats)
        shot_type_verbose_names = json.dumps(
            dict(TennisShot.SHOT_TYPE_CHOICES))
    else:
        return redirect(to='../')
    context_dict = {
        'user': request.user,
        'match': match,
        'int_board_key_values_list': int_board_key_values_list,
        'float_board_key_values_list': float_board_key_values_list,
        'SHOT_TYPE_CHOICES': TennisShot.SHOT_TYPE_CHOICES,
        'shot_type_verbose_names': shot_type_verbose_names
    }
    return render(request, 'tennis/ellipses.html', context_dict)


def zones_postprocessing_left(zones, x_grid):
    """Post processing of zones obtained from counting serves.
    WARNING: This function assumes that we are dealing with the left side of
    the half-court.
    Remove zones that are not interesting and make sure they are aggregated
    properly."""
    # The net zone:
    zones[(2, 2)] = sum([zones.pop((i, 2)) for i in range(len(x_grid) + 1)])

    # The zone near the serve central line needs particular treatment.
    zones[(3, 1)] += zones.pop((4, 1))

    zones[(2, 0)] = sum([zones.pop((i, 0)) for i in range(len(x_grid) + 1)])
    zones[(2, 0)] += zones.pop((0, 1))
    zones[(2, 0)] += sum([
        zones.pop((i, 1)) for i in range(int(np.floor(len(x_grid) / 2.)) + 1,
                                         len(x_grid) + 1)])
    print 'In zone postprocessing left'
    return zones


def zones_postprocessing_right(zones, x_grid):
    def apply_middle_axis_symmetry(zones):
        zones_reversed = {}
        for i, j in zones.keys():
            zones_reversed[(len(x_grid) - i, j)] = zones[(i, j)]
        return zones_reversed

    zones_reversed = apply_middle_axis_symmetry(zones)
    zones_reversed_processed = zones_postprocessing_left(zones_reversed,
                                                         x_grid)
    zones = apply_middle_axis_symmetry(zones_reversed_processed)
    return zones


@login_required
def zone_serves(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    if user_can_see_match(request.user, match):
        user_player_bool = (match.player_one == get_object_or_404(
            Player, user=request.user))

        shots = TennisShot.objects.filter(tennis_point__match_id=match_id,
                                          player=user_player_bool)

        serve_status = request.GET.getlist('serve_status')

        shots = shots.filter(serve_status__in=serve_status)

        # We split the first serves according to the service square they are
        # supposed to be played into.
        # WARNING: Remember the y axis in tennis logger was downwards...
        serves_right = shots.filter(
            Q(shot_type='S'),
            (Q(start_position_x__gte=0.5) & Q(start_position_y__gte=0.5))
            | (Q(start_position_x__lte=0.5) & Q(start_position_y__lte=0.5)))

        serves_left = shots.filter(
            Q(shot_type='S'),
            (Q(start_position_x__lte=0.5) & Q(start_position_y__gte=0.5))
            | (Q(start_position_x__gte=0.5) & Q(start_position_y__lte=0.5)))

        first_serves_right = serves_right.filter(number=1)
        first_serves_left = serves_left.filter(number=1)
        second_serves_right = serves_right.filter(number=2)
        second_serves_left = serves_left.filter(number=2)

        court = CourtUsedInRecording()
        x_grid = court.x_grid_serve()
        y_grid = court.y_grid_serve()

        zones_first_right = _get_zones_serve(x_grid, y_grid,
                                             first_serves_right, side='right')
        zones_first_left = _get_zones_serve(x_grid, y_grid,
                                            first_serves_left, side='left')

        zones_second_right = _get_zones_serve(x_grid, y_grid,
                                              second_serves_right,
                                              side='right')
        zones_second_left = _get_zones_serve(x_grid, y_grid,
                                             second_serves_left,
                                             side='left')

        zones_first_serve = {
            'left': transform_zones_json(zones_first_left,
                                         first_serves_left.count()),
            'right': transform_zones_json(zones_first_right,
                                          first_serves_right.count())
        }

        zones_second_serve = {
            'left': transform_zones_json(zones_second_left,
                                         second_serves_left.count()),
            'right': transform_zones_json(zones_second_right,
                                          second_serves_right.count())
        }

        zones_serve = {
            'first': zones_first_serve,
            'second': zones_second_serve
        }

        return HttpResponse(json.dumps(zones_serve))


def _get_zones_serve(x_grid, y_grid, serves, side='left'):
    """
    Return a dictionary with tuples as keys representing the zones.

    Just a helper function ('pipeline-like').
    :param serves:
    :return:
    """
    assert(side in ['left', 'right'])

    zones = zones_from_grid(x_grid, y_grid,
                            [(shot.end_position_x, 1 - shot.end_position_y)
                             for shot in serves])
    if side == 'left':
        zones = zones_postprocessing_left(zones, x_grid)
    elif side == 'right':
        zones = zones_postprocessing_right(zones, x_grid)
    return zones


def transform_zones_json(zones, n_shots):
    """Return a jsonable object (list of dict) to display zone percentages.

    Transform the zones object into the right format for JS.
    `n_shots`, the total number of shots in the zones, is necessary to
    get the percentages (normalization).
    """
    if n_shots == 0:
        n_shots = 1

    zones_json = [
        {
            'x_pos': key[0],
            'y_pos': key[1],
            'percentage': 100 * value / n_shots,
            'count': value
        }
        for key, value in zones.iteritems()]
    return zones_json