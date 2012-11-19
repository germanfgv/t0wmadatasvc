from WMCore.REST.Server import RESTEntity, restcall, rows
from WMCore.REST.Tools import tools
from WMCore.REST.Validation import *
from T0WmaDataSvc.Regexps import *
from operator import itemgetter

class RunId(RESTEntity):
  """REST entity for retrieving an specific run."""
  def validate(self, apiobj, method, api, param, safe):
    """Validate request input data."""
    validate_str('id', param, safe, RX_RUNID, optional = False)

  @restcall
  @tools.expires(secs=300)
  def get(self,id):
    """Retrieve information from a specific run id.

    :arg int id: the run id number 
    :returns: the run information"""

    c, _ = self.api.execute("""select * from run where run_id = :id""", id = id)
    return c

class Run(RESTEntity):
   """REST entity for retrieving run information."""
   def validate(self, apiobj, method, api, param, safe):
     """Validate request input data."""
     validate_rx('match', param, safe, optional = True)

   @restcall
   @tools.expires(secs=300)
   def get(self, match):
     """Retrieve runs. The results aren't ordered in any particular way.

     :arg str match: optional regular expression to filter by *run_id*
     :returns: columns description followed by the sequence of rows of runs."""

     return self.api.query(match, lambda row: str(row[0]), """select * from run""")
