import pandas as pd
import requests
import json
import numpy as np

URL = r"https://api.hypixel.net/v2/resources/skyblock/collections"

class Collections():


    def __init__(self, skills: list[str]) -> None:
        self._dataset = self._get(skills)
    
    def _get(self, skills: list[str]) -> None:
        raw_data = []
        response = requests.get(URL)
        req_body = None
        if response.status_code == 200:
            req_body = response.json()["collections"]
        
        else:
            pass #deal with this shit

        cols = None
        for k in req_body.keys():
            sub_body = req_body[k]["items"]
            for i in sub_body.keys():
                row = sub_body[i]
                skill = "skill"
                system_name = i
                if cols is None:
                    cols = [row, skill].extend([j for j in sub_body.keys()])
                sub_body[i]["skill"] = k
                sub_body[i]["sys_name"] = system_name
                raw_data.append(sub_body[i])

        return pd.DataFrame(raw_data, columns=cols)
    

    def get_names(self) -> list[str]:
        return self._dataset["name"].to_list()
    
    def get_sys_name(self) -> list[str]:
        return self._dataset["sys_name"].to_list()
    

    def get_dataframe(self) -> pd.DataFrame:
        return self._dataset.copy()
    

    def get_tiers_by_name(self, coll_name: str) -> dict:
        return self._dataset[self._dataset["name"] == coll_name]["tiers"].to_list()[0]

    
    def get_data_by_name(self, coll_name: str):
        return self._dataset[self._dataset["name"] == coll_name].to_dict()
    


