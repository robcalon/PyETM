import io
import pandas

class EnergyFlows:
    
    @property
    def energy_flows(self):
        
        # get energy flows
        if self._energy_flows is None:
            self.get_energy_flows()
        
        return self._energy_flows
    
    def get_energy_flows(self, **kwargs):
        """get the energy flows"""

        # raise without scenario id
        self._raise_scenario_id()
        
        # prepare post
        headers = {'Connection':'close'}
        post = f'/scenarios/{self.scenario_id}/energy_flow'
        
        # request response and convert to df
        resp = self.get(post, headers=headers, **kwargs)
        flows = pandas.read_csv(io.StringIO(resp))
        
        # set corresponsing parameter property
        self._energy_flows = flows

        return flows