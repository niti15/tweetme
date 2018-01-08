from django.utils.timesince import timesince

from rest_framework import serializers

from accounts.api.serializers import UserDisplaySerializer

from tweets.models import Tweets
#from ..models import Tweet

class ParentTweetModelSerializer(serializers.ModelSerializer):
  user = UserDisplaySerializer(read_only=True) #write only
  date_display = serializers.SerializerMethodField()
  timesince = serializers.SerializerMethodField()
  likes = serializers.SerializerMethodField()
  did_likes = serializers.SerializerMethodField()
  class Meta:
    model = Tweets
    fields = [
            'id',
           'user',
           'content',
           'timestamp',
           'date_display',
           'timesince',
           'likes',
           'did_likes',
          
           
                   
      ] 


  def get_did_likes(self, obj):
        request = self.context.get("request")
        try:
          user = request.user
          if user.is_authenticated():
            if user in obj.liked.all():
              return True
        except:
          pass
        return False

  def get_likes(self, obj):
        return obj.liked.all().count()

  def get_date_display(self, obj):
    return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

  def get_timesince(self, obj):
    return timesince(obj.timestamp) + "ago"


 

class TweetModelSerializer(serializers.ModelSerializer):
      parent_id = serializers.CharField(write_only=True, required=False)
      user = UserDisplaySerializer(read_only=True) #write only
      date_display = serializers.SerializerMethodField()
      timesince = serializers.SerializerMethodField()
      likes = serializers.SerializerMethodField()
      did_likes = serializers.SerializerMethodField()
      parent = ParentTweetModelSerializer(read_only=True)
      class Meta:
      	model = Tweets
      	fields = [
                'id',
               'user',
               'content',
               'timestamp',
               'date_display',
               'timesince',
               'parent',
               'likes',
               'did_likes',
               'reply',
               'parent_id',  
          ]	

        # read_only_fields = ['reply']

      def get_did_likes(self, obj):
        request = self.context.get("request")
        try:
          user = request.user
          if user.is_authenticated():
            if user in obj.liked.all():
              return True
        except:
          pass
        return False


      def get_likes(self, obj):
        return obj.liked.all().count()

      def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

      def get_timesince(self, obj):
        return timesince(obj.timestamp) + "ago"