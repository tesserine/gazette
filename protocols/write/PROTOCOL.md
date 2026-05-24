---
name: write
description: >-
  Writes the selected story candidates into reported stories, registering
  every factual claim against the source it rests on.
---

# Write

Write is where the issue is actually written. runa activates it when a
`lineup` exists. Write takes the lineup's selections and the candidate detail
in the `dispatch` and produces the `draft` — the reported stories themselves.

Write exists to turn editorial decisions into prose without losing the
grounding. Every factual assertion a story makes is registered as a claim with
the source behind it, so the chain from corpus to printed sentence stays
traceable into `factcheck`.

## Behavior Contract

**Given** a `lineup` and a `dispatch`,
**when** write runs,
**then** it produces a `draft` with exactly one story per selected candidate,
each story's factual claims registered against the source each one rests on.

## Goal

A `draft` of reported stories — one per `lineup.selected` entry, written in
the assigned angle, every claim attributed — ready for `factcheck` to verify
and `publish` to assemble.

## Discipline

Write one story for each entry in `lineup.selected`, in the `angle` the lineup
assigns, drawing detail from that candidate's `summary` and `source_trail` in
the dispatch. Every factual assertion in a story `body` is registered as a
`claim` carrying the `source_locator` it rests on. A sentence of fact with no
source behind it does not belong in the draft. Do not write a story for a
candidate the lineup did not select.

## Red and Green Signals

- **Green (mechanical):** the `draft` validates — at least one story, each
  story carrying at least one claim, each claim carrying a `source_locator`.
- **Red (mechanical):** a story with no claims, or a claim with no source.
- **Red (methodological):** a story count that does not match the selection
  count; a story written for an unselected candidate. Schema validation cannot
  compare the draft against the lineup; review and `publish` catch it.

## Delivering the draft

```
draft({
  instance_id: "<lineup.issue_id>",
  issue_id: "<lineup.issue_id>",
  stories: [
    { candidate_id: "...", headline: "...", body: "...",
      claims: [ { claim_id: "...", statement: "...", source_locator: "..." } ] }
  ]
})
```
