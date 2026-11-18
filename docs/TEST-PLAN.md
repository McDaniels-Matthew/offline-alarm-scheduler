# Test plan and deployment gates

## Automated reference tests

- Weekday vs weekend selection and independent profile enable flags
- Correct next occurrence ordering in UTC from any aware starting time
- Strict comparison with the search boundary (no occurrence at or before the instant)
- Nonexistent spring-forward local time is skipped, later dates remain schedulable
- Fall-back local time resolves to the first instance only
- Midnight/date rollover and timezone conversion behavior
- Invalid hours, minutes, masks, naive datetimes, and duplicated profile IDs are rejected

## Not yet demonstrated

- RTC calendar initialization and retention under power interruptions
- NVS schema compatibility, endurance and recovery of partially written settings
- Exactly-once event delivery across resets or manual time corrections
- Battery, power failure, motor and chime behavior
- DFU protocol and recovery guarantees; manufacturer hardware integration

## Future test gates

1. Add property-based tests and clock-simulation runs spanning multiple years.
2. Specify occurrence-ledger transactional semantics in a design review.
3. Prototype the scheduling core in original C/C++ against a desktop harness.
4. Validate target-specific calendar, flash endurance, actual USB protocol and full hardware recovery **in a separate authorized offline environment**.
