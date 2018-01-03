import re
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from hashtags.signals import parsed_hashtags
from django.db.models.signals import post_save
# from hashtag.models import

from django.conf import settings
from django.utils import timezone

# Create your models here.

from .validators import validate_content

class TweetManager(models.Manager):
  def retweet(self, user, parent_obj):
    if parent_obj.parent:
      og_parent = parent_obj.parent
    else:
      og_parent = parent_obj

    qs = self.get_queryset().filter(
      user=user, parent=og_parent
      ).filter(
          timestamp__year=timezone.now().year,
          timestamp__month=timezone.now().month,
          timestamp__day=timezone.now().day,

      )
    if qs.exists():
      return None

    qs = self.get_queryset().filter(user=user, parent=parent_obj)
    if qs.exists():
      return None;


    obj = self.model(
          parent = parent_obj,
          user = user,
          content = parent_obj.content,
      )
    obj.save()
    return obj

  def like_toggle(self, user, tweet_obj):
    if user in tweet_obj.liked.all():
      is_liked = False
      tweet_obj.liked.remove(user)
    else:
      is_liked = True
      tweet_obj.liked.add(user)
    return is_liked



class Tweets(models.Model):
  parent = models.ForeignKey("self", blank=True, null=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  content = models.CharField(max_length=140, validators=[validate_content])
  liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
  updated = models.DateTimeField(auto_now=True)
  reply = models.BooleanField(verbose_name='Is a reply?',default=False)
  timestamp = models.DateTimeField(auto_now_add=True)
  objects = TweetManager()

  def __str__(self):
	return str(self.content)

  def get_absolute_url(self):
  	return reverse("tweet:detail", kwargs={"pk":self.pk}) 	

  class Meta:
      ordering = ['-timestamp', 'content']	

  def get_parent(self):
    the_parent = self
    if self.parent:
      the_parent = self.parent
    return the_parent

  def get_children(self):
    parent = self
    if self.parent:
      parent = self.get_parent()
    return Tweets.objects.filter(parent=parent)
  # def clean(self, *args, **kwargs):
  #   content = self.content
  #   if content == "abc":
  #     raise ValidationError("Cannot be ABC")
  #   return super(Tweets, self).clean(*args, **kwargs)


def tweet_save_receiver(sender, instance, created, *args, **kwargs):
  if created and not instance.parent:
    # alert();
    user_regex = r'@(?P<username>[\w.@+-]+)'
    m = re.search(user_regex, instance.content)
    if m:
        username = m.group("username")
        # alert();
        print(username)


    hash_regex = r'#(?P<hashtag>[\w\d-]+)'
    h_m = re.search(hash_regex, instance.content)
    if h_m:
        hashtag = h_m.group("hashtag")
        parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtag)
        print(hashtag)



post_save.connect(tweet_save_receiver, sender=Tweets)
