__author__ = 'laurent'

import copy as copy


class Score(object):
    """A score object."""

    def __init__(self, points=(0, 0), games=(0, 0), sets=(0, 0)):
        """
        :param points:
        :param games:
        :param sets:
        :return:
        """
        self.sets_ = list(sets)
        self.games_ = list(games)
        self.points_ = list(points)

        # assert_is_instance(points, TennisPoint,
        # msg='Expected TennisPoint, got object '
        # 'of class {0}'.format(points.__class__))

    @property
    def points(self):
        return self.points_

    @property
    def games(self):
        return self.games_

    @property
    def sets(self):
        return self.sets_

    @points.setter
    def points(self, value):
        self.points_ = copy.deepcopy(value)

    @games.setter
    def games(self, value):
        self.games_ = copy.deepcopy(value)

    @sets.setter
    def sets(self, value):
        self.sets_ = copy.deepcopy(value)