# Copyright (c) 2012 Cloudera, Inc. All rights reserved.

try:
  import json
except ImportError:
  import simplejson as json

from cm_api.endpoints.types import config_to_json, json_to_config, BaseApiObject
from cm_api.endpoints.services import ApiService

class ApiLicense(BaseApiObject):
  """Model for a CM license."""
  RO_ATTR = ('owner', 'uuid', 'expiration')
  def __init__(self, resource_root):
    BaseApiObject.ctor_helper(**locals())

class ClouderaManager(BaseApiObject):
  """
  The Cloudera Manager instance.

  Provides access to CM configuration and services.
  """

  def __init__(self, resource_root):
    BaseApiObject.ctor_helper(**locals())

  def create_mgmt_service(self, service_setup_info):
    """
    Setup the Cloudera Management Service.

    @param service_setup_info: ApiServiceSetupInfo object.
    @return: The management service instance.
    """
    body = json.dumps(service_setup_info.to_json_dict())
    resp = self._get_resource_root().put('/cm/service', data=body)
    return ApiService.from_json_dict(resp, self._get_resource_root())

  def get_service(self):
    """
    Return the Cloudera Management Services instance.

    @return: An ApiService instance.
    """
    resp = self._get_resource_root().get('/cm/service')
    return ApiService.from_json_dict(resp, self._get_resource_root())

  def get_license(self):
    """
    Return information about the currently installed license.

    @return: License information.
    """
    resp = self._get_resource_root().get('/cm/license')
    return ApiLicense.from_json_dict(resp, self._get_resource_root())

  def update_license(self):
    """
    Install a new license.

    TODO: not yet implemented.
    """
    raise NotImplementedError

  def get_config(self, view = None):
    """
    Retrieve the Cloudera Manager configuration.

    The 'summary' view contains strings as the dictionary values. The full
    view contains ApiConfig instances as the values.

    @param view: View to materialize ('full' or 'summary')
    @return: Dictionary with configuration data.
    """
    resp = self._get_resource_root().get('/cm/config',
        params = view and dict(view=view) or None)
    return json_to_config(resp, view == 'full')

  def update_config(self, config):
    """
    Update the CM configuration.

    @param: config Dictionary with configuration to update.
    @return: Dictionary with updated configuration.
    """
    resp = self._get_resource_root().put('/cm/config',
        data = config_to_json(config))
    return json_to_config(resp, False)
