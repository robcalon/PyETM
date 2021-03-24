import io
import pandas

class HourlyElectricityPriceCurve:
    
    @property
    def hourly_electricity_price_curve(self):
        
        # get hourly electricity price curve
        if self._hourly_electricity_price_curve is None:
            self.get_hourly_electricity_price_curve()
        
        return self._hourly_electricity_price_curve
            
    def get_hourly_electricity_price_curve(self):
        """get the hourly electricity price curve"""
        
        # raise without scenario id
        self._raise_scenario_id()
        
        # prepare post
        headers = {'Connection':'close'}
        post = f'/scenarios/{self.scenario_id}/curves/electricity_price'
        
        # request response and convert to df
        resp = self.get(post, headers=headers)
        curves = pandas.read_csv(io.StringIO(resp))
        
        # set corresponsing parameter property
        self._hourly_electricity_price_curve = curves
        
        return curves