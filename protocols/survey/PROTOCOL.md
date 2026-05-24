---
name: survey
description: >-
  Opens a Gazette issue. Establishes the issue's grounded scope, discovers and
  maps the reachable source corpus with a quality assessment of each source,
  inherits open threads, and names materially relevant archive gaps. Entry
  point of the Gazette lifecycle.
---

# Survey

Survey is the entry point of the Gazette methodology. runa activates it when a
`brief` artifact enters the workspace — the external editorial commission for
an issue. Survey turns that commission into a grounded `beat`: the scope this
issue can honestly cover, an assessed map of the sources available to cover
it, and an honest account of what the corpus cannot reach.

Survey exists because the most dangerous move in chronicling is to promise
coverage the record cannot support. The brief states an *intended* scope and
an *initial* set of corpus pointers; survey's job is to confront that intent
with the *actual* corpus — including sources the brief did not name — and
produce a scope bounded by what the sources hold.

## Behavior Contract

**Given** a `brief`, and the prior issue's `ledger` if one exists,
**when** survey runs,
**then** it produces a `beat` whose `corpus_map` records both the sources
named in the brief and the relevant sources discovered by following trails
outward, each with a quality `assessment`; whose `scope` is grounded in what
that corpus demonstrably supports; whose `inherited_threads` carry every open
thread from the prior ledger; and whose `corpus_gaps` name every part of the
intended scope the corpus cannot reach, marking which gaps are materially
relevant.

## Goal

A `beat` that gives `report` an honest territory to mine: a bounded scope, an
assessed map of reachable sources, the threads inherited from the chronicle so
far, and an explicit account of what the corpus cannot reach and which of
those gaps matter.

## Discipline

**Discover, do not just receive.** The brief's `corpus_pointers` are a
starting set, not the whole corpus. From each pointer, follow the relevant
trails: git history leads to commits and their messages; an issue tracker
leads to tickets and their resolutions; an orientation doc points to other
records; live substrate can be read where it is reachable. A source reached by
following a trail is recorded in `corpus_map` with `discovered_from` set to the
locator that led to it, so the trail is auditable. Discovery follows relevant
trails — it is not an open-ended crawl; a trail that does not bear on the
issue's scope is not pursued.

**Assess every source.** Each `corpus_map` entry carries an `assessment`:
`reliability` (primary / secondary / unverified), `freshness` (current / aging
/ stale / unknown), `completeness` (full / partial / fragmentary), and
`ownership` where known. The assessment is practical — enough for `report`,
`edit`, and `factcheck` to judge how much weight a source can bear. It is not
a research grade; it is a working note.

**Bound the scope to the corpus.** Where the intended scope outruns what the
assessed corpus supports, the honest output is a narrowed `scope` plus a named
`corpus_gaps` entry — never a scope that asserts coverage the sources cannot
support.

**Name the gaps, and mark which matter.** Each `corpus_gaps` entry is marked
`material: true` when the gap is significant enough to be worth reporting as an
archive-gap story — for example, a development visible in one source with no
corresponding record where one was expected. A material gap carries
`gap_evidence`: the observation that establishes the gap exists. A gap that is
merely the scope's natural edge is recorded with `material: false`.

**Carry every inherited thread.** If a prior `ledger` is present, every thread
in its `open_threads` appears in the beat's `inherited_threads`. A thread is
not closed by being ignored.

## Red and Green Signals

- **Green (mechanical):** the `beat` validates against its schema — every
  `corpus_map` entry carries an `assessment`; every `corpus_gaps` entry is
  marked `material`.
- **Red (mechanical):** a missing or invalid `beat` — runa fails the protocol.
- **Red (methodological):** a `scope` claiming coverage `corpus_map` does not
  support; a source assessed more favorably than it merits; a material gap
  left unmarked or unevidenced; an inherited thread silently dropped. None is
  caught by schema validation; all are contract obligations of this protocol.

## Delivering the beat

```
beat({
  instance_id: "<brief.issue_id>",
  issue_id: "<brief.issue_id>",
  scope: "<the grounded, bounded scope>",
  corpus_map: [
    { locator: "...", description: "...", kind: "...",
      assessment: { reliability: "primary", freshness: "current",
                    completeness: "partial", ownership: "..." },
      discovered_from: "<locator that led here, if discovered>" }
  ],
  inherited_threads: [ /* threads from the prior ledger, or [] for issue one */ ],
  corpus_gaps: [
    { description: "...", material: true, gap_evidence: "..." }
  ]
})
```

Schema validity is not honesty: a `beat` whose scope outruns its `corpus_map`,
or whose assessments flatter weak sources, is structurally valid and
contractually wrong.
