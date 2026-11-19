from datetime import datetime, timezone
import unittest
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from offline_alarm import AlarmProfile, next_occurrences, WEEKDAYS, WEEKENDS, EVERY_DAY

try:
    EASTERN=ZoneInfo('America/New_York')
except ZoneInfoNotFoundError as exc:
    raise RuntimeError('IANA timezone data is required; run python -m pip install -r requirements.txt') from exc

class SchedulerTests(unittest.TestCase):
    def next(self,profiles,after,count=5):
        return next_occurrences(profiles,after,EASTERN,count=count)
    def test_weekday_and_weekend_profiles(self):
        profiles=[AlarmProfile('work',7,0,WEEKDAYS),AlarmProfile('off',9,15,WEEKENDS)]
        after=datetime(2026,11,20,8,0,tzinfo=EASTERN) # Friday
        got=self.next(profiles,after,3)
        self.assertEqual(['off','off','work'],[x.identity for x in got])
        self.assertEqual([(21,9,15),(22,9,15),(23,7,0)],[(x.local.day,x.local.hour,x.local.minute) for x in got])
    def test_disabled_profiles_are_silent(self):
        got=self.next([AlarmProfile('off',7,0,EVERY_DAY,False)],datetime(2026,11,18,1,tzinfo=EASTERN))
        self.assertEqual([],got)
    def test_skip_nonexistent_spring_time(self):
        profile=AlarmProfile('spring',2,30,EVERY_DAY)
        got=self.next([profile],datetime(2027,3,13,23,tzinfo=EASTERN),2)
        self.assertEqual([15,16],[x.local.day for x in got]) # 2027-03-14 02:30 absent
        self.assertTrue(all(x.local.hour==2 and x.local.minute==30 for x in got))
    def test_fall_repeated_hour_first_only(self):
        p=AlarmProfile('fold',1,30,EVERY_DAY)
        before=datetime(2027,11,7,0,0,tzinfo=EASTERN)
        first=self.next([p],before,1)[0]
        self.assertEqual(0,first.local.fold)
        self.assertEqual('2027-11-07T05:30:00+00:00',first.utc.isoformat())
        after_first=datetime(2027,11,7,6,0,tzinfo=timezone.utc) # During repeat
        second=self.next([p],after_first,1)[0]
        self.assertEqual(8,second.local.day) # no duplicate 01:30 second fold
    def test_strictly_after_and_next_midnight(self):
        p=AlarmProfile('a',0,0)
        after=datetime(2026,11,18,0,0,tzinfo=EASTERN)
        got=self.next([p],after,1)
        self.assertEqual(19,got[0].local.day)
    def test_utc_chronological_order(self):
        after=datetime(2026,11,18,3,0,tzinfo=timezone.utc)
        got=self.next([AlarmProfile('later',18,0),AlarmProfile('early',7,0)],after,4)
        self.assertEqual(sorted(x.utc for x in got),[x.utc for x in got])
    def test_duplicate_profile_ids_rejected(self):
        profiles=[AlarmProfile('same',7,0),AlarmProfile('same',8,0)]
        with self.assertRaises(ValueError):self.next(profiles,datetime.now(timezone.utc))
    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):self.next([AlarmProfile('a',7,0)],datetime(2026,11,18))
    def test_validation(self):
        for args in [('',7,0),( 'a',24,0),('a',0,60),('a',6,0,128)]:
            with self.subTest(args=args),self.assertRaises(ValueError):AlarmProfile(*args)

if __name__=='__main__': unittest.main()
