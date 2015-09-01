# -*- coding: utf-8 -*-

from __future__ import division

from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User

from tennis.score_tracker import ScoreTracker
from tennis.score import Score


class Player(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=42)

    def __unicode__(self):
        return "Username: {0} ; Player name: {1}".format(self.user.username,
                                                         self.name)


class StatsBoard(models.Model):
    aces = models.IntegerField(verbose_name=u'Aces')
    double_faults = models.IntegerField(verbose_name=u'Double fautes')
    first_serve = models.FloatField(verbose_name=u'Premier service')
    first_serve_won = models.FloatField(
        verbose_name=u'Points gagnés après premier service')
    second_serve_won = models.FloatField(
        verbose_name=u'Points gagnés après second service')
    winners = models.IntegerField(verbose_name=u'Coups gagnants')
    unforced_errors = models.IntegerField(verbose_name=u'Fautes directes')
    breakpoints = models.IntegerField(verbose_name=u'Balles de break obtenues')
    breakpoints_won = models.IntegerField(
        verbose_name=u'Balles de break converties')

    def sorted_board_two_players(self, other_statsboard):
        """
        Return a list of 3-tuple with the names of the attributes, the
        value for the current board and the value for the other stats board.

        Typically used in the template to display the statsboard.
        :param other_statsboard:
        :return:
        """
        int_fields = ["aces", "double_faults", "winners",
                      "unforced_errors", "breakpoints", "breakpoints_won"]
        float_fields = ["first_serve", "first_serve_won", "second_serve_won"]
        int_key_values_list = [(self._meta.get_field(key).verbose_name.title(),
                                self.__dict__[key],
                                other_statsboard.__dict__[key])
                               for key in int_fields]
        float_key_values_list = [
            (self._meta.get_field(key).verbose_name.title(),
             self.__dict__[key], other_statsboard.__dict__[key])
            for key in float_fields]

        return int_key_values_list, float_key_values_list

    def __unicode__(self):
        return u'{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}'.format(
            self.aces, self.double_faults, self.first_serve,
            self.first_serve_won, self.second_serve_won,
            self.winners, self.unforced_errors, self.breakpoints,
            self.breakpoints_won)


