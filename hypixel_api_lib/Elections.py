
import pandas as pd
import requests
import json
import numpy as np

URL = r"https://api.hypixel.net/v2/resources/skyblock/election"



class Perk:
    def __init__(self, name: str, description: str, minister: bool = None) -> None:
        self.name = name
        self.description = description
        self.minister = minister

class Minister:
    def __init__(self, key: str, name: str, perk: Perk):
        self._key = key
        self._name = name
        self._perk = perk

class Candidate:
    def __init__(self, key: str, name: str, perks: list[Perk], votes: int):
        self._key = key
        self._name = name
        self._perks = perks
        self._votes = votes


class Election:
    def __init__(self, year: int, candidates: list[Candidate]):
        self._year = year
        self._candidates = candidates



class Mayor:
    def __init__(self, key: str, name: str, perks: list[Perk], minister: Minister, election: Election) -> None:
        self._key = key
        self._name = name
        self._perks = perks
        self._minister = minister
        self._election = election

        





class Elections:
    def __init__(self) -> None:
        self._data = self.get_data()
        self._build_mayor()
        self._build_current()


    

    def _build_mayor(self):
        mayor = self._data["mayor"]
        perks = [Perk(i["name"], i["description"]) for i in  mayor["perks"]]
        minister = mayor["minister"]
        min_perk = minister["perk"]
        minister = Minister(minister["key"], minister["name"], Perk(min_perk["name"], min_perk["description"]
                                                                    , min_perk["minister"])) # type swithc fuck em
       
       
        election = mayor["election"]
        candidates = []
        for i in election["candidates"]:
            perks = [Perk(j["name"], j["description"], j["minister"]) for j in i["perks"]]
            candidates.append(Candidate(i["key"], i["name"], perks, i["votes"]))
        election = Election(election["year"], candidates)
        self._mayor = Mayor(mayor["key"], mayor["name"], perks, minister, election)


    def _build_current(self):
        current = self._data["current"]
        candidates = []
        for i in current["candidates"]:
            perks = [Perk(j["name"], j["description"], j["minister"]) for j in i["perks"]]
            candidates.append(Candidate(i["key"], i["name"], perks, i["votes"]))
        current = Election(current["year"], candidates)
        self._current = current


    def get_data(self):
        try:
            response = requests.get(URL)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        



