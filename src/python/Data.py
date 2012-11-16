from WMCore.REST.Server import DatabaseRESTApi
from T0WmaDataSvc.DataHello import *

class Data(DatabaseRESTApi):
  """Server object for REST data access API."""
  def __init__(self, app, config, mount):
    """
    :arg app: reference to application object; passed to all entities.
    :arg config: reference to configuration; passed to all entities.
    :arg str mount: API URL mount point; passed to all entities."""
    DatabaseRESTApi.__init__(self, app, config, mount)
    self._add({ "hello": Hello(app, self, config, mount) })
