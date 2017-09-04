from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import ugettext_lazy as _

class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password'].help_text = ''
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

class SignUpForm(UserCreationForm):
    error_messages = {
                         'unique_email': _("Email already exists."),
                     },

    first_name = forms.CharField(max_length=30, label="First Name", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your First Name ...'
    }))
    last_name = forms.CharField(max_length=30, label="Last Name", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Last Name ...'
    }))
    email = forms.EmailField(max_length=254, label="Email", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Email ...'
    }))
    contact_no = forms.CharField(max_length=10, label="Contact-No.", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Contact No ...'
    }))

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email', 'contact_no', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Your UserName...'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Your Password...'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Your Password...'})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
               _("The two password fields didn't match.")
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                _("Email already exists.")
            )

        return email

class ChangePasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):

        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        # self.fields['old_password'].help_text = ''
        # self.fields['new_password1'].help_text = ''
        # self.fields['new_password2'].help_text = ''
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Old password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New password confirmation'})

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        print(old_password)
        print(self.user)
        if not self.user.check_password(old_password):
            raise forms.ValidationError(

                _("Your old password was entered incorrectly. Please enter it again.")
            )
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        print(password1)
        print(password2)
        print(self.user)
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    _("The two password fields didn't match.")
                )
        password_validation.validate_password(password2, self.user)
        return password2


