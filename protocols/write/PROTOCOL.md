---
name: write
description: >-
  Writes the selected story candidates into reported stories, registering
  every factual claim against the source it rests on and declaring the
  confidence of each claim.
---

# Write

Write is where the issue is actually written. runa activates it when a
`lineup` exists. Write takes the lineup's selections and the candidate detail
in the `dispatch` and produces the `draft` — the reported stories themselves.

Write exists to turn editorial decisions into prose without losing the
grounding. Every factual assertion a story makes is registered as a claim with
the source behind it and the strength of that grounding declared, so the chain
from corpus to printed sentence stays traceable into `factcheck`.

## Behavior Contract

**Given** a `lineup` and a `dispatch`,
**when** write runs,
**then** it produces a `draft` with exactly one story per selected candidate,
each story's factual claims registered against the source each one rests on,
and each claim's `confidence` declared `firm` or `qualified` — a qualified
claim stating its `limits`.

## Goal

A `draft` of reported stories — one per `lineup.selected` entry, written in
the assigned angle, every claim attributed and its confidence honest — ready
for `factcheck` to verify and `publish` to assemble.

## Discipline

**One story per selection, in the assigned angle.** Write one story for each
entry in `lineup.selected`, in the `angle` the lineup assigns, drawing detail
from that candidate's `summary` and `source_trail` in the dispatch. The
story's `kind` echoes the candidate's. Do not write a story for a candidate
the lineup did not select.

**Every claim carries a source — without exception.** Every factual assertion
in a story `body` is registered as a `claim` carrying the `source_locator` it
rests on. A sentence of fact with no source behind it does not belong in the
draft. This is the grounding floor and v0.2 does not move it.

**Declare confidence honestly.** Each claim declares `confidence`. A `firm`
claim is one its source fully supports as asserted. A `qualified` claim is one
the source supports only partially or indirectly — and a qualified claim
states its `limits`: what the source does not establish. Qualified is not a
license for weak sourcing. A claim whose source does not support it at all is
not a qualified claim — it is an unsupported claim, and it does not belong in
the draft. The honest path for an under-supported assertion is to narrow the
statement until the source does support it, mark it qualified with its limits,
or drop it. Writing a confident sentence and labelling it `qualified` to slip
past grounding is the failure this contract exists to forbid.

**Archive-gap stories.** A story whose `kind` is `archive_gap` reports a
material silence. Its claims assert the existence and extent of the gap, each
grounded in the evidence of absence carried in the candidate's trail. An
archive-gap story does not assert the missing facts themselves — it reports,
with grounding, that they are missing.

## Red and Green Signals

- **Green (mechanical):** the `draft` validates — at least one story, each
  story carrying at least one claim, each claim carrying a `source_locator`
  and a `confidence`.
- **Red (mechanical):** a story with no claims; a claim with no source; a
  claim with no declared confidence.
- **Red (methodological):** a story count that does not match the selection
  count; a story for an unselected candidate; a `qualified` claim with no
  stated `limits`; an under-supported claim dressed as `qualified` rather than
  narrowed or dropped; an archive-gap story that asserts the missing facts
  instead of reporting their absence. Schema validation cannot catch these;
  `factcheck` and `publish` catch them.

## Delivering the draft

```
draft({
  instance_id: "<lineup.issue_id>",
  issue_id: "<lineup.issue_id>",
  stories: [
    { candidate_id: "...", kind: "development", headline: "...", body: "...",
      claims: [
        { claim_id: "...", statement: "...", source_locator: "...",
          confidence: "firm" },
        { claim_id: "...", statement: "...", source_locator: "...",
          confidence: "qualified", limits: "what the source does not establish" }
      ] }
  ]
})
```
