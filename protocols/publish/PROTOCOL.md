---
name: publish
description: >-
  Assembles the verified draft into the published newspaper issue, gating on
  grounding, and updates the chronicle's continuity ledger for the next issue.
---

# Publish

Publish closes the issue. runa activates it when a `grounding` exists. Publish
assembles the verified `draft` into the `issue` — the newspaper itself — and
produces the updated `ledger`, the continuity state the next issue inherits.

Publish exists to do two things at once: put the issue to bed honestly, and
hand the chronicle forward. It is where the grounding, coverage, and
continuity contracts are enforced — none of them by runa, all of them by this
protocol.

## Behavior Contract

**Given** a `draft`, a `grounding`, a `lineup`, and a `beat`,
**when** publish runs,
**then** it produces an `issue` containing only stories whose claims
`grounding` marked `supported`, with a `coverage_report` accounting
committed-versus-published, and a `ledger` whose `open_threads` carries every
still-open thread forward.

## Goal

The published `issue` — the newspaper, emitted to `brief.publication_target` —
and the updated `ledger`, the chronicle's running state for the next run.

## Discipline — three obligations, none enforced by runa

1. **Grounding gate.** A claim that `grounding` marked `unsupported` must not
   appear in any published story. The story is corrected to drop that claim,
   or the story is pulled. Publish does not print ungrounded claims.
2. **Coverage honesty.** `coverage_report` records `committed` (the lineup's
   selected candidate_ids), `published` (what actually ran), and `omitted`
   (carried from the lineup). `unresolved` lists anything committed but not
   published; it should be empty, and a non-empty list carries an honest
   reason.
3. **Continuity.** `ledger.open_threads` is the beat's inherited threads still
   open, plus this issue's `deferred` omissions — no thread dropped by
   silence. `ledger.covered` and `issues_published` are extended; `last_issue`
   is this issue.

## The ledger is a singleton

Deliver the `ledger` under the constant `instance_id` `ledger`, overwriting
the prior one. The ledger carries no `issue_id`: it is the chronicle's
periodical state, not one issue's. The orchestrator carries it into the next
issue's workspace as `survey`'s continuity input.

## Red and Green Signals

- **Green (mechanical):** the `issue` and the `ledger` both validate.
- **Red (mechanical):** a missing or invalid `issue` or `ledger` — runa fails
  the protocol.
- **Red (methodological):** an unsupported claim published; a committed story
  missing without an honest `unresolved` entry; an open thread absent from the
  new ledger. None is caught by schema validation; all three are contract
  obligations of this protocol.

## Delivering the issue and the ledger

```
issue({
  instance_id: "<beat.issue_id>",
  issue_id: "<beat.issue_id>",
  title: "...",
  published_stories: [ { candidate_id: "...", headline: "...", body: "..." } ],
  coverage_report: { committed: ["..."], published: ["..."],
                     omitted: [ { candidate_id: "...", reason: "...",
                                  disposition: "dropped" } ],
                     unresolved: [] },
  publication_target: "<brief.publication_target>"
})

ledger({
  instance_id: "ledger",
  chronicle: "...",
  last_issue: "<beat.issue_id>",
  issues_published: [ "..." ],
  open_threads: [ { thread_id: "...", summary: "...", origin_issue: "..." } ],
  covered: [ { candidate_id: "...", issue_id: "...", headline: "..." } ]
})
```
