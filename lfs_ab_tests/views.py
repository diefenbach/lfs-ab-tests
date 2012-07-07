# django imports
from django.conf import settings
from django.db import connection
from django.db.models import Count
from django.shortcuts import render_to_response
from django.template import RequestContext

# lfs_ab_tests imports
from lfs_ab_tests.models import TargetInformation


def targets_by_theme(request, template_name="lfs_ab_tests/targets_by_theme.html"):
    """
    Returns a report with targets by theme.
    """
    targets = []
    for source, destination in getattr(settings, "LFS_AB_TESTS_TARGETS", []):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT source, destination, source_url, destination_url, theme, count(*)
            FROM lfs_ab_tests_targetinformation
            WHERE source = '%s'
            AND destination = '%s'
            GROUP BY source, destination, theme""" % (source, destination))

        for row in cursor.fetchall():
            targets.append({
                "source": row[0],
                "destination": row[1],
                "source_url": row[2],
                "destination_url": row[3],
                "theme": row[4],
                "amount": row[5],
            })

    return render_to_response(template_name, RequestContext(request, {
        "targets" : targets,
    }))


def all_targets(request, template_name="lfs_ab_tests/all_targets.html"):
    """
    Returns a report with all targets.
    """
    targets = []
    for source, destination in getattr(settings, "LFS_AB_TESTS_TARGETS", []):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT source, destination, source_url, destination_url, theme
            FROM lfs_ab_tests_targetinformation
            WHERE source = '%s'
            AND destination = '%s'""" % (source, destination))

        for row in cursor.fetchall():
            targets.append({
                "source": row[0],
                "destination": row[1],
                "source_url": row[2],
                "destination_url": row[3],
                "theme": row[4],
            })

    return render_to_response(template_name, RequestContext(request, {
        "targets" : targets,
    }))
