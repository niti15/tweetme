
from django.conf.urls import url, include
from django.views.generic.base  import RedirectView
from .views import  (
   
    UserDetailView,
    UserFollowView,
    
    )
urlpatterns = [
    # url(r'^', include('django.contrib.auth.urls')),
    #url(r'^admin/', admin.site.urls),
    # url(r'^$', RedirectView.as_view(url="/")), #/tweet/
    # url(r'^search/$', TweetListView.as_view(), name='list'), #/tweet/
    # url(r'^create/$', TweetCreateView.as_view(), name='create'), #/tweet/create/
    # url(r'^profiles/', include('accounts.urls', namespace='profiles')),
    #   # url(r'^(?P<pk>\d+)/$', tweet_detail_view, name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='detail'), #tweet/1
    url(r'^(?P<username>[\w.@+-]+)/follow/$', UserFollowView.as_view(), name='follow'), #tweet/1
    # url(r'^(?P<pk>\d+)/update/$', TweetUpdateView.as_view(), name='update'), #/tweet/1/update
    # url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(), name='delete'), #/tweet/1/delete
    # #url(r'^tweet/', include('tweets.urls')),

]

