import requests
from services.general.helpers.base_helper import BaseHelper


class GradesHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"
    GRADES_STATS_ENDPOINT = f"{ENDPOINT_PREFIX}/stats/"
    GRADES_CREATE_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def get_grades_stats(self, params: dict) -> requests.Response:
        response = self.api_utils.get(endpoint_url=self.GRADES_STATS_ENDPOINT, params=params)
        return response

    def post_create_grades(self, data: dict) -> requests.Response:
        response = self.api_utils.post(endpoint_url=self.GRADES_CREATE_ENDPOINT, data=data)
        return response
