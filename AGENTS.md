# Codex project instructions — independent, public scheduler

This repository must contain **original software and original documentation only**. Do not copy, derive code from, or export portions of the vendor's firmware, disassembly, resource files, memory dumps, keys, or Ghidra pseudocode. Firmware research exists in a separate offline lab. Do not introduce unverified claims of hardware compatibility or instructions for circumventing device protections.

## Implementation

- Python 3.11+ standard-library reference model; no network calls, telemetry or remote services.
- Keep scheduling pure: input immutable profiles + time/timezone; output scheduled occurrences. Physical triggering, persistent storage and display are separate adapters to be designed later.
- Monday-first bitmask (bit 0 = Monday, bit 6 = Sunday).
- Explicit DST behavior: skip nonexistent wall times; choose first occurrence on repeated fall-back times.
- Build tests covering weekdays, DST, midnight, repeated hour, disabled profiles, boundary comparisons, and next-occurrence ordering.
- Treat device power loss / actual RTC trust as an open engineering issue, not as solved by Python's calendar support.
- Run tests and publication audit before every push; inspect diff for newly introduced copied text or non-original resources.
