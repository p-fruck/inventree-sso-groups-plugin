import json

from django.contrib.auth.models import Group

from allauth.socialaccount.signals import social_account_added, social_account_updated

from plugin import InvenTreePlugin
from plugin.mixins import SettingsMixin


class SsoGroupsPlugin(SettingsMixin, InvenTreePlugin):
    """Use docstrings for everything... pls
    """

    NAME = "SSO Groups Plugin"

    # metadata
    AUTHOR = "Philipp Fruck"
    DESCRIPTION = "WIP syncing SSO groups with InvenTree"
    PUBLISH_DATE = "2024-05-20"
    VERSION = "0.1.0"  # We recommend semver and increase the major version with each new major release of InvenTree
    WEBSITE = "https://github.com/p-fruck/inventree-sso-groups-plugin"
    LICENSE = "MIT"

    SETTINGS = {
        'GROUP_MAP': {
            'name': 'Group map',
            'description': 'Map SSO groups to local groups',
            'validator': json.loads,
            'default': '{}',
        },
        'GROUP_KEY': {
            'name': 'Group key',
            'description': 'The name of the groups claim attribute',
            'validator': str,
        },
    }

    def __init__(self):
        super().__init__()
        social_account_added.connect(self.ensure_sso_roles)
        social_account_updated.connect(self.ensure_sso_roles)
        
    def ensure_sso_roles(self, sender, **kwargs):
        extra_data = kwargs["sociallogin"].account.extra_data
        group_key = self.get_setting("GROUP_KEY")
        group_map = json.loads(self.get_setting("GROUP_MAP"))
        print(f"{group_map=}", flush=True)
        # map SSO groups to InvenTree groups
        groups = []
        for sso_group in extra_data[group_key]:
            groups.append(group_map[sso_group])
        # ensure user has groups
        user = kwargs["sociallogin"].user
        for group in groups:
            try:
                user.groups.get(name=group)
            except Group.DoesNotExist:
                # ToDo: Handle group not found
                print(f"Adding {group} to {user}", flush=True)
                user.groups.add(Group.objects.get(name=group))
        # ToDo: Remove leftover groups for user
        # print("="*77, flush=True)
        # print(extra_data, flush=True)
        # print(f"{user.groups=}", flush=True)
