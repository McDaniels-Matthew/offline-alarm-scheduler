"""Additional deterministic scheduler boundary tests, independent of device firmware."""
from datetime import datetime, timezone
import unittest
from zoneinfo import ZoneInfo

from offline_alarm import AlarmProfile, EVERY_DAY, next_occurrences

EASTERN = ZoneInfo('America/New_York')


class SchedulerEdgeCaseTests(unittest.TestCase):
    def test_spring_forward_valid_time_remains_on_transition_day(self):
        after = datetime(2027, 3, 14, 1, 59, tzinfo=EASTERN)
        profile = AlarmProfile('post-gap', 3, 0, EVERY_DAY)
        occurrence = next_occurrences([profile], after, EASTERN, count=1)[0]
        self.assertEqual((2027, 3, 14, 3, 0), (
            occurrence.local.year, occurrence.local.month, occurrence.local.day,
            occurrence.local.hour, occurrence.local.minute))
        self.assertEqual('2027-03-14T07:00:00+00:00', occurrence.utc.isoformat())

    def test_equal_instant_sorted_by_profile_identity(self):
        profiles = [AlarmProfile('z', 7, 0), AlarmProfile('a', 7, 0)]
        after = datetime(2026, 11, 18, 0, 0, tzinfo=timezone.utc)
        occurrences = next_occurrences(profiles, after, EASTERN, count=2)
        self.assertEqual(['a', 'z'], [o.identity for o in occurrences])
        self.assertEqual(occurrences[0].utc, occurrences[1].utc)

    def test_day_mask_uses_local_date_not_utc_date(self):
        # 04:00 UTC Monday is 23:00 Sunday in New York in November.
        only_sunday = AlarmProfile('sun', 23, 30, days=1 << 6)
        after = datetime(2026, 11, 23, 4, 0, tzinfo=timezone.utc)
        occurrence = next_occurrences([only_sunday], after, EASTERN, count=1)[0]
        self.assertEqual((2026, 11, 22, 23, 30), (
            occurrence.local.year, occurrence.local.month, occurrence.local.day,
            occurrence.local.hour, occurrence.local.minute))
        self.assertEqual('2026-11-23T04:30:00+00:00', occurrence.utc.isoformat())

    def test_empty_day_mask_has_no_occurrences(self):
        after = datetime(2026, 11, 18, tzinfo=timezone.utc)
        self.assertEqual([], next_occurrences(
            [AlarmProfile('never', 7, 0, days=0)], after, EASTERN))

    def test_query_parameter_bounds(self):
        after = datetime(2026, 11, 18, tzinfo=timezone.utc)
        profiles = [AlarmProfile('daily', 7, 0)]
        for options in ({'count': 0}, {'lookahead_days': 0},
                        {'lookahead_days': 36601}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                next_occurrences(profiles, after, EASTERN, **options)


if __name__ == '__main__':
    unittest.main()
