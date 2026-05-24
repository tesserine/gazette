---
name: survey
description: >-
  Opens a Gazette issue. Establishes the issue's grounded scope and maps the
  reachable historical source corpus, inheriting open threads from the prior
  issue's ledger. Entry point of the Gazette lifecycle.
---

# Survey

Survey is the entry point of the Gazette methodology. runa activates it when a
`brief` artifact enters the workspace — the external editorial commission for
an issue. Survey turns that commission into a grounded `beat`: the scope this
issue can honestly cover, and a map of the sources available to cover it.

Survey exists because the most dangerous move in chronicling is to promise
coverage the record cannot support. The brief states an *intended* scope;
survey's job is to confront that intent with the *actual* corpus and produce a
scope bounded by what the sources hold.

## Behavior Contract

**Given** a `brief`, and the prior issue's `ledger` if one exists,
**when** survey runs,
**then** it produces a `beat` whose `scope` is grounded in what `corpus_map`
demonstrably supports, whose `inherited_threads` carry every open thread from
the prior ledger, and whose `corpus_gaps` name every part of the brief's
intended scope the corpus cannot reach.

## Goal

A `beat` artifact that gives `report` an honest territory to mine: a bounded
scope, an assessed map of reachable sources, the threads inherited from the
chronicle so far, and an explicit statement of what the corpus cannot reach.

## Discipline

Map the corpus before fixing the scope. Visit each pointer in
`brief.corpus_pointers`; record what is actually there, not what the brief
hoped would be there. Where the intended scope outruns the corpus, the honest
output is a narrowed `scope` plus a named entry in `corpus_gaps` — never a
scope that asserts coverage the sources cannot support.

If a prior `ledger` is present, every thread in its `open_threads` must appear
in the beat's `inherited_threads`. A thread is not closed by being ignored.

## Red and Green Signals

- **Green (mechanical):** the `beat` validates against its schema.
- **Red (mechanical):** a missing or invalid `beat` — runa fails the protocol.
- **Red (methodological):** a `scope` claiming coverage `corpus_map` does not
  support; an inherited thread silently dropped. Neither is caught by schema
  validation; both are contract obligations of this protocol.

## Delivering the beat

Deliver the `beat` by invoking the `beat` artifact tool. `instance_id` names
the artifact instance — use the issue identifier from `brief.issue_id`.

```
beat({
  instance_id: "<brief.issue_id>",
  issue_id: "<brief.issue_id>",
  scope: "<the grounded, bounded scope>",
  corpus_map: [ { locator: "...", description: "...", kind: "..." } ],
  inherited_threads: [ /* threads from the prior ledger, or [] for issue one */ ],
  corpus_gaps: [ "..." ]
})
```

Delivery succeeds when the tool returns without error. Schema validity is not
honesty: a `beat` whose scope outruns its `corpus_map` is structurally valid
and contractually wrong.
