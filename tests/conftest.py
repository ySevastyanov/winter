import django
from django.conf import settings

from .entities import Guest


def pytest_configure():

    settings.configure(
        ROOT_URLCONF='tests.urls',
        REST_FRAMEWORK={
            'DEFAULT_RENDERER_CLASSES': ('winter_django.renderers.JSONRenderer',),
            'UNAUTHENTICATED_USER': Guest,
        },
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    'debug': True,  # We want template errors to raise
                },
            },
        ],
        INSTALLED_APPS=(
            'tests',
        ),
    )

    import winter.web
    import winter_openapi

    django.setup()
    winter.web.setup()
    winter_openapi.setup()