class Match(models.Model):
    timestamp = models.DateTimeField(verbose_name='Date et heure du match',
                                     auto_now_add=True)
    name = models.CharField(verbose_name='Nom', max_length=200)
    player_one = models.ForeignKey('Player', verbose_name='Joueur_1',
                                   related_name='player_one')
    player_two = models.ForeignKey('Player', verbose_name='Joueur_2',
                                   related_name='player_two')
    player_one_global_stats = models.ForeignKey(
        'StatsBoard', verbose_name=u'Statistiques joueur 1',
        related_name='player_one_global_stats', null=True)
    player_two_global_stats = models.ForeignKey(
        'StatsBoard', verbose_name=u'Statistiques joueur 2',
        related_name='player_two_global_stats', null=True)
    video = models.URLField(verbose_name=u'Lien vers la vidéo', null=True)

    objects = models.Manager()

    def __unicode__(self):
        return unicode(self.name + str(self.timestamp))

    def aces(self):
        """
        Returns a QuerySet of points with the aces of the match.
        :return: django.db.models.query.QuerySet
        """
        aces = (self.points.filter(conclusion='W').
                annotate(num_shot_types=Count('shots__shot_type',
                                              distinct=True)).
                filter(num_shot_types=1))
        return aces

    def doubles(self):
        """
        Returns a QuerySet with the double faults of the match.
        :return: django.db.models.query.QuerySet
        """
        doubles = (self.points.filter(conclusion='U').
                   annotate(num_shot_types=Count('shots__shot_type',
                                                 distinct=True)).
                   filter(num_shot_types=1))
        return doubles

    def first_serves(self):
        """Returns a QuerySet with the points of the match for which the first
        serve went in.
        :return: django.db.models.query.QuerySet
        """
        first_serves = (self.points.filter(shots__shot_type='S').
                        annotate(num_serves=Count('shots__shot_type')).
                        filter(num_serves=1))
        return first_serves

    def second_serves(self):
        """Returns a QuerySet with the points of the match for which the first
        serve did not go in.
        :return: django.db.models.query.QuerySet
        """
        second_serves = (self.points.filter(shots__shot_type='S').
                         annotate(num_serves=Count('shots__shot_type')).
                         filter(num_serves=2))
        return second_serves

    def _get_stats_board(self, player, aces, double_faults, first_serve,
                         second_serve, winners_and_aces,
                         unforced, breakpoints):
        first_serve_count_player = len(
            first_serve.filter(player_serving=player))
        second_serve_count_player = len(
            second_serve.filter(player_serving=player))

        n_doubles = double_faults.filter(player_scoring=not player).count()

        try:
            second_serve_won = (100 * len(second_serve.filter(
                player_serving=player, player_scoring=player)
            ) / second_serve_count_player)
        except ZeroDivisionError:
            second_serve_won = 0

        return StatsBoard(
            aces=aces.filter(player_scoring=player).count(),
            double_faults=n_doubles,
            first_serve=(
                100 * first_serve_count_player
                / len(self.points.filter(player_serving=player))),
            first_serve_won=(
                100 * len(first_serve.filter(player_serving=player,
                                             player_scoring=player))
                / first_serve_count_player),
            second_serve_won=second_serve_won,
            winners=(winners_and_aces.filter(player_scoring=player).count()
                     - aces.filter(player_scoring=player).count()),
            unforced_errors=(unforced.filter(player_scoring=not player).count()
                             - n_doubles),
            breakpoints=breakpoints.filter(player_serving=not player).count(),
            breakpoints_won=breakpoints.filter(
                player_serving=not player,
                player_scoring=player).count())

    def set_stats_board(self):
        """Add match-level player statistics to the Match object.

        Set player_one_global_stats and player_one_global_stats attributes.
        :return: None
        """
        aces = self.aces()
        double_faults = self.doubles()
        first_serve = self.first_serves()
        second_serve = self.second_serves()
        winners_and_aces = self.points.filter(conclusion='W')
        unforced = self.points.filter(conclusion='U')
        breakpoints = self.points.filter(special='B')

        player_one_stats_board = self._get_stats_board(
            player=True, aces=aces, double_faults=double_faults,
            first_serve=first_serve, second_serve=second_serve,
            winners_and_aces=winners_and_aces, unforced=unforced,
            breakpoints=breakpoints)

        player_two_stats_board = self._get_stats_board(
            player=False, aces=aces, double_faults=double_faults,
            first_serve=first_serve, second_serve=second_serve,
            winners_and_aces=winners_and_aces, unforced=unforced,
            breakpoints=breakpoints)

        player_one_stats_board.save()
        player_two_stats_board.save()
        self.player_one_global_stats = player_one_stats_board
        self.player_two_global_stats = player_two_stats_board

    def get_score_list(self):
        """Return a list containing the score after each point."""
        st = ScoreTracker()
        score_list = []
        for point in self.points.order_by('number'):
            st.update_score(point)
            score_list.append(st.current_score)
        return score_list

    def save(self, *args, **kwargs):
        # if not self.pk: a good way to add something ONLY on creation of
        # the object.
        self.process_match()
        if self.points.all():
            self.set_stats_board()
        super(Match, self).save(*args, **kwargs)

    def process_match(self):
        """Process the game, assign score to points and mark breakpoints."""
        st = ScoreTracker(match=self)
        for point in self.points.order_by('number'):
            st.update_score(point)
            point.save()
            point.process_point()
            point.save()


