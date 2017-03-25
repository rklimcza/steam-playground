import requests
import json

class SteamAPI:
    _steam_api = "http://api.steampowered.com/"
    _getowned = "IPlayerService/GetOwnedGames/v0001/"
    _playersummary = "ISteamUser/GetPlayerSummaries/v0002/"
    
    def __init__(self, key):
        self._key = key
        
    def get_name(self, id64):
        payload = {"key":self._key,
                   "steamids":id64}
        r = requests.get(self._steam_api + self._playersummary,
                         params=payload)
        summary = json.loads(r.text)
        return summary["response"]["players"][0]["personaname"]
        
    def get_games(self, id64):
        payload = {"key": self._key,
			       "steamid": id64,
			       "include_appinfo":1}
        r = requests.get(self._steam_api + self._getowned,
                         params=payload)
        games = json.loads(r.text)
        return games["response"]["games"]
