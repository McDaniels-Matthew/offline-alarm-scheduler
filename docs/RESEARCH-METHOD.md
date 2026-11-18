# Embedded research method (sanitized)

This project emphasizes disciplined, lawful experimentation rather than publishing third-party code. For user-owned devices, a reproducible workflow can include: firmware provenance and hashes; identifying CPU and on-device update packaging; distinguishing vendor app code from standard SDK/runtime dependencies; recording disassembler assumptions; tracing event-driven behavior; and validating each inference with isolated tests.

Working rules:

- Separate **observed fact**, **static-analysis interpretation**, and **untested hypothesis**.
- A decompiler's inferred type or function boundary is not source-level truth.
- String references frequently lead to diagnostics rather than the named handler.
- Any apparent date/time support must be tested across startup, calendar rollover and loss of power before proposing weekday-based logic.
- Plan rollback and recovery before attempting a writable experiment.
- Independently authored functional models belong in the public repository; vendor-derived dumps remain offline.

The companion hardware investigation is not included in this public repository. No proprietary offsets, source excerpts, captured binaries, or exploit payloads are necessary to understand the reference scheduler.
