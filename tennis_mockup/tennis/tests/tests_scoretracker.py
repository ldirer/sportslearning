from tennis_mockup.tennis.models import TennisPoint
from tennis_mockup.tennis.score_tracker import ScoreTracker
from nose.tools import assert_equal


def test_server_scores_an_incrementing_point():
    score_tracker = ScoreTracker()
    score_tracker.increment_point(scorer=0)
    assert_equal([1, 0], score_tracker.current_score.points)


def test_receiver_scores_an_incrementing_point():
    score_tracker = ScoreTracker(points=(0, 0))
    score_tracker.increment_point(scorer=1)
    assert_equal([0, 1], score_tracker.current_score.points)


def test_receiver_scores_with_advantage():
    score_tracker = ScoreTracker(points=(4, 5))
    score_tracker.increment_point(1)
    assert_equal([0, 0], score_tracker.current_score.points)


def test_wins_games_by_two_clear_points():
    score_tracker = ScoreTracker(points=(1, 3))
    score_tracker.increment_point(1)
    assert_equal([0, 0], score_tracker.current_score.points)
    assert_equal([0, 1], score_tracker.current_score.games)


def test_wins_sets_with_tiebreak():
    score_tracker = ScoreTracker(points=(5, 6), games=(6, 6), sets=(1, 1))
    score_tracker.increment_point(1)
    assert_equal([0, 0], score_tracker.current_score.points)
    assert_equal([0, 0], score_tracker.current_score.games)
    assert_equal([1, 2], score_tracker.current_score.sets)


def test_wins_set_without_tiebreak():
    score_tracker = ScoreTracker(points=(1, 3), games=(5, 6), sets=(1, 1))
    score_tracker.increment_point(1)
    assert_equal([0, 0], score_tracker.current_score.points)
    assert_equal([0, 0], score_tracker.current_score.games)
    assert_equal([1, 2], score_tracker.current_score.sets)


def test_print_smoke():
    score_tracker = ScoreTracker(points=(1, 3), games=(5, 6), sets=(1, 1))
    score_tracker.__unicode__()


def test_set_breakpoint():
    score_tracker = ScoreTracker(points=(1, 3), games=(5, 6), sets=(1, 1))
    point = TennisPoint()
    score_tracker.set_breakpoint(point)
    assert_equal(point.special, 'B')


if __name__ == '__main__':
    import nose
    nose.runmodule()
