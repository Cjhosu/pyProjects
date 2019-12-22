import re
import requests

API_KEY = 'Ua9RwKUQnbKDNp5obJkw'

SINCE = '2019-12-18'
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
            incident_key = incident["incidents"][0]["incident_key"]
            self.key_serializer(self,incident_key)
            self.OFFSET += 1
            self.is_more = incident["more"]

    def key_serializer(self, incident_key):
        key_list = incident_key.split(';')
        #print(key_list)
        if ('event_source=service') in key_list:
            for item in key_list:
                pair = item.split('=')
                head , sep, tail = pair[1].partition('-')
                dictrep = {pair[0] : head}
                print(dictrep)
            print('\n')

if __name__ == '__main__':
    Incident.list_incidents(Incident)
