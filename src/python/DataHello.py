from WMCore.REST.Server import RESTEntity, restcall, rows
from WMCore.REST.Tools import tools
from WMCore.REST.Validation import *
from T0WmaDataSvc.Regexps import *
import json

class Hello(RESTEntity):
  """REST entity describing the calling user."""
  def validate(self, apiobj, method, api, param, safe):
    """Validate request input data."""
    pass

  @restcall
  @tools.expires(secs=-1)
  def get(self):
    """Hello world api call.

    ``paramname``
      This is a paramater.

    :returns: world"""

    return json.dumps(rows(["world"]))
