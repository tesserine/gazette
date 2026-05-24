---
name: factcheck
description: >-
  Verifies a draft against its source trails, issuing one grounding verdict
  per claim and flagging every unsupported claim before publication.
---

# Factcheck

Factcheck is the chronicle's credibility gate. runa activates it when a
`draft` exists. Factcheck examines every claim the draft asserts, checks it
against the source it cites, and produces `grounding` — the per-claim verdict
that `publish` uses to decide what may go to print.

Factcheck exists because a chronicle's worth is its grounding. It does not
write and it does not fix; it reports the truth about whether each claim is
actually supported.

## Behavior Contract

**Given** a `draft` and a `dispatch`,
**when** factcheck runs,
**then** it produces a `grounding` carrying one verdict for every claim in the
draft, with `unsupported_count` equal to the number of unsupported verdicts.

## Goal

A `grounding` record that lets `publish` gate the issue on credibility: every
draft claim judged, the verdict honest, the unsupported ones counted.

## Discipline

For each `claim` in the draft, examine the source it cites — `source_locator`,
traceable to the dispatch's `source_trail` — and judge whether that source
actually supports the claim's `statement`. Record the verdict honestly:
`supported` or `unsupported`, with what was `checked_against`. Factcheck does
not repair the draft; reporting an `unsupported` verdict is factcheck working
correctly, not failing. `unsupported_count` must equal the count of
`unsupported` verdicts.

## Red and Green Signals

- **Green (mechanical):** the `grounding` validates — one verdict per claim is
  the methodological obligation; schema enforces verdict structure.
- **Red (mechanical):** a malformed `grounding`.
- **The grounding signal:** `unsupported_count > 0` is a value inside a
  *valid* artifact. runa cannot reject it — a correct factcheck of a flawed
  draft legitimately reports unsupported claims. The *gate* on that signal
  lives in `publish`'s contract, not in schema validation. This is
  methodological by design.
- **Red (methodological):** a verdict missing for a draft claim; a dishonest
  `supported` verdict.

## Delivering the grounding

```
grounding({
  instance_id: "<draft.issue_id>",
  issue_id: "<draft.issue_id>",
  claim_verdicts: [
    { claim_id: "...", status: "supported",
      checked_against: "...", note: "..." }
  ],
  unsupported_count: 0
})
```
