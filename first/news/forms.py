import re
from django.core.exceptions import ValidationError

from django import forms
from news.models import News, NewsComment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ['title', 'content', 'is_publishied', 'category']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                   'category': forms.Select(attrs={'class': 'form-control'})}

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        else:
            return title


class CommentForm(forms.ModelForm):

    class Meta:
        model = NewsComment
        fields = ['author', 'mail', 'content']
        widgets = {'author': forms.HiddenInput(),
                   'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                   'mail': forms.HiddenInput()}


class RegistrationForm(UserCreationForm):
    captcha = CaptchaField()
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Имя пользователя')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Электронная почта')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Введите пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Введите пароль повторно')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Пароль')
