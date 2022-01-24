import datetime
from dataclasses import dataclass
import json
from hashlib import md5

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


@dataclass
class ExposureSite:
    times: str
    suburb: str
    address: str
    update_date: datetime.datetime

    def __init__(self, times: str, suburb: str, address: str, update_date: datetime.datetime):
        self.times = times.strip()
        self.suburb = suburb.strip()
        self.address = address.strip()
        self.update_date = update_date

    def __bytes__(self):
        return bytes(self.__str__(), "utf-8")

    def __str__(self):
        return self.times + "\n" + (
            ", ".join([self.suburb, self.address, "Updated: " + self.update_date.strftime("%d/%m/%Y")]))

    def hash_(self) -> str:
        """Returns a md5 hash representation of the object."""
        return md5(self.__bytes__()).hexdigest()

    def toJSON(self):
        """Returns a JSON string representation of the object."""
        return json.dumps(self.__dict__)
