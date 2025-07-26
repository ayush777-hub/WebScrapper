from requests import request

from SearchEngines.BaseSearchEngine import BaseSearchEngine

class SearchAggregator:
    def __init__(self, search_engines: list[BaseSearchEngine]):
        self.search_engines = search_engines

    def GetSitesToScrape(self, query)->list[str]:
        results = []
        for engine in self.search_engines:
            response = request("GET", 
                               engine.url, 
                               params= GetQueryParams(engine, query))
            if response.status_code == 200:
                jsonResponse = response.json()
                if 'items' in jsonResponse:
                    if isinstance(jsonResponse['items'], list):
                        for item in jsonResponse['items']:
                            results.append(item['link'])
        return results
    

def GetQueryParams(engine: BaseSearchEngine, query: str):
    engineQuery: dict[str, str] = engine.GetQueryParams()

    return { 'q': query, **engineQuery }