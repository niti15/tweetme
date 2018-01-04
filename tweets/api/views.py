from rest_framework import generics
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from tweets.models import Tweets
from .serializers import TweetModelSerializer
from rest_framework import permissions
from .pagination import StandardResultPagination




class LikeToggleAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def get(self, request, pk,  format=None):
		# tweet = get_object_or_404(Tweets, pk=pk)
		tweet_qs = Tweets.objects.filter(pk=pk)
		message = "Not allowed"
		if request.user.is_authenticated():
			is_liked = Tweets.objects.like_toggle(request.user, tweet_qs.first())
			return Response({'liked': is_liked})
			
		return Response({"message": message}, status=400)



class RetweetAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def get(self, request, pk,  format=None):
		# tweet = get_object_or_404(Tweets, pk=pk)
		tweet_qs = Tweets.objects.filter(pk=pk)
		message = "Not allowed"
		if tweet_qs.exists() and tweet_qs.count() == 1:
			# if request.user.is_authenticated():
				new_tweet = Tweets.objects.retweet(request.user, tweet_qs.first())
				if new_tweet is not None:

					data  = TweetModelSerializer(new_tweet).data
					return Response(data)
				message = "cannot retwet in same 1 day"
		return Response({"message": message}, status=400)

class TweetcreateAPIView(generics.CreateAPIView):
	serializer_class = TweetModelSerializer
	permission_classes = [permissions.IsAuthenticated]



	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

class TweetDetailAPIView(generics.RetrieveAPIView):
	queryset = Tweets.objects.all()
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultPagination
	permission_classes = [permissions.AllowAny]

	def get_queryset(self, *args, **kwargs):
		tweet_id = self.kwargs.get("pk")
		qs = Tweets.objects.filter(pk=tweet_id)
		if qs.exists()  and qs.count() == 1:
			parent_obj = qs.first()
			qs1 = parent_obj.get_children()
			qs = (qs | qs1).distinct().extra(select={"parent_id_null": 'parent_id IS NULL'})
		return qs.order_by("-parent_id_null", 'timestamp')

class SearchTweetAPIView(generics.ListAPIView):
	queryset = Tweets.objects.all().order_by("-timestamp")
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultPagination

	def get_serializer_context(self, *args, **kwargs):
		context = super(SearchTweetAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	def get_queryset(self, *args, **kwargs):
		qs = self.queryset
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
					)
		return qs



class TweetListAPIView(generics.ListAPIView):
	serializer_class = TweetModelSerializer
	pagination_class = StandardResultPagination

	def get_serializer_context(self, *args, **kwargs):
		context = super(TweetListAPIView, self).get_serializer_context(*args, **kwargs)
		context['request'] = self.request
		return context

	
	def get_queryset(self, *args, **kwargs):
		requested_user = self.kwargs.get("username")
		if requested_user:
			# im_following = self.request.user.profile.get_following()
			# qs1 = Tweets.objects.filter(user__in=im_following).order_by("-timestamp")
			qs = Tweets.objects.filter(user__username=requested_user).order_by("-timestamp")
		else:
			im_following = self.request.user.profile.get_following()

			qs1 = Tweets.objects.filter(user__in=im_following).order_by("-timestamp")
			qs2 = Tweets.objects.filter(user=self.request.user)
			qs = (qs1 | qs2).distinct().order_by("-timestamp")
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
					)
		return qs