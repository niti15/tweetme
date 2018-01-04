from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your tests here.

from .models import Tweets

User = get_user_model()

class TweetModeTestCase(TestCase):
	def setUp(self):
		some_random_user = User.objects.create(username='apple')

	def test_tweet_item(self):
		obj = Tweets.objects.create(
			user= User.objects.first(),
			content= 'Some Random Content'
			)
		self.assertTrue(obj.content == "some random content")
		self.assertTrue(obj.id == 1)
		absolute_url = reverse("tweet:detail", kwargs={"pk": 1})
		self.assertEqual(obj.get_absolute_url(), absolute_url)

	def  test_tweet_url(self):
		obj = Tweets.objects.create(
		user= User.objects.first(),
		content= 'Some Random Content')
		absolute_url = reverse("tweet:detail", kwargs={"pk": 1})
		self.assertEqual(obj.get_absolute_url(), absolute_url)
