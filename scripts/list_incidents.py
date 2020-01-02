import requests
import subprocess
import time
from datetime import datetime, timedelta

API_KEY = 'MyKey'
last_hour = (datetime.now() - timedelta(hours=2)).isoformat()
SINCE = last_hour
UNTIL = ''
SERVICE_IDS = ['PSLDOMB']
LIMIT = '1'
TIME_ZONE = 'UTC'

class Incident:
    OFFSET = 0
    is_more = True
    host_name = ''
    service_desc = ''

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
            self.key_serializer(self,incident_key)
            self.OFFSET += 1
            self.is_more = incident["more"]

    def key_serializer(self, incident_key):
        key_list = incident_key.split(';')
        if ('event_source=service') in key_list:
            for item in key_list:
                pair = item.split('=')
                head , sep, tail = pair[1].partition('-')
                dictrep = {pair[0] :head}
                self.set_metric(self, dictrep)
            bash = 'echo "production.dba_on_call_incident.'+self.service_desc+'.'+self.host_name+':1|s" | nc -u -w1 production.statsd.service.infrastructure.consul 8125'
            subprocess.call(bash, shell=True)
            time.sleep(5)

    def set_metric(self, dictrep):
        if 'host_name' in dictrep:
            self.host_name = dictrep['host_name']
        elif 'service_desc' in dictrep:
            self.service_desc = dictrep['service_desc']

if __name__ == '__main__':
    Incident.list_incidents(Incident)
