from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from conf.views import Config, EntryFormView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'domosys_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', 'base.views.login_user'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
	url(r'^tasks/', include('djcelery.urls')),
	url(r'^$', 'base.views.index', name='index'),

	url(r'^config/$', Config.as_view()),
	url(r'^config/(?P<caption_type>\w+)/(?P<caption_id>\d+)', EntryFormView.as_view()),
)
