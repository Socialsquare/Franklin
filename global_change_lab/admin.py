from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from global_change_lab.models import User

# see: http://stackoverflow.com/questions/16391467/customise-useradmin-model
# and: http://stackoverflow.com/questions/15012235/using-django-auth-useradmin-for-a-custom-user-model

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

    exclude_fields = ['id', 'date_joined']
    print('user fields', exclude_fields)

    _all_fields = [f.name for f in User._meta.fields]
    _fields = list(set(_all_fields) - set(exclude_fields))

    # List comprehensions and lambdas in the class definition cannot use class
    # variables from the class definition. This is due to their scope rules.
    # See: http://stackoverflow.com/questions/13905741/accessing-class-variables-from-a-list-comprehension-in-the-class-definition
    # This means that the following will _not_ work:
    # _all_fields = [f.name for f in User._meta.fields if f.name not in exclude_fields]

    fieldsets = (
        (None, { 'fields':
            _fields
        }),
    )

    # Columns shown in admin
    list_display = ('username', 'email', 'is_superuser')
    # Filters shown in admin
    list_filter = ('is_superuser', )


admin.site.register(User, CustomUserAdmin)


from solo.admin import SingletonModelAdmin
from global_change_lab.models import SiteConfiguration

admin.site.register(SiteConfiguration, SingletonModelAdmin)

