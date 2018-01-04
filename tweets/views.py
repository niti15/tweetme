from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import (
	DetailView,  
	ListView, 
	CreateView, 
	UpdateView,
	DeleteView,
	)
			
from .models import Tweets

# from django import forms from django.forms.utils import ErrorList
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .forms import TweetModelForm
# Create your views here.

class RetweetView(View):
	def get(self, request, pk, *args, **kwargs):
		tweet = get_object_or_404(Tweets, pk=pk)
		if request.user.is_authenticated():
			new_tweet = Tweets.objects.retweet(request.user, tweet)
			return HttpResponseRedirect("/")
		return HttpResponseRedirect(tweet.get_absolute_url())

class TweetCreateView(FormUserNeededMixin, CreateView):

	form_class = TweetModelForm
	template_name = "tweets/create_view.html"
	#success_url = reverse_lazy("tweet:detail")

	
def tweet_create_view(request):

	form = TweetModelFormweet(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()

	context = {
		"form": form
	}
	return render(request, "tweets/create_view.html", context)

class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
	queryset = Tweets.objects.all()
	form_class = TweetModelForm
	template_name = "tweets/update_view.html"
	#success_url = "/tweet/"

class TweetDetailView(DetailView):
	
	 queryset = Tweets.objects.all()


class TweetDeleteView(LoginRequiredMixin, DeleteView):
	model = Tweets
	template_name = "tweets/delete_confirm.html"
	success_url = reverse_lazy("tweet:list") #revers()
 

class TweetListView(LoginRequiredMixin, ListView):
	 
	#SSqueryset = Tweets.objects.all()
	def get_queryset(self, *args, **kwargs):
		qs = Tweets.objects.all()
		print(self.request.GET)
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter(
				Q(content__icontains=query) |
				Q(user__username__icontains=query)
					)
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(TweetListView, self).get_context_data(*args, **kwargs)
		context['create_form'] = TweetModelForm()
		context['create_url'] = reverse_lazy("tweet:create")
		return context
	 

def tweet_detail_view(request, pk=None):
	#obj = Tweets.objects.get(id=id) #getting from DB
	obj = get_object_or_404(Tweets, pk=pk)
	print(obj)

	context = {
			"object": obj,
		
	}
	return render(request, "tweets/detail_view.html", context)

# def tweet_list_view(request):
# 	queryset =  Tweets.objects.all() 
# 	print(queryset)
# 	for obj in queryset:
# 		print(obj.content)
# 	context = {
# 			"object_list": queryset
# 	}
# 	#print(context)
# 	return render(request, "tweets/list_view.html", context)

#create view backup
# class TweetCreateView(LoginRequiredMixin, FormUserNeededMixin, CreateView):

# 	form_class = TweetModelForm
# 	template_name = "tweets/create_view.html"
# 	success_url = reverse_lazy("tweet:detail")
#  	login_url = "/admin/"
    # redirect_field_name = 'redirect_to'