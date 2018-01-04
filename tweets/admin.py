from django.contrib import admin

# Register your models here.
from .forms import TweetModelForm
from .models import Tweets



# admin.site.register(Tweets)

class TweetModelAdmin(admin.ModelAdmin):
	# form = TweetModelForm
	class Meta:
		model  = Tweets
		

admin.site.register(Tweets, TweetModelAdmin)