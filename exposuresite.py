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
    update_date: datetime

    def __bytes__(self):
        return bytes(self.__str__(), "utf-8")

    def __str__(self):
        return self.times.strip() + "\n" + (
            ", ".join([self.suburb.strip(), self.address.strip(), "Updated: " + self.update_date.strftime("%d/%m/%Y")]))

    def hash_(self) -> str:
        return md5(self.__bytes__()).hexdigest()

    def toJSON(self):
        return json.dumps(self.__dict__)
