

from django.conf.urls import url
from django.views.generic.base  import RedirectView
from .views import  (
    LikeToggleAPIView,
    RetweetAPIView,
	TweetcreateAPIView,
    TweetListAPIView,
    TweetDetailAPIView,
	)
urlpatterns = [
    # #url(r'^admin/', admin.site.urls),
    # url(r'^$', RedirectView.as_view(url="/")), #/tweet/
    url(r'^$', TweetListAPIView.as_view(), name='list'), #/tweet/
    url(r'^create/$', TweetcreateAPIView.as_view(), name='create'), #/tweet/create/
    # url(r'^(?P<pk>\d/+)/retweet/$', RetweetAPIView.as_view(), name='retweet'), 
    url(r'^(?P<pk>\d+)/retweet/$', RetweetAPIView.as_view(), name='retweet'),#/tweet/create/
    url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like-toggle'),#/tweet/create/
     url(r'^(?P<pk>\d+)/$', TweetDetailAPIView.as_view(), name='detail'),#/tweet/create/

    #   # url(r'^(?P<pk>\d+)/$', tweet_detail_view, name='detail'),
    # url(r'^(?P<pk>\d+)/$', TweetDetailView.as_view(), name='detail'), #tweet/1
    # url(r'^(?P<pk>\d+)/update/$', TweetUpdateView.as_view(), name='update'), #/tweet/1/update
    # url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(), name='delete'), #/tweet/1/delete
    #url(r'^tweet/', include('tweets.urls')),

]

