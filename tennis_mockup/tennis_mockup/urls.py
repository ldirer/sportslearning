from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.contrib import admin
from django.contrib.auth.views import login, logout


admin.autodiscover()

urlpatterns = patterns('',
                       (r'^accounts/login/$', login),
                       (r'^accounts/logout/$', logout)
)

urlpatterns += patterns('',
                        url(r'^tennis/', include('tennis.urls')),
                        url(r'^admin/', include(admin.site.urls))
)

urlpatterns += patterns('',
                        url(r'^$', RedirectView.as_view(url='tennis'))
)


# The function staticfiles_urlpatterns() only works with DEBUG=True.
# It should thus be used only during development!
if settings.DEBUG and False:
    urlpatterns += staticfiles_urlpatterns()
