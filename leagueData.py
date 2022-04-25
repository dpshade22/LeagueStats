import requests
import pandas as pd

header = {"X-Riot-Token": "RGAPI-9c25c780-777b-400d-961d-bdfdda5016d7"}

matchesDF = pd.DataFrame()

matchesDF["MatchID"] = []
matchesDF["ChampionID"] = []
matchesDF["PartnerChampionID"] = []
matchesDF["Win/Lost"] = []


def getSummoner(summoner):
    summoner = requests.get(
        f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}",
        headers=header,
    )
    return summoner.json()


def getMatchIDs(puuid):
    matchIDs = requests.get(
        f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=75",
        headers=header,
    )
    return matchIDs.json()


def getMatch(matchID):
    matches = requests.get(
        f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchID}",
        headers=header,
    )
    return matches.json()


class Summoner:
    def __init__(self, summonerName):
        self.name = summonerName
        self.puuid = getSummoner(summonerName)["puuid"]
        self.matchIDs = getMatchIDs(self.puuid)
        self.partnerName = ""
        self.partnerPuuid = ""

    def initPartner(self, partnerName):
        r = getSummoner(partnerName)
        self.partnerPuuid = r["puuid"]
        self.partnerName = r["name"]

        for matchID in self.matchIDs:
            matchJSON = getMatch(matchID)
            participants = matchJSON["info"]["participants"]

            if self.partnerPuuid in matchJSON["metadata"]["participants"]:
                myNdx = 0
                partnerNdx = 0

                while participants[myNdx]["summonerName"] != self.name:
                    myNdx += 1
                while participants[partnerNdx]["summonerName"] != self.partnerName:
                    partnerNdx += 1

                me = participants[myNdx]
                partner = participants[partnerNdx]

                myChampion = me["championId"]
                partnersChampion = partner["championId"]

                if me["win"]:
                    win = 1
                else:
                    win = 0

                newMatch = pd.Series(
                    [
                        matchID, myChampion, partnersChampion, win
                    ],
                    index=["MatchID", "ChampionID",
                           "PartnerChampionID", "Win/Lost"],
                )

                matchesDF.append(newMatch, ignore_index=True)


dylan = Summoner("41619")
dylan.initPartner("yongbin")
