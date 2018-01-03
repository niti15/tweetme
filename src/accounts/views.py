# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Userprofile
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from .forms import UserRegisterForm


# Create your views here.

User = get_user_model()

class UserRegisterView(FormView):
  template_name = 'accounts/user_register_form.html'
  form_class = UserRegisterForm
  success_url = '/login'

  def form_valid(self,form):
    #form.send_email()
    username = form.cleaned_data.get("username")
    email = form.cleaned_data.get("email")
    password = form.cleaned_data.get("password")
    new_user = User.objects.create(username=username, email=email)
    new_user.set_password(password)
    new_user.save()
    return super(UserRegisterView, self).form_valid(form)

class UserDetailView(DetailView):
  print("UserDetailView1")
  queryset = User.objects.all()
  #SSprint(queryset)
  template_name = 'accounts/user_detail.html'


  def get_object(self):
    return get_object_or_404(User, username__iexact=self.kwargs.get("username"))

  def get_context_data(self, *args, **kwargs):
    context = super(UserDetailView, self).get_context_data(*args, **kwargs)
    following = Userprofile.objects.is_following(self.request.user, self.get_object())
    context['following'] = Userprofile.objects.is_following(self.request.user, self.get_object())
    context['recommended'] = Userprofile.objects.recommended(self.request.user)
    return context


class UserFollowView(View):

  def get(self, request, username, *args, **kwargs):
    toggle_user = get_object_or_404(User, username__iexact=username)
    if request.user.is_authenticated():
     is_following = Userprofile.objects.toggle_follow(request.user, toggle_user)
# user_profile, created = Userprofile.objects.get_or_create(user=request.user)
# if toggle_user in user_profile.following.all():
# 	user_profile.following.remove(toggle_user)
# else:
# 	user_profile.following.add(toggle_user)
    return redirect("profiles:detail", username=username)



