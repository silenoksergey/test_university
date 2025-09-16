import requests

from services.general.helpers.base_helper import BaseHelper


class TeachersHelper(BaseHelper):
    ENDPOINT_PREFIX = "/teachers"
    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"

    def post_teachers(self, json: dict) -> requests.Response:
        response = self.api_utils.post(endpoint_url=self.ROOT_ENDPOINT, json=json)
        return response
