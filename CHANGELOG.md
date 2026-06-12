# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- README hero rewritten for the ecosystem README pass: gazette positioned as
  the existence proof that methodologies generalize beyond code, with the
  grounding floor, qualified claims, and archive-gaps-as-news discipline
  surfaced up front; the source-of-truth map linked directly.

### Added

- `examples/weforge-001/` — a complete worked issue: input brief and every
  protocol's output artifact through the published issue and continuity
  ledger, demonstrating the grounding floor, a qualified claim with visible
  limits, an archive-gap story, no-silent-drop omission accounting, and
  thread carry-forward.
- `tests/test_schemas.py` + CI (`.github/workflows/validate.yml`) — schema
  validity against the declared draft, example conformance against every
  schema, and coherence checks for the worked example's load-bearing
  properties.
- README "Running an issue" quickstart and an artifact-graph table
  (protocol × requires/accepts/produces/trigger).
- `LICENSE` (MIT) and this changelog.
- README pointer to the canonical principles corpus
  (`pentaxis93/principles`) and to commons (#5).

## [0.2.0] — 2026-05-24

### Added

- v0.2 methodology: six protocols (survey, report, edit, write, factcheck,
  publish), eight artifact schemas, and the imperfect-archive reporting
  model (assessed sources, declared uncertainty, archive gaps as news).
