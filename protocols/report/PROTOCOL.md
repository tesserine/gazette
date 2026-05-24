---
name: report
description: >-
  Mines the surveyed corpus for developments worth reporting and for
  materially relevant archive gaps, producing grounded story candidates — each
  carrying the source trail that supports it.
---

# Report

Report is the chronicle's field work. runa activates it when a `beat` exists.
Report mines the sources mapped in the beat and turns what it finds into
`dispatch` — a set of grounded story candidates for the editor to choose from.

Report exists to separate *finding* from *deciding*. It does not decide what
runs; it surfaces every development the corpus genuinely supports, and every
archive gap material enough to matter, with the evidence attached, so the
editorial judgment downstream has honest material.

## Behavior Contract

**Given** a `beat`,
**when** report runs,
**then** it produces a `dispatch` of story candidates — `development`
candidates for things that happened, and `archive_gap` candidates for
materially relevant silences in the record — each candidate carrying a
non-empty `source_trail`.

## Goal

A `dispatch` of grounded candidates: real developments found within the
issue's scope, and material archive gaps worth reporting, each with the
specific records that support it, ready for `edit` to select among.

## Discipline

**Two kinds of candidate, one grounding floor.** A `development` candidate is
a development actually found in the corpus — never invented to fill the issue.
An `archive_gap` candidate is a silence the beat marked `material: true` —
where the record fails to show something a reader would expect. Both kinds
carry a non-empty `source_trail`; the grounding floor is absolute. For a
development, the trail cites the records of what happened. For an archive gap,
the trail cites the *evidence of absence*: the record present in one place
with no corresponding record where one was expected, naming what was looked
for and not found. A gap with no such evidence is not a candidate — an
ungrounded absence is speculation, not reporting.

**Material gaps only.** An `archive_gap` candidate is raised only for a gap
the beat marked material. The natural edges of scope are not news; a silence
becomes a candidate only when it is materially relevant to the chronicle.
Archive-gap candidates are not filler for a thin issue.

**Weigh sources by their assessment.** The beat's `corpus_map` assessed each
source. Report uses that: a candidate resting on `unverified` or `fragmentary`
sources is still a candidate, but report carries that weakness forward
honestly in the `summary` and the trail rather than presenting a shaky finding
as a solid one.

**Mine within scope, and tag threads.** A development outside the beat's
`scope` is not reported here. When a candidate continues an inherited thread,
tag it with that `thread_id` so the continuity stays traceable.

## Red and Green Signals

- **Green (mechanical):** the `dispatch` validates. Because the schema
  requires `source_trail` to hold at least one citation, *every candidate —
  development and archive_gap alike — being grounded* is mechanically enforced
  here.
- **Red (mechanical):** a candidate with an empty source trail; a candidate
  with no `kind` — schema invalid, runa fails the protocol.
- **Red (methodological):** a development invented rather than found; an
  archive-gap candidate raised for a non-material gap, or with a trail that
  does not actually evidence the absence; a shaky source presented as solid.
  Schema validation cannot catch these; `factcheck` verifies grounding
  downstream.

## Delivering the dispatch

```
dispatch({
  instance_id: "<beat.issue_id>",
  issue_id: "<beat.issue_id>",
  candidates: [
    { candidate_id: "...", kind: "development", headline: "...", summary: "...",
      source_trail: [ { locator: "...", excerpt_or_detail: "..." } ],
      thread_id: "<if it continues an inherited thread>" },
    { candidate_id: "...", kind: "archive_gap", headline: "...",
      summary: "what the record does not show and why it matters",
      source_trail: [ { locator: "...", excerpt_or_detail: "what was looked for and not found" } ] }
  ]
})
```
