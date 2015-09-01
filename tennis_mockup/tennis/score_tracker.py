__author__ = 'laurent'

from score import Score
import copy as copy
import jsonpickle as jsonpickle


POINTS_STR = ('0', '15', '30', '40')


class ScoreTracker(object):
    def __init__(self, match=None, points=(0, 0), games=(0, 0), sets=(0, 0),
                 sets_final_score=()):
        self.match = match
        self.tennis_points = []
        self.current_score = Score(points, games, sets)
        self.sets_to_win = 3
        self.match_is_over = False
        self.sets_final_score = list(sets_final_score)
        if match is not None and match.points.all().count() > 0:
            self.first_player_to_serve = [
                p.player_serving
                for p in match.points.order_by('number')
                if p.player_serving is not None][0]
        else:
            self.first_player_to_serve = None

    def update_score(self, tennis_point):
        """Update the ScoreTracker with a TennisPoint object (last point
        played).

        Also take care of assigning score and special property to the given
        tennis_point.
        """
        tennis_point.assign_score(self.current_score)
        if self.match_is_over:
            raise (ValueError,
                   "The match is over, the final score was {0}".format(self.sets_final_score))
        if self.in_tiebreak():
            self.increment_point_tiebreak(scorer=tennis_point.player_scoring)
        else:
            self.set_breakpoint(tennis_point)
            self.increment_point(tennis_point.player_scoring)
        self.tennis_points.append(copy.deepcopy(tennis_point))

    def set_breakpoint(self, tennis_point):
        """Set the `special` attribute of the given point if it is a
        breakpoint.

        Warning: this function should only be called in a non-tiebreak
        situation.
        """
        a, b = self.current_score.points
        is_gamepoint_player_one = (b >= 3 and b > a)
        is_gamepoint_player_two = (a >= 3 and a > b)

        is_breakpoint_player_one = (is_gamepoint_player_one and
                                    not tennis_point.player_serving)
        is_breakpoint_player_two = (is_gamepoint_player_two and
                                    tennis_point.player_serving)
        if is_breakpoint_player_one or is_breakpoint_player_two:
            tennis_point.special = 'B'

    # def breakpoints(self):
    # """Returns a QuerySet with all breakpoints."""
    # #TODO: implement!
    #     def is_breakpoint(point):
    #         a, b = point.points_player_one, point.points_player_two
    #         breakpoint_player_one = (a >= 3 and a > b and point.player_serving)
    #         breakpoint_player_two = (b >= 3 and b > a and point.player_serving)
    #         return breakpoint_player_one or breakpoint_player_two

    # def is_setpoint(point):
    #     g_a, g_b = point.games_player_one, point.games_player_two
    #     p_a, p_b = point.points_player_one, point.points_player_two
    #
    #     setpoint_player_one = (g_a >= 5 and g_a > g_b) and
    #
    #     (a >= 3 and a > b and point.player_serving)
    #     pass
    #
    # #TODO: to filter the points it is probably better to loop over the qs.
    # for point in self.points.all():
    #     if is_breakpoint(point):
    #         point.special = 'B'
    #     else:

    def increment_point(self, scorer):
        """Updates the current score by adding a point to scorer following
        rules in a non-tiebreak situation."""
        self.current_score.points[scorer] += 1
        points = self.current_score.points
        if ((points[scorer] > (points[(scorer + 1) % 2] + 1)) and
                (points[scorer] > 3)):
            self.increment_games(scorer)

    def increment_point_tiebreak(self, scorer):
        """Updates the current score by adding a point to scorer following
        tiebreak rules."""
        self.current_score.points[scorer] += 1
        points = self.current_score.points
        # Condition rule to win the tiebreak.
        if ((points[scorer] > (points[(scorer + 1) % 2] + 1)) and
                (points[scorer] >= 7)):
            self.increment_games(scorer)

    def increment_sets(self, scorer):
        """Increments the total of sets the `scorer` player won."""
        self.sets_final_score.append(copy.copy(self.current_score.games))
        self.current_score.games = [0, 0]
        self.current_score.sets[scorer] += 1
        if self.current_score.sets[scorer] == self.sets_to_win:
            print 'MATCH OVER'
            print self.sets_to_win
            print self.current_score.sets[scorer]
            self.match_is_over = True

    def increment_games(self, scorer):
        """Increments the total of games the `scorer` player won, counting
        a new set when required."""
        last_game_was_a_tiebreak = self.in_tiebreak()
        self.current_score.points = [0, 0]
        self.current_score.games[scorer] += 1
        games = self.current_score.games
        if ((games[scorer] > (games[(scorer + 1) % 2] + 1)) and
                (self.current_score.games[scorer] >= 6)):
            self.increment_sets(scorer)
        if last_game_was_a_tiebreak:
            # We are not in a last sets: the last game was a tiebreak.
            self.increment_sets(scorer)

    def in_tiebreak(self):
        """Tells if the current score corresponds to a tiebreak situation."""
        return ((sum(self.current_score.sets) < (2 * self.sets_to_win - 1))
                and (self.current_score.games == [6, 6]))

    def __unicode__(self):
        games = self.current_score.games
        points = self.current_score.points
        sets_final_score = [s[i] for i in [0, 1]
                            for s in self.sets_final_score]
        if not sets_final_score:
            # list is empty.
            sets_final_score = ['', '']
        player_score_str = []
        for i in [0, 1]:
            if self.in_tiebreak():
                games_and_points_str = ' '.join([games[i], points[i]])
            else:
                if max(points) > 3:
                    # We are in a deuce/advantage situation
                    if points[i] > points[(i + 1) % 2]:
                        games_and_points_str = '{0} {1}'.format(games[i],
                                                                'Ad')
                    else:
                        games_and_points_str = '{0} {1}'.format(games[i],
                                                                ' - ')
                else:
                    games_and_points_str = '{0} {1}'.format(
                        games[i], POINTS_STR[points[i]])

            player_score_str.append("\n Player {0}: {1} - {2}".format(
                i, ' '.join(sets_final_score[i]), games_and_points_str))
        print player_score_str
        score_str = "The score currently is:\n{0}\n{1}".format(
            player_score_str[0], player_score_str[1])
        return score_str

    def pop_point(self):
        """
        Removes the last point and 'rewinds' the score accordingly.
        """
        self.tennis_points.pop()
        if len(self.tennis_points) > 0:
            self.current_score = copy.deepcopy(self.tennis_points[-1].score)
        else:
            self.current_score = Score()

    def json_serializer(self, filename='logfile.txt'):
        jsonpickle.set_encoder_options('json', indent=4)
        with open(filename, 'w') as f:
            json_obj = jsonpickle.encode(self)
            f.write(json_obj)
            f.close()
