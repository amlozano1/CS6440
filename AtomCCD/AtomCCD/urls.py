from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AtomCCD.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^CCD/', include('CCD.urls', namespace='CCD')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', login),
    url(r'^accounts/logout/', logout, {'next_page': '/CCD/'}),
    )
if settings.DEBUG:
# static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
