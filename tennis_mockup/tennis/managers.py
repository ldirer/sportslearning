from django.db import models
from django.db import connection

from tennis.models import Match, TennisPoint, TennisShot

class MatchManager(models.Manager):
    #TODO: Assess if this is the right way to do things or if it is easier with the ORM (both methods below).
    #TODO: Mb we can do smt to group shot_type_count and special_shot_count...
    #TODO: Mb that is not the role of a manager (meant for table-level functionality, here we are at row level.

    def shot_type_count_orm(self):
        points = self.points
        shots = [shot for p in points.all() for shot in p.shots.all()]
        shot_types = [shot.shot_type for shot in shots]
        shot_type_count = {}
        for shot_type, pretty_shot_type in TennisShot.SHOT_TYPE_CHOICES:
            shot_type_count[pretty_shot_type] = shot_types.count(shot_type)
        return shot_type_count

    def shot_type_count(self):
        c = connection.cursor()
        c.execute("""
        select shot_type, count(shot_type)
        from tennis_tennisshot,
          tennis_tennispoint
        where tennis_point_id == tennis_tennispoint.id
          and tennis_tennispoint.match_id == %s
          group by shot_type
        """, self.id)
        shot_type_count = {}
        for row in c.fetchall():
            shot_type_count[row[0]] = row[1]
        return shot_type_count

    def special_shot_count(self):
        c = connection.cursor()
        c.execute("""
        select shot_type, count(shot_type)
        from tennis_tennisshot,
          tennis_tennispoint
        where tennis_point_id == tennis_tennispoint.id
          and tennis_tennispoint.match_id == %s
          group by shot_type
        """, self.id)
        special_shot_count = {}
        for row in c.fetchall():
            special_shot_count[row[0]] = row[1]
        return special_shot_count

#
# #FROM THE DOCS:
# class PollManager(models.Manager):
#     def with_counts(self):
#         from django.db import connection
#         cursor = connection.cursor()
#         cursor.execute("""
#             SELECT p.id, p.question, p.poll_date, COUNT(*)
#             FROM polls_opinionpoll p, polls_response r
#             WHERE p.id = r.poll_id
#             GROUP BY p.id, p.question, p.poll_date
#             ORDER BY p.poll_date DESC""")
#         result_list = []
#         for row in cursor.fetchall():
#             p = self.model(id=row[0], question=row[1], poll_date=row[2])
#             p.num_responses = row[3]
#             result_list.append(p)
#         return result_list
#
# class OpinionPoll(models.Model):
#     question = models.CharField(max_length=200)
#     poll_date = models.DateField()
#     objects = PollManager()
#
# class Response(models.Model):
#     poll = models.ForeignKey(OpinionPoll)
#     person_name = models.CharField(max_length=50)
#     response = models.TextField()
#
#
# class AuthorManager(models.Manager):
#     def get_queryset(self):
#         return super(AuthorManager, self).get_queryset().filter(role='A')
#
# class EditorManager(models.Manager):
#     def get_queryset(self):
#         return super(EditorManager, self).get_queryset().filter(role='E')
#
# class Person(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     role = models.CharField(max_length=1, choices=(('A', _('Author')), ('E', _('Editor'))))
#     people = models.Manager()
#     authors = AuthorManager()
#     editors = EditorManager()
