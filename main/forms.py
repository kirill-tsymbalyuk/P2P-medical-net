from django import forms


class UserForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}))
    mail = forms.EmailField(required=True, widget=forms.TextInput(attrs={"placeholder": "Почта"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}))
