from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder, Div


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD', required=False)
    about = forms.CharField(max_length=500)
    mobile = forms.CharField(max_length=10)
    address = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.helper = FormHelper()
        self.helper.layout = Layout(Div(
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'about',
            'mobile',
            'address',
            ButtonHolder(Submit('register', 'SignUp', css_class='btn-primary col-sm-offset-4')),
            css_class='col-sm-4 col-sm-offset-4'))

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(Div(
            'username',
            'password',
            ButtonHolder(Submit('login', 'LogIn', css_class='btn-primary col-sm-offset-4')),
            css_class='col-sm-4 col-sm-offset-4'
        ))