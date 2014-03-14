from django import forms
from django.forms import widgets
from django.forms.models import fields_for_model, model_to_dict
from global_change_lab.models import User, UserInfo
from datetime import date

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


# From: https://docs.djangoproject.com/en/1.6/ref/forms/widgets/#django.forms.MultiWidget.format_output
class DateSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        # create choices for days, months, years
        # example below, the rest snipped for brevity.
        _widgets = (
            widgets.TextInput(attrs={'maxlength': '2', 'placeholder': 'DD'}),
            widgets.TextInput(attrs={'maxlength': '2', 'placeholder': 'MM'}),
            widgets.TextInput(attrs={'maxlength': '4', 'placeholder': 'YYYY'}),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.day, value.month, value.year]
        return [None, None, None]

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        print(data)
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        try:
            D = date(day=int(datelist[0]),
                     month=int(datelist[1]),
                     year=int(datelist[2]))
            return D
        except ValueError:
            return ''

        return None


class UserInfoForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        # Add these fields from the user object
        _fields = ('username', 'description')
        # Retrieve initial (current) data from the user object
        _initial = {}
        _instance = None

        if user is not None:
            _initial.update(model_to_dict(user, _fields))
            try:
                _instance = user.userinfo
                _initial.update(model_to_dict(_instance))
            except UserInfo.DoesNotExist:
                pass

        # Pass the initial data to the base
        super(UserInfoForm, self).__init__(initial=_initial, instance=_instance, *args, **kwargs)
        # Retrieve the fields from the user model and update the fields with it
        self.fields.update(fields_for_model(User, _fields))
        # Set description field to be required
        self.fields['description'].required = True

    class Meta:
        model = UserInfo
        exclude = ('user',)

    def save(self, *args, **kwargs):
        u = self.user
        u.username = self.cleaned_data['username']
        u.description = self.cleaned_data['description']
        userinfo = super(UserInfoForm, self).save(*args,**kwargs)
        userinfo.user = u
        userinfo.save()
        # u.userinfo = userinfo
        u.save()
        return userinfo

    # username = forms.CharField(max_length=30, label='Username')
    # email = forms.CharField(max_length=100, label='Email')

    sex = forms.ChoiceField(choices=UserInfo.SEXES, widget=forms.RadioSelect(), required=True)
    birthdate = forms.DateField(widget=DateSelectorWidget, required=True)
    # country = forms.CharField(max_length=80, label='Country')

    # birthday_day   = forms.CharField(max_length=80, label='Country')
    # birthday_month = forms.CharField(max_length=80, label='Country')
    # birthday_year  = forms.CharField(max_length=80, label='Country')

    # organization = forms.CharField(max_length=140, label='Organization')

