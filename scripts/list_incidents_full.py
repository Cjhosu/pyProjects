import requests
import os
from datetime import datetime, timedelta

api_key_from_env = os.environ.get('PDAPI_DATABASE')
API_KEY = api_key_from_env
last_hour = (datetime.now() - timedelta(days=1)).isoformat()
SINCE = last_hour
UNTIL = ''
SERVICE_IDS = ['PSLDOMB']
LIMIT = '1'
TIME_ZONE = 'UTC'

class Incident:
    OFFSET = 0
    is_more = True

    def list_incidents(self):
        while self.is_more == True:
            url = 'https://api.pagerduty.com/incidents'
            headers = {
                'Accept': 'application/vnd.pagerduty+json;version=2',
                'Authorization': 'Token token={token}'.format(token=API_KEY)
            }
            payload = {
                'since': SINCE,
                'until': UNTIL,
                'service_ids[]': SERVICE_IDS,
                'time_zone': TIME_ZONE,
                'offset': self.OFFSET,
                'limit': LIMIT,
            }
            r = requests.get(url, headers=headers, params=payload)
            incident = r.json()
            try:
                incident_key = incident["incidents"][0]["incident_key"]
            except:
                return
            self.OFFSET += 1
            print(incident)
            self.is_more = incident["more"]


if __name__ == '__main__':
    Incident.list_incidents(Incident)
