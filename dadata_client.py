from dadata import Dadata

class DadataClient:
    
    def __init__(self, token, secret, lang) -> None:
        self.client = Dadata(token, secret)
        self.lang = lang


    def get_suggestions(self, query: str) -> list:
        suggestions = []
        buffer = self.client.suggest('address', query, count = 20, language = self.lang, locations = [{'country':"*"}])
        for i in range(len(buffer)):
            suggestions.append(buffer[i]['value'])
        return suggestions
    

    def get_geolocate(self, full_address: str) -> dict:
        geolocate = {}
        buffer = self.client.clean('address', full_address)

        geolocate['address'] = full_address
        geolocate['long'] = buffer['geo_lon']
        geolocate['latitude'] = buffer['geo_lat']
        
        return geolocate

