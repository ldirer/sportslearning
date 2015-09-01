__author__ = 'laurent'

from rest_framework import serializers
from rest_framework import generics
from django.db.models import Count

from tennis.models import Match, TennisPoint, TennisShot


"""
Filtering from the bottom up might be slow if we have many matches: to get only
forehands for a given match it requires looking at all the shots from all
matches to see if they are from the right match.
However it is possible that the lazy evaluation of querysets makes it
irrelevant.
"""


class SimpleMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('name', 'player_one', 'player_one_global_stats',
                  'player_two', 'player_two_global_stats',
                  'timestamp', 'video')


class ShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TennisShot
        fields = ('start_position_x', 'start_position_y', 'end_position_x',
                  'end_position_y', 'player', 'shot_type', 'special_shot',
                  'serve_status', 'is_final_shot', 'number')


class PointSerializer(serializers.ModelSerializer):
    shots = ShotSerializer(many=True)

    class Meta:
        model = TennisPoint
        fields = ('number', 'player_scoring', 'conclusion', 'shots')


class CompleteMatchSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)

    class Meta:
        model = Match
        fields = ('name', 'player_one', 'player_one_global_stats',
                  'player_two', 'player_two_global_stats',
                  'timestamp', 'video', 'points')


class MatchList(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = SimpleMatchSerializer


class MatchDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Match.objects.all()
    serializer_class = CompleteMatchSerializer


class PointsFiltered(generics.ListAPIView):
    queryset = TennisPoint.objects.all()
    serializer_class = PointSerializer

    def get_queryset(self):
        match_id = self.request.QUERY_PARAMS.get('match_id', None)
        conclusion = self.request.QUERY_PARAMS.get('conclusion', None)
        player_scoring = self.request.QUERY_PARAMS.get('player_scoring', None)
        sets_player_one = self.request.QUERY_PARAMS.get('sets_player_one',
                                                        None)
        sets_player_two = self.request.QUERY_PARAMS.get('sets_player_two',
                                                        None)
        games_player_one = self.request.QUERY_PARAMS.get('games_player_one',
                                                         None)
        games_player_two = self.request.QUERY_PARAMS.get('games_player_two',
                                                         None)

        if sets_player_one is not None:
            self.queryset = self.queryset.filter(
                sets_player_one=sets_player_one)
        if sets_player_two is not None:
            self.queryset = self.queryset.filter(
                sets_player_two=sets_player_two)
        if games_player_one is not None:
            self.queryset = self.queryset.filter(
                games_player_one=games_player_one)
        if games_player_two is not None:
            self.queryset = self.queryset.filter(
                games_player_two=games_player_two)

        if player_scoring is not None:
            self.queryset = self.queryset.filter(player_scoring=player_scoring)
        if match_id is not None:
            self.queryset = self.queryset.filter(match_id=match_id)
        if conclusion is not None:
            self.queryset = self.queryset.filter(conclusion=conclusion)
        return self.queryset


class ShotsFiltered(generics.ListAPIView):
    queryset = TennisShot.objects.all()
    serializer_class = ShotSerializer

    def get_queryset(self):
        match_id = self.request.QUERY_PARAMS.get('match_id')
        player = self.request.QUERY_PARAMS.get('player')
        player_scoring = self.request.QUERY_PARAMS.get('player_scoring')
        conclusion = self.request.QUERY_PARAMS.getlist('conclusion')

        is_final_shot = self.request.QUERY_PARAMS.get('is_final_shot')
        number = self.request.QUERY_PARAMS.getlist('number')
        shot_type = self.request.QUERY_PARAMS.getlist('shot_type')
        special_shot = self.request.QUERY_PARAMS.getlist('special_shot')
        serve_status = self.request.QUERY_PARAMS.getlist('serve_status')

        n_shots = self.request.QUERY_PARAMS.get('n_shots')

        if match_id is not None:
            self.queryset = self.queryset.filter(
                tennis_point__match_id=match_id)
        if player is not None:
            self.queryset = self.queryset.filter(player=player)
        if player_scoring is not None:
            self.queryset = self.queryset.filter(
                tennis_point__player_scoring=player_scoring)

        if n_shots is not None:
            self.queryset = self.queryset.annotate(
                n_shots=Count('tennis_point__shots')).filter(n_shots=n_shots)

        if is_final_shot is not None:
            self.queryset = self.queryset.filter(
                is_final_shot=is_final_shot)

        if shot_type:
            print shot_type.__class__
            print shot_type
            self.queryset = self.queryset.filter(shot_type__in=shot_type)

        if special_shot:
            self.queryset = self.queryset.filter(special_shot__in=special_shot)

        if conclusion:
            self.queryset = self.queryset.filter(
                tennis_point__conclusion__in=conclusion)
        if serve_status:
            self.queryset = self.queryset.filter(serve_status__in=serve_status)

        if number:
            self.queryset = self.queryset.filter(number__in=number)

        return self.queryset


class ShotsAces(generics.ListAPIView):
    """
    WIP: Currently just a regular shots view that allows filtering using
    default filter backend (?shot_type=F&?tennis_point__conclusion=W works
    but not ?shot_type__in).
    """
    queryset = TennisShot.objects.all()
    serializer_class = ShotSerializer
    filter_fields = ('shot_type', 'tennis_point__conclusion')


if __name__ is '__main__':
    CompleteMatchSerializer(pk=1)
