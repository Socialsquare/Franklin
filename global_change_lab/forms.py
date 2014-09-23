from django import forms
from django.forms import widgets
from django.forms.models import fields_for_model, model_to_dict
from global_change_lab.models import User, UserInfo
from datetime import date
from django.utils.safestring import mark_safe

class SignupForm(forms.Form):
    email = forms.CharField(max_length=100, label='Email')
    username = forms.CharField(max_length=30, label='Username')
    terms = forms.BooleanField(
        label=mark_safe('I agree to the <a href="/pages/terms-of-service/">Terms of Service</a> of Franklin'),
        error_messages={'required': 'You must accept the terms and conditions'}
    )
    # password = forms.PasswordField(max_length=30, label='Password')

    def signup(self, request, user):
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
    def __init__(self, *args, **kwargs):

        self.user = kwargs['instance']
        self.userinfo = self.user.userinfo

        _retrieve_fields = ('birthdate', 'sex', 'country', 'organization')

        # Retrieve initial (current) data from the User and UserInfo object
        _initial = {}
        #_initial.update(model_to_dict(self.user, _fields))
        _initial.update(model_to_dict(self.userinfo, _retrieve_fields))

        # Pass the initial data to the base
        super(UserInfoForm, self).__init__(initial=_initial, *args, **kwargs)

        # Add these automatically fields from the UserInfo object
        _add_fields = ('country', 'organization')
        self.fields.update(fields_for_model(UserInfo, _add_fields))

        # Set description field to be required
        self.fields['description'].required = True
        self.fields['username'].required = True
        self.fields['username'].unique = True
        self.fields['email'].unique = True

    class Meta:
        model = User
        fields = ('username', 'email', 'description')

    def save(self, *args, **kwargs):
        self.userinfo.birthdate = self.cleaned_data['birthdate']
        self.userinfo.sex = self.cleaned_data['sex']
        self.userinfo.country = self.cleaned_data['country']
        self.userinfo.organization = self.cleaned_data['organization']
        self.userinfo.save()
        user = super(UserInfoForm, self).save(*args,**kwargs)
        return user

    sex = forms.ChoiceField(choices=UserInfo.SEXES, widget=forms.RadioSelect(), required=True)
    birthdate = forms.DateField(widget=DateSelectorWidget, required=True)
    # country = forms.CharField(max_length=80, label='Country')

    # birthday_day   = forms.CharField(max_length=80, label='Country')
    # birthday_month = forms.CharField(max_length=80, label='Country')
    # birthday_year  = forms.CharField(max_length=80, label='Country')

    # organization = forms.CharField(max_length=140, label='Organization')

