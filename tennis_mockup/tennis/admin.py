from django.contrib import admin
from tennis.models import Match, Player, TennisPoint, StatsBoard

# Register your models here.


class MatchAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'name', 'player_one', 'player_two')
    list_filter = ()
    timestamp_hierarchy = 'timestamp'
    ordering = ('timestamp', )


admin.site.register(Match, MatchAdmin)
admin.site.register(Player,)
admin.site.register(TennisPoint,)
admin.site.register(StatsBoard,)

