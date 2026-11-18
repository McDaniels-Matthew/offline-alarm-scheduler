"""Small offline CLI demonstration of upcoming recurring alarms."""
from datetime import datetime
from zoneinfo import ZoneInfo
from .scheduler import AlarmProfile, WEEKDAYS, WEEKENDS, next_occurrences

def main()->None:
    tz=ZoneInfo('America/New_York')
    profiles=[AlarmProfile('weekdays',7,0,WEEKDAYS),AlarmProfile('weekends',9,0,WEEKENDS)]
    after=datetime(2026,11,18,6,0,tzinfo=tz)
    for occurrence in next_occurrences(profiles,after,tz,count=5):
        print(f'{occurrence.identity:10s} {occurrence.local.isoformat()} [UTC {occurrence.utc.isoformat()}]')

if __name__=='__main__':main()
