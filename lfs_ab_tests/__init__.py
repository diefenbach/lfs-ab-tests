# python imports
import random
import re
import urlparse

from threading import local
_thread_locals = local()

# django imports
from django.conf import settings
from django.dispatch import receiver
from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader

# lfs imports
from lfs.core.signals import order_submitted


def get_current_request():
    return getattr(_thread_locals, 'request', None)


class Loader(BaseLoader):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        request = get_current_request()
        if request is None:
            raise TemplateDoesNotExist(template_name)

        theme = request.session.get("ab_tests")
        if not theme:
            theme = self.get_theme(request)
            request.session["ab_tests"] = theme

        if theme == "a":
            raise TemplateDoesNotExist(template_name)
        else:
            template_name = "%s/%s/%s" % (settings.LFS_AB_TESTS_DIRECTORY, theme, template_name)
            try:
                return open(template_name).read(), template_name
            except IOError:
                raise TemplateDoesNotExist(template_name)

    def get_theme(self, request):
        """
        Returns the theme for the given request.
        """
        from lfs_ab_tests.models import ThemeInformation

        themes = getattr(settings, "LFS_AB_TESTS_THEMES", [])
        for i, theme in enumerate(themes):
            theme, frequency = theme.split(":")
            try:
                frequency = int(frequency)
            except ValueError, TypeError:
                frequency = 1

            ti, created = ThemeInformation.objects.get_or_create(theme=theme)

            if created:
                return theme
            else:
                if ti.count < frequency:
                    ti.count += 1
                    ti.save()
                    return theme

        ThemeInformation.objects.all().delete()
        return self.get_theme(request)


class ABTestsMiddleware(object):
    def process_request(self, request):
        """
        Stores information when a target has been reached.
        """
        from lfs_ab_tests.models import TargetInformation
        _thread_locals.request = request

        theme = request.session.get("ab_tests", "-")
        source_url = request.META.get("HTTP_REFERER", "-")
        if source_url != "-":
            source_url = urlparse.urlparse(source_url).path
        destination_url = request.META.get("PATH_INFO", "-")

        for source, destination in getattr(settings, "LFS_AB_TESTS_TARGETS", []):
            if re.search(source, source_url) and re.search(destination, destination_url):
                TargetInformation.objects.create(
                    source = source,
                    destination = destination,
                    source_url = source_url,
                    destination_url = destination_url,
                    theme = theme,
                )
                break


@receiver(order_submitted)
def set_theme(sender, **kwargs):
    """
    Saves the current theme to new orders.
    """
    order = sender.get("order")
    request = sender.get("request")

    from lfs_ab_tests.models import OrderInformation
    OrderInformation.objects.create(order=order, theme=request.session.get("ab_tests", "-"))
