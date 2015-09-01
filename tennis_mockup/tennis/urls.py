from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin

import api
from views import ListMatchesByUser


admin.autodiscover()


urlpatterns = patterns(
    'tennis.views',
    url(r'^$', ListMatchesByUser.as_view(), name='match_list_user'),
    url(r'^match/(?P<match_id>\d+)$', 'match_detail'),
    url(r'^match/(?P<match_id>\d+)/courts$', 'courts_with_zone_data'),
    url(r'^match/(?P<match_id>\d+)/courts_serve$',
        'court_with_zone_data_serve',
        name='court_with_zone_data_serve'),
    url(r'^match/shot_type_count.json', 'shot_type_count'),
    url(r'^match/(?P<match_id>\d+)/forehands', 'forehands'),
    url(r'^match/(?P<match_id>\d+)/winners_split',
    'winners_split'),
    url(r'^match/(?P<match_id>\d+)/unforced_split$',
     'unforced_split'),
    url(r'^match/(?P<match_id>\d+)/first_serve_split$',
        'first_serve_split'),
    url(r'^match/(?P<match_id>\d+)/second_serve_split$',
    'second_serve_split'),
    url(r'^match/(?P<match_id>\d+)/dashboard$',
    'dashboard'),
    url(r'^qunit$', TemplateView.as_view(
    template_name='tennis/qunit_shot_type_count.html')),
    url(r'^match/(?P<match_id>\d+)/zone_data', 'zone_data'),
    url(r'^match/(?P<match_id>\d+)/serves', 'zone_serves', name='zone_serves'),
    url(r'^match/(?P<match_id>\d+)/ellipses', 'ellipses'),
    )

urlpatterns_api = patterns('tennis.api',
                           url(r'^api/matches/$', api.MatchList.as_view()),
                           url(r'^api/matches/(?P<pk>[0-9]+)',
                               api.MatchDetail.as_view()),
                           url(r'^api/points',
                               api.PointsFiltered.as_view(),
                               name='api_points'),
                           url(r'^api/shots',
                               api.ShotsFiltered.as_view(), name='api_shots'),
                           url(r'^api/aces',
                               api.ShotsAces.as_view(), name='api_aces'),
                           )

urlpatterns += format_suffix_patterns(urlpatterns_api)
