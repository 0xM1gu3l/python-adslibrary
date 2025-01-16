import requests
import json

class SearchResult():
    def __init__(self, data):
        if data["type"] == "query":
            self.type = data["type"]
            self.ad_count = data["ad_count"]
            self.page_names = data["page_names"]
            self.page_ids = data["page_ids"]
            self.date_range = data["date_range"]
            self.ads = data["ads"]
        if data["type"] == "page":
            self.type = data["type"]
            self.ad_count = data["ad_count"]
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
        if type == "page":
            self.variables["searchType"] = "page"
            self.variables["viewAllPageIDs"] = kwargs["page_id"]
        if type == "query":
            self.variables["queryString"] = kwargs["query"]
            self.variables["searchType"] = "KEYWORD_UNORDERED"
            self.variables["viewAllPageID"] = "0"
        if "date_min" in kwargs and "date_max" in kwargs:
            date_range = {
                "date_start": kwargs["date_min"],
                "date_end": kwargs["date_max"],
            }
            self.variables["startDate"] = date_range
        else:
            date_range = None
        data = {"variables": json.dumps(self.variables), "doc_id": self.docID}
        r = requests.post(self.base_url, data=data)
        response_data = json.loads(r.text.split("\n")[1])

        ad_count = response_data["data"]["ad_library_main"][
            "search_results_connection"
        ]["count"]
        page_names = []
        page_ids = []

        for ad in response_data["data"]["ad_library_main"]["search_results_connection"][
            "edges"
        ]:
            if ad["node"]["collated_results"][0]["page_name"] not in page_names:
                page_names.append(ad["node"]["collated_results"][0]["page_name"])
            if ad["node"]["collated_results"][0]["page_id"] not in page_ids:
                page_ids.append(ad["node"]["collated_results"][0]["page_id"])
        if type == "query":
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
        if type == "page":
            return SearchResult({
                "type": type,
                "ad_count": ad_count,
                "date_range": date_range,
                "ads": response_data["data"]["ad_library_main"][
                    "search_results_connection"
                ]["edges"],
            })