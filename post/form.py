from django import forms
from .models import post,comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ('body',)


class Editepostform(forms.ModelForm):
    class Meta:
        model = post
        fields = ('body',)


class Addcommentform(forms.ModelForm):
    class Meta:
        model = comment
        fields = ('body',)
        error_messages={
            'body':{
                'required': 'این فیلد اجباری است',
        }
        }


class Addreplyform(forms.ModelForm):
    class Meta:
        model = comment
        fields = ('body',)

