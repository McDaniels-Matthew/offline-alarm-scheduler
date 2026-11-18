# Offline Alarm Scheduler

**Independent reference implementation** of a recurring alarm scheduler for embedded-style clocks. This is a learning and portfolio project emphasizing local-first behavior, deterministic testing, robust handling of daylight-saving transitions, and a clear separation between scheduling decisions and physical alarm hardware.

Inspired by the author's interest in improving a personally owned **Nanu Arc** alarm clock. **Not affiliated with, approved by, or supported by Nanu Electrics.** No manufacturer firmware, disassembly, decompiler output, proprietary assets, patched images, private captures or copied vendor code are included. **This project is not an installable firmware update.**

## Current features

- Independent weekday/weekend or arbitrary per-day recurring profiles using Monday-first 7-bit masks
- Timezone-aware next-occurrence calculation with a deterministic UTC output
- Explicit policy: nonexistent local alarm times are skipped on spring-forward days; repeated fall-back times fire only at the first occurrence
- Disabled alarms, overlapping schedules, wall-clock time comparisons, next-occurrence preview
- Offline standard-library Python reference code; no telemetry, network calls, accounts or cloud services
- Unit tests covering normal days and U.S. DST boundaries

> **Important:** These are reference-model behaviors, not verified or integrated Nanu firmware features. A trustworthy clock calendar, storage, delivery, battery behavior and physical recovery must all be validated before an embedded deployment.

## Run locally

Python 3.11+:

```bash
python -m unittest discover -s tests -v
python -m offline_alarm.demo
python tools/audit_repo.py --root .
```

For Windows systems without IANA timezone data, install the open-source `tzdata` package using `python -m pip install tzdata`. The Python reference model does not require Nanu hardware.

The package layout makes `offline_alarm` importable directly from the repository root. The production scheduler is intentionally not coupled to Ghidra or ESP-IDF.

## Development boundaries

- Never introduce manufacturer's firmware, decompiled C, ROM contents, image resources or cryptographic material.
- Do not publish device-specific bypass instructions or patched images.
- Keep test data synthetic and review all commits before publishing.
- Avoid claims of demonstrated device compatibility until independently validated.

See `docs/ARCHITECTURE.md`, `docs/DST-POLICY.md`, `docs/TEST-PLAN.md`, `docs/PROVENANCE.md`, `SECURITY.md`.

## Project goals

Research and independently prototype alarm scheduling for user-owned offline devices; practice embedded architecture, firmware analysis methodology, C/C++ design translation, test engineering and reliability. Collaboration or commercial use is not required for the project's success.

## License

The original code and original documentation in this repository are published under the MIT license. This license does **not** cover any manufacturer's firmware or third-party intellectual property, none of which is provided here.
