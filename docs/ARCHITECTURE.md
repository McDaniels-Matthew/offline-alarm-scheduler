# Architecture — independent reference model

## Layers

1. **Calendar input** — trusted timezone-aware current time plus an IANA timezone identifier.
2. **Profile store (future adapter)** — independently enabled profiles with (hour, minute, weekday mask); persistence format intentionally unspecified.
3. **Pure scheduler** — computes next occurrences from profiles and calendar time, returning unambiguous UTC instants.
4. **Trigger delivery (future adapter)** — uses a persistent per-occurrence identifier and state-machine event queue; not implemented in the reference model.
5. **Physical actuator/display (outside scope)** — chime, stepper motor, snooze and user interface remain separate concerns.

```
Calendar + profiles
        |
        v
Pure next-occurrence scheduler ----> preview
        |
        v
[Future] exactly-once delivery ---> [Future] physical alarm state machine
```

## Invariants

- No schedule if wall clock is not trustworthy; no network or cloud requirement.
- Explicitly choose DST fold behavior, never rely on ambiguous local time comparisons.
- Active profiles must have unique IDs; days mask uses Monday bit 0 through Sunday bit 6.
- Scheduler never moves the clock's physical hands or changes actual wall time.
- Disabled profiles produce no occurrences.
- A duplicate occurrence cannot be triggered merely because the wall clock moves backward. True exactly-once activation requires *persistent* delivery state, not just the pure scheduler.

## Status

The scheduler exists as tested Python code. There is currently **no ESP-IDF integration**, no physical device update, and no proof that a target clock preserves a correct date across a power failure. An eventual embedded C/C++ implementation should be independently written and validated against the reference model.
