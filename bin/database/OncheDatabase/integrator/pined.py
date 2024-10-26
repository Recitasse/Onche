from datetime import datetime
from dataclasses import dataclass
from bin.database.OncheDatabase.link.link import Link


@dataclass(init=False)
class PinedIntegrator(Link):
    def insert_pined(self, ) -> None:
        query = 'INSERT INTO pined () VALUES ()'
        params = ()
        self.QUERY(query=query, values=params)
