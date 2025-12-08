# API Client
import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get(self, endpoint):
        return requests.get(f'{self.base_url}/{endpoint}')
