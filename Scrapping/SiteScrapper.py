import requests

success_codes = [200, 201, 202, 204]

class SiteScrapper:
    def __init__(self, url: str):
        self.url = url

    def fetch_content(self):
        # Logic to fetch content from the URL
        response = requests.get(self.url)
        if(response.status_code in success_codes):
            return response.text
        pass