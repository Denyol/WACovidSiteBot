#!/usr/bin/env python3

import json

import requests
from bs4 import BeautifulSoup
import twitter
from exposuresite import ExposureSite
from rich.console import Console
from rich.table import Table
import datetime
import sys

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


class ExposureSiteBot:

    @staticmethod
    def get_post_history() -> dict:
        with open("post_history.json", "r") as f:
            json_file = json.load(f)

            return json_file["history"]

    @staticmethod
    def get_last_site_update_date() -> datetime.datetime:
        with open("post_history.json", "r") as f:
            json_file = json.load(f)

            date = json_file["last_site_updated"]

            return datetime.datetime.strptime(date, "%d/%m/%Y")

    @staticmethod
    def simple_date(date: datetime.datetime) -> str:
        """Returns the date in the form 'dd/mm/YYYY'"""
        return date.strftime("%d/%m/%Y")

    @staticmethod
    def remove_saved_post(tweet_id: str):
        with open("post_history.json", "r+") as file_:
            json_file = json.load(file_)

            history = json_file["history"]
            json_file["history"] = {key: val for key, val in history.items()
                                    if str(val) != tweet_id}

            file_.seek(0)

            json.dump(json_file, file_, indent=2)
            file_.truncate()

    def __init__(self):
        self.recent_updated = datetime.datetime(2000, 1, 1)
        self.exposure_sites = None
        self.console = Console()

    def post_sites(self):

        self.console.print("[blue]Fetching exposure sites")
        self.fetch_new_sites()

        tw = twitter.Twitter()
        last_updated = self.recent_updated

        if len(self.exposure_sites) > 0:
            post_history = {}
            last_hash = None

            for site in reversed(self.exposure_sites):

                tweet_text = str(site) + "\n" + site.hash_() + "\n" + "#WA #WACOVID #Perth"

                response = tw.tweet(tweet_text[0:250])

                try:
                    post_history[site.hash_()] = response["data"]["id"]
                    last_hash = site.hash_()
                except:
                    self.console.print("[red]Error occurred!")
                    self.console.print("[red]", response.get("errors"))
                    self.exposure_sites.remove(site)

            with open("post_history.json", "r+") as f:
                history = json.load(f)

                f.seek(0)

                history["last_site_updated"] = ExposureSiteBot.simple_date(last_updated)
                history["time"] = ExposureSiteBot.simple_date(datetime.datetime.now())
                history["history"].update(post_history)
                history["last post hash"] = last_hash

                json.dump(history, f, indent=2)
                f.truncate()

    def fetch_new_sites(self):

        self.exposure_sites = []

        last_site_updated = ExposureSiteBot.get_last_site_update_date()

        r = requests.get(
            "https://www.healthywa.wa.gov.au/Articles/A_E/Coronavirus/Locations-visited-by-confirmed-cases")
        soup = BeautifulSoup(r.text, 'html.parser')

        location_blocks = soup.find_all(id="mobileLocationList")

        table = Table(title="Exposure Sites", show_lines=True)
        table.add_column("Exposure Times")
        table.add_column("Suburb")
        table.add_column("Address")
        table.add_column("Updated:")
        table.add_column("Hash")

        posted_hashes = ExposureSiteBot.get_post_history().keys()

        for location in location_blocks:

            times, suburb, loc, updated = None, None, None, None
            for location_content in location.find_all(class_="content"):
                if "content2" in location_content.attrs["class"]:
                    suburb = location_content.text
                elif "content1" in location_content.attrs["class"]:
                    times = location_content.text
                elif "content3" in location_content.attrs["class"]:
                    loc = location_content.text
                elif "content4" in location_content.attrs["class"]:
                    updated = datetime.datetime.strptime(str.strip(location_content.text), "%d/%m/%Y")

            es = ExposureSite(times, suburb, loc, updated)

            curr_hash = es.hash_()
            if updated > last_site_updated or (updated == last_site_updated and curr_hash not in posted_hashes):

                if updated > self.recent_updated:
                    self.recent_updated = updated

                self.console.print("[red]Found new site:[normal]", str(es) + "\n", curr_hash)

                table.add_row(times, suburb, loc, ExposureSiteBot.simple_date(updated), curr_hash)

                self.exposure_sites.append(es)


def run():
    bot = ExposureSiteBot()
    console = Console()

    console.print("[blue]Finding new exposure sites and uploading to twitter!")
    bot.post_sites()


if __name__ == '__main__':

    args = sys.argv

    if len(args) > 1:
        if args[1] == "delete":
            if len(args) < 3:
                print("Incorrect syntax! Insert post ID.")
            else:
                twitter.Twitter().delete(args[2])
    else:
        run()
