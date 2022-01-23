import json

import requests
from requests_oauthlib import OAuth1
from rich import print

__copyright__ = "Copyright 2022 Daniel Tucker"
__license__ = """
    Copyright 2022 Daniel Tucker

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""


class Twitter:
    tweet_url = "https://api.twitter.com/2/tweets"

    @staticmethod
    def load_credentials(file_name: str) -> tuple[str, str, str, str]:
        """Returns the client key, client secret, api key, and api secret as a tuple."""
        with open(file_name, "r") as file_:
            json_content = json.load(file_)

            client_key = json_content["client_key"]
            client_secret = json_content["client_secret"]
            api_key = json_content["api_key"]
            api_secret = json_content["api_secret"]

        return client_key, client_secret, api_key, api_secret

    def __init__(self):
        client_key, client_secret, api_key, api_secret = Twitter.load_credentials("twitter_credentials.json")

        self.header = OAuth1(api_key, api_secret, client_key, client_secret, signature_type="auth_header",
                             callback_uri="https://github.com/Denyol")

    def tweet(self, text: str) -> json:
        """Returns twitter JSON response"""
        data = {"text": text}

        r = requests.post(Twitter.tweet_url, json=data, auth=self.header)
        print("[bold blue]Tweet posted:", r.content)

        return r.json()

    def delete(self, tweet_ids: list):
        url = "https://api.twitter.com/2/tweets/"

        for t_id in tweet_ids:
            print("Deleting", t_id)
            r = requests.delete(url + t_id, auth=self.header)
            print(r.text, r.status_code)
