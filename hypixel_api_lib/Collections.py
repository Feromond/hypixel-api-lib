import requests
import pandas as pd

URL = r"https://api.hypixel.net/v2/resources/skyblock/collections"

class Collections():
    def __init__(self) -> None:
        self._dataset = self._get()
    
    def _get(self) -> None:
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




class Unlock():
    def __init(self, num: int, descr: str):
        self.num = num
        self.descr = descr

class Tier():
    def __init__(self, num: int, amount_requried: str, unlocks: list[Unlock]):
        self.tier_num = num
        self.amount_required = amount_requried
        self.unlocks = unlocks

class Collection():
    def __init__(self, item_name: str, max_tiers: int, tiers: list[Tier]):
        self.item_name = item_name
        self.max_tiers = max_tiers
        self.tiers = tiers




'''
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
'''
    