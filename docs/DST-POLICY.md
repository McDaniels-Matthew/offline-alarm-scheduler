# Daylight saving time policy

All alarm profiles express **local wall time** in a specified IANA timezone. The reference implementation resolves that wall time to a UTC instant using `zoneinfo` and a UTC round trip.

1. **Spring forward (nonexistent local time):** skip that date's occurrence. Example: an alarm for 02:30 in `America/New_York` on the spring transition Sunday is not shifted to 03:30.
2. **Fall back (ambiguous local time):** choose the **first** physical occurrence only (`fold=0` in the reference timezone). Do not trigger again in the repeated hour.
3. **Calendar change:** the day-mask is computed using the local calendar date; it is not derived from UTC day numbers.
4. **Manual clock edits and power loss:** must not silently generate retroactive alarms. Future embedded delivery needs a persistent ledger keyed by alarm identity and scheduled UTC instant or an equivalent monotonic occurrence identifier.
5. **Timezone rule updates:** firmware without network access should carry a documented timezone rule set and update mechanism. Rules can change by legislation; never claim perpetual accuracy without a maintenance strategy.

The chosen policy is a user-experience design decision, not necessarily the behavior of any existing manufactured clock.
