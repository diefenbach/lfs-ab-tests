# django imports
from django.conf.urls.defaults import *


urlpatterns = patterns('lfs_ab_tests.views',
    url(r'^targets-by-theme$', "targets_by_theme", name="lfs_ab_tests_targets_by_theme"),
    url(r'^all-targets$', "all_targets", name="lfs_ab_tests_all_targets"),
)
