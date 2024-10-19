
import pandas as pd
import requests
import json
import numpy as np

URL = r"https://api.hypixel.net/v2/resources/skyblock/election"




class Perk:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

class Mayor:
    def __init__(self, key: str, name: str, perks: list[Perk]) -> None:
        self._key = key
        self._name = name
        self._perks = perks

        





class Elections:
    def __init__(self) -> None:
        self._data = self.get_data()
        mayor = self._data["mayor"]
        perks = [Perk(i["name"], i["description"]) for i in  mayor["perks"]]
        self._mayor = Mayor(mayor["key"], mayor["name"], perks)
        


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
    mayor = e._mayor
    for i in mayor._perks:
        print(i.description)


if __name__ == "__main__":
    main()