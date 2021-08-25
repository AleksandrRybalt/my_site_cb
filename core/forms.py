from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from . import models


choices_currency = (
        ("AUD, Австралийского доллара, R01010", 'Австралийский доллар'),
        ("GBP, Фунта стерлингов Соединенного королевства, R01035", 'Фунт стерлингов Соединенного королевства'),
        ("BYN, Белорусских рублей, R01090", 'Белорусский рубль'),
        ("DKK, Датской кроны, R01215", 'Датская крона'),
        ("USD, Доллара США, R01235", 'Доллар США'),
        ("EUR, Евро, R01239", 'Евро'),
        ("CAD, Канадского доллара, R01350", 'Канадский доллар'),
        ("CHF, Швейцарского франка, R01775", 'Швейцарский франк'),
    )


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберете категорию'

    class Meta:
        model = models.PostsModel
        fields = ['title', 'slug', 'content', 'image', 'category', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'title-input'}),
            'slug': forms.TextInput(attrs={'class': 'slug-input'}),
            'content': forms.Textarea(attrs={'class': 'title-input', 'cols': 70, 'rows': 10}),
            'category': forms.Select(attrs={'class': 'form-select category'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'published-input'}),
        }



class AddUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'login-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'pass1-input'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'pass2-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'login-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'pass-input'}))


class RateForm(forms.Form):
    currency = forms.ChoiceField(choices=choices_currency, widget=forms.Select(
        attrs={'class': 'form-select currency', 'name': "currency"}),)
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': "date", 'name': "date"}))


class BikForm(forms.Form):
    bik = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control", 'name': "bik"}))


class CurrencyDynamicForm(forms.Form):
    currency = forms.ChoiceField(choices=choices_currency, widget=forms.Select(
        attrs={'class': 'form-select currency', 'name': "currency"}))
    start_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': "date", 'name': "start_date"}))
    end_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': "date", 'name': "end_date"}))


class PreciousMetalsForm(forms.Form):
    choices_metals = (
        ("1, Золота", 'Золото'),
        ("2, Серебра", 'Серебро'),
        ("3, Платины", 'Платина'),
        ("4, Палладия", 'Палладий'),
    )
    metal = forms.ChoiceField(choices=choices_metals, widget=forms.Select(
        attrs={'class': 'form-select currency', 'name': "metal"}))
    start_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': "date", 'name': "start_date"}))
    end_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': "date", 'name': "end_date"}))
