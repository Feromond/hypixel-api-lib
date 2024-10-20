
import pandas as pd
import requests
import json
import numpy as np

URL = r"https://api.hypixel.net/v2/resources/skyblock/election"






class Perk:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

class Minister:
    def __init__(self, key: str, name: str, perk: Perk):
        self._key = key
        self._name = name
        self._perk = perk
        self.minister = True    # putting this here


class Mayor:
    def __init__(self, key: str, name: str, perks: list[Perk], minister: Minister) -> None:
        self._key = key
        self._name = name
        self._perks = perks
        self._minister = minister

        





class Elections:
    def __init__(self) -> None:
        self._data = self.get_data()
        mayor = self._data["mayor"]
        perks = [Perk(i["name"], i["description"]) for i in  mayor["perks"]]
        minister = mayor["minister"]
        min_perk = minister["perk"]
        minister = Minister(minister["key"], minister["name"], Perk(min_perk["name"], min_perk["description"])) # type swithc fuck em
        self._mayor = Mayor(mayor["key"], mayor["name"], perks, minister)



        


    def get_data(self):
        try:
            response = requests.get(URL)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        





def main():
    e = Elections()
    minister = e._mayor._minister
    print(minister._key)
    print(minister._perk.name)

if __name__ == "__main__":
    main()