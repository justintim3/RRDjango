from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = 'website'
    path = '/opt/python/current/app/website'
    default_app_config = 'website.apps.WebsiteConfig'
