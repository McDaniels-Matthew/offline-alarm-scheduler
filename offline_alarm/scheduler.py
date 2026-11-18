"""Pure recurring local-time scheduler with deterministic DST gap/fold policy.

Independent educational reference code; not embedded firmware or a device driver.
Monday = bit 0, Sunday = bit 6. UTC is used for occurrence ordering.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

WEEKDAYS = 0b0011111        # Mon..Fri
WEEKENDS = 0b1100000        # Sat..Sun
EVERY_DAY = WEEKDAYS | WEEKENDS
UTC = timezone.utc

@dataclass(frozen=True, slots=True)
class AlarmProfile:
    identity: str
    hour: int
    minute: int
    days: int = EVERY_DAY
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.identity or not self.identity.strip():
            raise ValueError('profile identity must be nonempty')
        if not 0 <= self.hour <= 23: raise ValueError('hour must be in [0, 23]')
        if not 0 <= self.minute <= 59: raise ValueError('minute must be in [0, 59]')
        if not 0 <= self.days <= EVERY_DAY: raise ValueError('days must be a 7-bit mask')

    def active_on(self, calendar_date: date) -> bool:
        return self.enabled and bool(self.days & (1 << calendar_date.weekday()))

@dataclass(frozen=True, slots=True)
class Occurrence:
    identity: str
    local: datetime
    utc: datetime


def _resolve_first_real_occurrence(day:date,hour:int,minute:int,tz:ZoneInfo) -> datetime | None:
    """Resolve a local wall time to earliest UTC instant; nonexistent wall time -> None.

    Both PEP 495 folds are tested by UTC roundtrip, distinguishing ambiguous
    repeated times from nonexistent times. The earliest valid UTC instant wins.
    """
    wall=datetime.combine(day,time(hour,minute))
    real=[]
    for fold in (0,1):
        candidate=wall.replace(tzinfo=tz,fold=fold)
        instant=candidate.astimezone(UTC)
        roundtrip=instant.astimezone(tz).replace(tzinfo=None)
        if roundtrip==wall and instant not in real:
            real.append(instant)
    return min(real) if real else None


def next_occurrences(
    profiles: list[AlarmProfile] | tuple[AlarmProfile,...],
    after:datetime,
    tz:ZoneInfo,
    count:int=5,
    lookahead_days:int=370,
) -> list[Occurrence]:
    """Return at most `count` upcoming alarm instants strictly AFTER `after`.

    `after` must be timezone-aware; profile times are local to `tz`.
    The function does NOT deliver alarms or enforce exactly-once after reboot.
    """
    if after.tzinfo is None or after.utcoffset() is None:
        raise ValueError('after must be timezone-aware')
    if not isinstance(tz,ZoneInfo): raise TypeError('tz must be an IANA ZoneInfo object')
    if count<1: raise ValueError('count must be positive')
    if not 1<=lookahead_days<=36600: raise ValueError('lookahead_days outside permitted range')
    ids=[p.identity for p in profiles]
    if len(set(ids))!=len(ids): raise ValueError('profile identities must be unique')

    after_utc=after.astimezone(UTC)
    first_day=after_utc.astimezone(tz).date()
    events=[]
    for d in range(lookahead_days):
        day=first_day + timedelta(days=d)
        for p in profiles:
            if not p.active_on(day):continue
            utc=_resolve_first_real_occurrence(day,p.hour,p.minute,tz)
            if utc is None or utc<=after_utc:continue
            events.append(Occurrence(p.identity,utc.astimezone(tz),utc))
        if len(events)>=count and d>=1:
            # Future dates cannot precede an event from a prior local day.
            break
    events.sort(key=lambda x:(x.utc,x.identity))
    return events[:count]
