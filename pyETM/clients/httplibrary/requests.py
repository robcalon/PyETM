import os
import io
import logging
import requests

from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class RequestsCore:
    
    @property
    def beta_engine(self):
        return self.__beta_engine
        
    @beta_engine.setter
    def beta_engine(self, boolean):

        # check instance
        if not isinstance(boolean, bool):
            raise TypeError('beta_engine must be a boolean')
            
        # set boolean
        self.__beta_engine = boolean
        
        # reset session
        self._reset_session()
    
    @property
    def proxies(self):
        return self.__proxies
    
    @proxies.setter
    def proxies(self, proxies):
        
        # get environment vars
        if proxies == "auto":
            proxies = {
                "http": os.environ.get("HTTP_PROXY"),
                "https": os.environ.get("HTTPS_PROXY")
            }
        
        # set proxies
        self.__proxies = proxies
    
    @property
    def base_url(self):
        """"base url for carbon transition model"""
        
        # return beta engine url
        if self.beta_engine:
            return "https://beta-engine.energytransitionmodel.com/api/v3"
        
        # return production engine url
        return "https://engine.energytransitionmodel.com/api/v3"
        
    def __make_url(self, url):
        """join url with base url"""
        return self.base_url + url
    
    def __handle_response(self, response, decoder=None):
        """handle API response"""
        
        ### SYMETRIC WITH AIOHTTP ###
        
        # check response
        if not response.ok:
            response.raise_for_status()
            
        if decoder == "json":
            return response.json()
        
        if decoder == "text":
            return response.text
        
        if decoder == "bytes":
            return io.BytesIO(response.content)
        
        return response        
        
    def post(self, url, decoder="json", **kwargs):
        """make post request"""
        
        # make target url
        url = self.__make_url(url)
        
        # post request
        with requests.Session() as session:
            with session.post(url=url, proxies=self.proxies, **kwargs) as resp:
                return self.__handle_response(resp, decoder=decoder)
                    
    def put(self, url, decoder="json", **kwargs):
        """make put request"""
        
        # make target url
        url = self.__make_url(url)
        
        # put request
        with requests.Session() as session:
            with session.put(url=url, proxies=self.proxies, **kwargs) as resp:
                return self.__handle_response(resp, decoder=decoder)

    def get(self, url, decoder="json", **kwargs):
        """make get request"""
        
        # make target url
        url = self.__make_url(url)

        # get request
        with requests.Session() as session:
            with session.get(url, proxies=self.proxies, **kwargs) as resp:
                return self.__handle_response(resp, decoder=decoder)
            
    def delete(self, url, decoder="json", **kwargs):
        """make delete request"""
        
        # make target url
        url = self.__make_url(url)

        # delete request
        with requests.Session() as session:
            with session.delete(url, proxies=self.proxies, **kwargs) as resp:
                return self.__handle_response(resp, decoder=decoder)
            
    def put_series(self, url, series, name=None, **kwargs):
        """put series object"""
        
        # set key as name
        if name is None:
            name = series.key

        # convert series to string
        data = series.to_string(index=False)
        form = {"file": (name, data)}
        
        return self.put(url, files=form, **kwargs)