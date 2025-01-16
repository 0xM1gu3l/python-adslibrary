import requests
import json
from datetime import datetime, timedelta

class SearchResult():
    def __init__(self, data):
            self.type = data["type"]
            self.ad_count = data["ad_count"]
            self.page_names = data["page_names"]
            self.page_ids = data["page_ids"]
            self.date_range = data["date_range"]
            self.ads = data["ads"]

class AdsLibrary:
    def __init__(self, country, ad_category):

        ###############################
        #          VARIABLES          #
        ###############################

        self.base_url = "https://www.facebook.com/api/graphql/"
        self.docID = "8835744153171108"

        self.variables = {
            "activeStatus": "ACTIVE",
            "adType": ad_category,
            "audienceTimeframe": "LAST_7_DAYS",
            "bylines": [],
            "contentLanguages": [],
            "countries": [country],
            "country": country,
            "excludedIDs": [],
            "fetchPageInfo": False,
            "fetchSharedDisclaimers": False,
            "isTargetedCountry": False,
            "location": None,
            "mediaType": "ALL",
            "multiCountryFilterMode": None,
            "pageIDs": [],
            "potentialReachInput": [],
            "publisherPlatforms": [],
            "queryString": "",
            "regions": [],
            "searchType": "",
            "sortData": None,
            "source": None,
            "startDate": None,
            "v": "3a313b",
            "viewAllPageID": "0",
        }
        """
        Little docs here:
        if (viewAllPageId = 0 and searchType = KEYWORD_UNORDERED): type = query_search
        if (viewAllPageId != 0 and searchType = page): type = page_search
        """

    def search(self, type, **kwargs):
        # Verify kwargs
        # if type == "query" and kwargs["query"] == "":
        
        if type == "page":
            self.variables["searchType"] = "page"
            self.variables["viewAllPageID"] = kwargs["page_id"]
            self.variables["queryString"] = ""
        
        if type == "query":
            self.variables["queryString"] = kwargs["query"]
            self.variables["searchType"] = "KEYWORD_UNORDERED"
            self.variables["viewAllPageID"] = "0"
        
        if "date_min" in kwargs and "date_max" in kwargs:
            if kwargs["date_min"] == kwargs["date_max"]:
                print("Warning: Inserting the same date in both date_min and date_max will act like if you don't pass them, I'll add one day to date_max to get the ads in the day you specified")
                
                date_max = datetime.strptime(kwargs["date_max"], "%Y-%m-%d")
                date_max = date_max + timedelta(days=1)
                kwargs["date_max"] = date_max.strftime("%Y-%m-%d")
            
            date_range = {
                "min": kwargs["date_min"],
                "max": kwargs["date_max"],
            }
            self.variables["startDate"] = date_range
        else:
            date_range = None
        
        data = {"variables": json.dumps(self.variables), "doc_id": self.docID}
        r = requests.post(self.base_url, data=data)
        response_data = json.loads(r.text.split("\n")[1])

        ad_count = response_data["data"]["ad_library_main"]["search_results_connection"]["count"]
        page_names = []
        page_ids = []

        for ad in response_data["data"]["ad_library_main"]["search_results_connection"][
            "edges"
        ]:
            if ad["node"]["collated_results"][0]["page_name"] not in page_names:
                page_names.append(ad["node"]["collated_results"][0]["page_name"])
            if ad["node"]["collated_results"][0]["page_id"] not in page_ids:
                page_ids.append(ad["node"]["collated_results"][0]["page_id"])
        return SearchResult({
            "type": type,
            "ad_count": ad_count,
            "page_names": page_names,
            "page_ids": page_ids,
            "date_range": date_range,
            "ads": response_data["data"]["ad_library_main"][
                "search_results_connection"
            ]["edges"],
        })