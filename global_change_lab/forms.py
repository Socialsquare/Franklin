from django import forms

class SignupForm(forms.Form):
    email = forms.CharField(max_length=100, label='Email')
    username = forms.CharField(max_length=30, label='Username')
    terms = forms.BooleanField(
        label='Terms and conditions',
        error_messages={'required': 'You must accept the terms and conditions'},
    )
    # password = forms.PasswordField(max_length=30, label='Password')

    def save(self, user):
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        # user.password = self.cleaned_data['password']
        user.save()
