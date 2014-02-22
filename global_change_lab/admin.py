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

    fieldsets = (
        (None, { 'fields': ('email',) }),
    )
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': (,)}),
    # )

    # Columns shown in admin
    list_display = ('username', 'email', )
    # Filters shown in admin
    list_filter = ('is_superuser', )


admin.site.register(User, CustomUserAdmin)


from solo.admin import SingletonModelAdmin
from global_change_lab.models import SiteConfiguration

admin.site.register(SiteConfiguration, SingletonModelAdmin)