class TennisPoint(models.Model):
    """
    The `special` attribute supports only breakpoints for now, not setpoints
    nor matchpoints. Enabling it will require changing the 'breakpoints'
    method.
    """
    WINNER = 'W'
    UNFORCED = 'U'
    REGULAR_ERROR = 'R'
    CONCLUSION_CHOICES = (
        (WINNER, u'Coup gagnant'),
        (UNFORCED, u'Faute directe'),
        (REGULAR_ERROR, u'Faute provoquée'),
    )
    BREAKPOINT = 'B'
    SETPOINT = 'S'
    MATCHPOINT = 'M'
    BREAKPOINT_SETPOINT = 'BS'
    BREAKPOINT_MATCHPOINT = 'BM'
    SPECIAL_POINTS = (
        (BREAKPOINT, u'Balle de break'),
        (SETPOINT, u'Balle de set'),
        (MATCHPOINT, u'Balle de match'),
        (BREAKPOINT_SETPOINT, u'Balle de break et de set'),
        (BREAKPOINT_MATCHPOINT, u'Balle de break et de match'),
    )
    number = models.IntegerField(verbose_name=u'Numéro du coup')
    player_serving = models.BooleanField(verbose_name=u'Joueur 1 au service')
    player_scoring = models.BooleanField(
        verbose_name=u'Joueur 1 gagne le point')
    conclusion = models.CharField(max_length=1,
                                  verbose_name=u'Conclusion du point',
                                  choices=CONCLUSION_CHOICES)
    special = models.CharField(max_length=2, verbose_name=u'Point important',
                               choices=SPECIAL_POINTS, null=True)
    # TODO: Verbose names?
    points_player_one = models.IntegerField(null=True)
    points_player_two = models.IntegerField(null=True)
    games_player_one = models.IntegerField(null=True)
    games_player_two = models.IntegerField(null=True)
    sets_player_one = models.IntegerField(null=True)
    sets_player_two = models.IntegerField(null=True)

    match = models.ForeignKey(
        to='Match', verbose_name=u'Le Match associé',
        related_name='points')

    objects = models.Manager()

    def assign_score(self, score):
        assert (isinstance(score, Score))
        self.points_player_one, self.points_player_two = score.points
        self.games_player_one, self.games_player_two = score.games
        self.sets_player_one, self.sets_player_two = score.sets

    def __unicode__(self):
        return 'point won by ' + str(self.player_scoring)

    def process_point(self):
        self.set_shot_number()
        self.set_is_final_shot()
        self.set_serve_status()

    def set_shot_number(self):
        """
        Set shot number field for the shots in the point.
        """
        for i, shot in enumerate(self.shots.all()):
            shot.number = i + 1
            shot.save()

    def set_is_final_shot(self):
        """
        Process the point to assign shot_status to each shot.
        """
        final_shot = self.shots.order_by('number').last()
        if final_shot:
            final_shot.is_final_shot = True
            final_shot.save()

    def set_serve_status(self):
        """Process the point to assign serve_status and is_first_serve
        in the point.
        """
        serves = self.shots.filter(shot_type='S').order_by('number')

        n_shots = self.shots.count()
        n_serves = serves.count()

        if n_serves > 0:
            last_serve = serves.last()
            if n_serves > 1:
                print 'n_serves > 1'
                # We have two serves or more: the first is out.
                first_serve = serves[0]
                first_serve.serve_status = TennisShot.OUT
                first_serve.save()

            if n_serves == n_shots:
                print 'n_serves == n_shots'
                # If we have only serves in the point,
                # then the last serve is an ace or a double.
                if self.conclusion == TennisPoint.UNFORCED:
                    last_serve.serve_status = TennisShot.OUT
                elif self.conclusion == TennisPoint.WINNER:
                    last_serve.serve_status = TennisShot.ACE
                else:
                    print 'set_serve_status: n_serves==n_shots and yet the ' \
                          'point is neither a winner nor an unforced.'
            elif n_shots > n_serves:
                # We cannot have an ace or a double anymore.
                if ((n_serves + 1) == n_shots) and (
                            self.player_scoring == self.player_serving):
                    last_serve.serve_status = TennisShot.WINNING_SERVE
                else:
                    last_serve.serve_status = TennisShot.IN

                shot_after_serve = self.shots.order_by('number')[n_serves]
                shot_after_serve.serve_status = TennisShot.RETURN
                shot_after_serve.save()
            last_serve.save()
        else:
            print 'n_serves is 0'
            return


class TennisShot(models.Model):
    FOREHAND = 'F'
    BACKHAND = 'B'
    SERVE = 'S'
    SHOT_TYPE_CHOICES = (
        (FOREHAND, 'Coup Droit'),
        (BACKHAND, 'Revers'),
        (SERVE, 'Service'),
    )
    VOLLEY = 'V'
    SMASH = 'S'
    SPECIAL_SHOT_CHOICES = (
        (VOLLEY, 'Volée'),
        (SMASH, 'Smash'),
    )

    start_position_x = models.FloatField(verbose_name=u'Frappe - x')
    start_position_y = models.FloatField(verbose_name=u'Frappe - y')
    end_position_x = models.FloatField(verbose_name=u'Impact - x')
    end_position_y = models.FloatField(verbose_name=u'Impact - y')
    timestamp = models.DateTimeField(
        verbose_name=u'Instant auquel le coup est joué', null=True)
    shot_type = models.CharField(max_length=1, choices=SHOT_TYPE_CHOICES,
                                 default=None)
    special_shot = models.CharField(
        max_length=1, choices=SPECIAL_SHOT_CHOICES, default=None)
    player = models.BooleanField(verbose_name=u'Coup joué par le joueur 1')
    tennis_point = models.ForeignKey(to='TennisPoint',
                                     verbose_name=u'Point associé',
                                     related_name='shots')

    ACE = 'A'
    WINNING_SERVE = 'W'
    OUT = 'O'
    IN = 'I'
    RETURN = 'R'

    SERVE_STATUS_CHOICES = (
        (ACE, 'Ace'),
        (WINNING_SERVE, 'Service gagnant'),
        (OUT, 'Faute'),
        (IN, u'Service retourné'),
        (RETURN, u'Retour de service'),
    )

    serve_status = models.CharField(max_length=1, choices=SERVE_STATUS_CHOICES,
                                    default=None, null=True, blank=True)

    is_final_shot = models.NullBooleanField(
        verbose_name=u'Le coup joué est le dernier du point')

    number = models.IntegerField(null=True)


if __name__ == '__main__':
    pass
    # import os
    #
    # os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
    # import django
    #
    # django.setup()
    # m = Match.objects.get(id=1)
    # m.save()
