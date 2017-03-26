import requests
import json

class SteamAPI:
    _steam_api = "http://api.steampowered.com/"
    _getowned = "IPlayerService/GetOwnedGames/v0001/"
    _playersummary = "ISteamUser/GetPlayerSummaries/v0002/"
    _recentlyplayed = "IPlayerService/GetRecentlyPlayedGames/v0001/"
    _userstatsforgame = "ISteamUserStats/GetUserStatsForGame/v0002/"
    _playerachievements = "ISteamUserStats/GetPlayerAchievements/v0001/"
    
    def __init__(self, key):
        self._key = key
        
    def get_account_summary(self, id64):
        payload = {"key":self._key,
                   "steamids":id64}
        r = requests.get(self._steam_api + self._playersummary,
                         params=payload)
        summary = json.loads(r.text)
        return summary["response"]["players"][0]

    def __get_games_json(self, id64):
        payload = {"key": self._key,
			       "steamid": id64,
			       "include_appinfo":1}
        r = requests.get(self._steam_api + self._getowned,
                         params=payload)
        return json.loads(r.text)
        
    def get_games(self, id64):
        return __get_games_json(id64)["response"]["games"]

    def get_games_count(self, id64):
        return __get_games_json(id64)["response"]["game_count"]

    def __get_recently_played_games_json(self, id64):
        payload = {"key":self._key,
                   "steamid":id64,
                   "format":"json"}
        r = requests.get(self._steam_api + self._recentlyplayed,
                         params=payload)
        return json.loads(r.text)
    
    def get_recently_played_games(self, id64):
        return self.__get_recently_played_games_json(id64)["response"]["games"]

    def get_recently_played_games_count(self, id64):
        return self.__get_recently_played_games_json(id64)["response"]["total_count"]

    def __get_user_stats_for_game(self, appid, id64):
        payload = {"appid":appid,
                   "key":self._key,
                   "steamid":id64}
        r = requests.get(self._steam_api + self._userstatsforgame,
                         params=payload)
        return json.loads(r.text)
    
    def get_user_stats_for_game_stats(self, appid, id64):
        data = self.__get_user_stats_for_game(appid, id64)["playerstats"]["stats"]
        dictionary = dict(zip([item["name"] for item in data],
                              [item["value"] for item in data]))
        return dictionary

    def get_player_achievements(self, appid, id64):
        payload = {"appid":appid,
                   "key":self._key,
                   "steamid":id64}
        r = requests.get(self._steam_api + self._playerachievements,
                         params=payload)
        data = json.loads(r.text)["playerstats"]["achievements"]
        dictionary = dict(zip([item["apiname"] for item in data],
                              [item["achieved"] for item in data]))
        return dictionary
