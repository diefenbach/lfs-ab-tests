# django imports
from django.db import models
from django.utils.translation import ugettext as _

# lfs imports
from lfs.order.models import Order


class OrderInformation(models.Model):
    """
    Saves ab test information to orders.
    """
    order = models.ForeignKey(Order, verbose_name=_(u"Order"))
    theme = models.CharField(_(u"Theme"), max_length=100)


class TargetInformation(models.Model):
    """Saves information for a target
    """
    source = models.CharField(_("Target"), max_length=200)
    destination = models.CharField(_(u"Destination"), max_length=200)
    source_url = models.CharField(_(u"Source"), max_length=200)
    destination_url = models.CharField(_(u"Source"), max_length=200)
    theme = models.CharField(_(u"Theme"), max_length=100)
    creation_date = models.DateTimeField(_(u"Creation Date"), auto_now_add=True)


class ThemeInformation(models.Model):
    """Saves information for selecte themes
    """
    theme = models.CharField(_(u"Theme"), max_length=100)
    count = models.PositiveSmallIntegerField(_(u"Count"), default=1)
    creation_date = models.DateTimeField(_(u"Creation Date"), auto_now_add=True)
