---
name: report
description: >-
  Mines the surveyed source corpus for developments worth reporting, producing
  grounded story candidates — each one carrying the source trail that supports
  it.
---

# Report

Report is the chronicle's field work. runa activates it when a `beat` exists.
Report mines the sources mapped in the beat and turns the developments it
finds into `dispatch` — a set of grounded story candidates for the editor to
choose from.

Report exists to separate *finding* from *deciding*. It does not decide what
runs; it surfaces every development the corpus genuinely supports, with the
evidence attached, so the editorial judgment downstream has honest material.

## Behavior Contract

**Given** a `beat`,
**when** report runs,
**then** it produces a `dispatch` of story candidates, each carrying a
non-empty `source_trail` of citations drawn from the beat's `corpus_map`.

## Goal

A `dispatch` of grounded candidates: real developments found within the
issue's scope, each with the specific records that support it, ready for
`edit` to select among.

## Discipline

Every candidate is a development actually found in the corpus — never invented
to fill the issue. Every candidate carries the specific sources that support
it; a candidate with no `source_trail` is not a candidate. Mine within the
beat's `scope`; a development outside scope is not reported here. When a
candidate continues an inherited thread, tag it with that `thread_id` so the
continuity stays traceable.

## Red and Green Signals

- **Green (mechanical):** the `dispatch` validates. Because the schema
  requires `source_trail` to hold at least one citation, *every candidate
  being grounded* is mechanically enforced at this stage.
- **Red (mechanical):** a candidate with an empty source trail — schema
  invalid, runa fails the protocol.
- **Red (methodological):** a source trail citing records that do not in fact
  support the candidate; a development invented rather than found. Schema
  validation cannot catch either; `factcheck` verifies the first downstream.

## Delivering the dispatch

```
dispatch({
  instance_id: "<beat.issue_id>",
  issue_id: "<beat.issue_id>",
  candidates: [
    { candidate_id: "...", headline: "...", summary: "...",
      source_trail: [ { locator: "...", excerpt_or_detail: "..." } ],
      thread_id: "<if it continues an inherited thread>" }
  ]
})
```
