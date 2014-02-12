Overridding admin and comments templates
----------------------------------------
The templates from app are loaded in the order specified in `INSTALLED_APPS`.
This means that if you put your custom admin templates in
`myapp/templates/admin`, then `myapp` should be listed before
`django.contrib.admin` in `INSTALLED_APPS`.

    # Won't work
    INSTALLED_APPS = (
        'django.contrib.admin',
        'myapp',
    )

    # Will work
    INSTALLED_APPS = (
        'myapp',
        'django.contrib.admin',
    )

Otherwise the default templates in `django.contrib.admin` will be found first
when searching for templates, and will be used instead of your custom templates.
