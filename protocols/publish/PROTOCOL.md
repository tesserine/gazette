---
name: publish
description: >-
  Assembles the verified draft into the published newspaper issue — gating on
  grounding, confirming qualified claims, surfacing archive gaps — and updates
  the chronicle's continuity ledger for the next issue.
---

# Publish

Publish closes the issue. runa activates it when a `grounding` exists. Publish
assembles the verified `draft` into the `issue` — the newspaper itself — and
produces the updated `ledger`, the continuity state the next issue inherits.

Publish exists to do two things at once: put the issue to bed honestly, and
hand the chronicle forward. It is where the grounding, coverage, uncertainty,
and continuity contracts are enforced — none of them by runa, all of them by
this protocol.

## Behavior Contract

**Given** a `draft`, a `grounding`, a `lineup`, and a `beat`,
**when** publish runs,
**then** it produces an `issue` in which no claim `grounding` marked
`unsupported` appears; every published claim `grounding` marked
`partially_supported` is carried as a declared `qualified` claim with stated
`limits`; archive-gap stories are published as such; the `coverage_report`
accounts committed-versus-published and lists the archive gaps reported; and a
`ledger` whose `open_threads` carries every still-open thread forward.

## Goal

The published `issue` — the newspaper, emitted to `brief.publication_target` —
in which a reader can tell grounded facts, declared uncertainties, omissions,
and archive gaps apart; and the updated `ledger`, the chronicle's running
state for the next run.

## Discipline — four obligations, none enforced by runa

1. **Grounding gate.** A claim that `grounding` marked `unsupported` must not
   appear in any published story. The story is corrected to drop that claim,
   or the story is pulled. Publish does not print ungrounded claims. This gate
   is absolute and unchanged from v0.1.

2. **Uncertainty is declared, never hidden and never fabricated.** A claim
   that `grounding` marked `partially_supported` may be published *only* as a
   `qualified` claim — the draft must have declared `confidence: qualified`
   with stated `limits`, and the published story carries that claim in its
   `qualified_claims` with the limit visible to the reader. A
   partially-supported claim the draft declared `firm` is not publishable as
   written: it is corrected — narrowed until firm, re-declared qualified, or
   dropped. Uncertainty travels into print as *stated* uncertainty or not at
   all.

3. **Coverage honesty.** `coverage_report` records `committed` (the lineup's
   selected candidate_ids), `published` (what actually ran), and `omitted`
   (carried from the lineup). `unresolved` lists anything committed but not
   published; it should be empty, and a non-empty list carries an honest
   reason. `archive_gaps_reported` lists the candidate_ids of published
   stories whose `kind` is `archive_gap` — the issue's explicit account of
   where the record was found wanting.

4. **Continuity.** `ledger.open_threads` is the beat's inherited threads still
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
- **Red (methodological):** an unsupported claim published; a
  partially-supported claim published without being declared `qualified` and
  carried in `qualified_claims` with its limits; a committed story missing
  without an honest `unresolved` entry; an archive-gap story published with
  its `kind` lost so a reader cannot tell it from a development; an open
  thread absent from the new ledger. None is caught by schema validation; all
  are contract obligations of this protocol.

## Delivering the issue and the ledger

```
issue({
  instance_id: "<beat.issue_id>",
  issue_id: "<beat.issue_id>",
  title: "...",
  published_stories: [
    { candidate_id: "...", kind: "development", headline: "...", body: "...",
      qualified_claims: [
        { claim_id: "...", statement: "...", limits: "..." }
      ] },
    { candidate_id: "...", kind: "archive_gap", headline: "...", body: "..." }
  ],
  coverage_report: { committed: ["..."], published: ["..."],
                     omitted: [ { candidate_id: "...", reason: "...",
                                  disposition: "dropped" } ],
                     unresolved: [],
                     archive_gaps_reported: ["..."] },
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
