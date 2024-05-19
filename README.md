# InvenTree SSO Groups Plugin

This plugin allows to sync your SSO groups with InvenTree and is currently considered being in draft state.

## Usage

This plugin isn't packaged yet, just take the `src/inventree_sso_groups/SsoGroupsPlugin.py` and throw it into your `data/plugins` folder.

## Configuration

The plugin must be enabled in the InvenTree settings and must receive the following two config options:

`GROUP_KEY`: The name of the claim containing all groups, e.g. `groups` or `roles`

`GROUP_MAP`: A mapping from SSO groups to InvenTree groups as JSON, e.g. `{"/inventree/admins": "admin"}`


### Keycloak

This plugin has been tested with Keycloak and OIDC. The steps below describe how to sync Keycloak Groups with InvenTree.

To handle authorization centrally, groups can be created and assigned directly in Keycloak. Those groups are not sent to the OIDC client by default. To enable such functionality, create a new client scope named `groups`. For this scope, add a new mapper ('By Configuration') and select 'Group Membership'. Give it a descriptive name and set the token claim name to `groups`.

For each client that relies on those group, explicitly add the `groups` scope to client scopes. The groups will now be sent to client upon request.

**Note:** A group named `foo` will be displayed as `/foo`. For this reason, I recommend using group names like `appname/rolename` which will be sent to the client as `/appname/rolename`.
