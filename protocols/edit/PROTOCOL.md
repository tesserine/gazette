---
name: edit
description: >-
  Exercises editorial judgment over an issue: selects which story candidates
  run — developments and archive gaps alike — names which are omitted and why,
  and records the coverage rationale.
---

# Edit

Edit is the chronicle's editorial desk. runa activates it when a `dispatch`
exists. Edit takes the grounded candidates and the issue's `beat` and decides
the issue: which candidates run as stories, which are held back, and why.

Edit exists because a chronicle is judgment, not a dump. Not every candidate
the corpus supports belongs in this issue. Edit is where coverage balance and
continuity are decided — and where every omission is made explicit rather than
left silent.

## Behavior Contract

**Given** a `beat` and a `dispatch`,
**when** edit runs,
**then** it produces a `lineup` in which every dispatch candidate — every
`development` and every `archive_gap` — is accounted for as either `selected`
or `omitted`, the selection sits within the beat's `scope`, and each omission
carries an honest reason and disposition.

## Goal

A `lineup` — the issue's editorial plan — that tells `write` exactly which
stories to write and in what angle, and tells `publish` what was committed and
what was deliberately set aside.

## Discipline

Select the candidates that best serve the issue's `scope` and the chronicle's
continuity. An `archive_gap` candidate is weighed on the same editorial
footing as a `development`: a material gap can be the right thing to run, and a
gap candidate is judged by its relevance, not set aside merely for being a gap.
A run made thin by a sparse corpus is honestly reported as such — including,
where apt, by running the archive-gap stories that say so — rather than padded
with weak developments.

Every candidate in the dispatch that is not selected must appear in `omitted`
with a `reason` and a `disposition`: `deferred` — a live thread for a future
issue, tagged with a `thread_id` — or `dropped`. No candidate is left
unaccounted for. `coverage_rationale` states the judgment behind the selection
and its balance, including the balance between developments and archive gaps.

## Red and Green Signals

- **Green (mechanical):** the `lineup` validates — at least one selection, an
  `omitted` array present, a `coverage_rationale`.
- **Red (mechanical):** an empty `selected` array.
- **Red (methodological):** a dispatch candidate that appears in neither
  `selected` nor `omitted` — a silent drop; an archive-gap candidate dismissed
  without an honest reason. Schema validation cannot compare the lineup
  against the dispatch; `publish`'s coverage report and review catch it.

## Delivering the lineup

```
lineup({
  instance_id: "<beat.issue_id>",
  issue_id: "<beat.issue_id>",
  selected: [ { candidate_id: "...", angle: "...", prominence: "..." } ],
  omitted: [ { candidate_id: "...", reason: "...",
               disposition: "deferred", thread_id: "..." } ],
  coverage_rationale: "<the editorial judgment behind this selection>"
})
```
