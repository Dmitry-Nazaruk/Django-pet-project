from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from vote_app.models import Posts, Customuser, Comments


class RegForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_name = forms.CharField(max_length=100)
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    date_birth = forms.CharField(required=True)
    city = forms.CharField(required=True)
    # email = forms.EmailField(required=True)
    # date_of_birth = forms.DateField(required=True)
    # city = forms.CharField(required=True)

    class Meta:
       # model = User
        model = Customuser
        fields = ("email", "user_name", "first_name", "last_name", "password1", "password2", "date_birth", "city")

    def save(self, commit=True):
        user = super(RegForm, self).save(commit=False)
        user.user_name = self.cleaned_data["user_name"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.date_birth = self.cleaned_data["date_birth"]
        user.city = self.cleaned_data["city"]
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['body', 'title']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

class UpdateProfileForm(forms.ModelForm):
    email = forms.EmailField()
    user_name = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    date_birth = forms.DateField()
    city = forms.CharField(max_length=100)

    class Meta:
        model = Customuser
        fields = ['email', 'user_name', 'first_name', 'last_name', 'date_birth', 'city']