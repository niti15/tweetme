from django import forms


from .models import Tweets

class TweetModelForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(
    attrs={'placeholder': "Your Message",
    'class': "form-control"
    }       ))
    
    class Meta:
        model = Tweets
        fields = [
        # "user",
        "content"
        ]


    # def clean_content(self, *args, **kwargs):
    #    content = self.cleaned_data.get("content")

    #    if content == "abc":
    # 	 raise forms.ValidationError("Cannot be ABC")
    #    return content
