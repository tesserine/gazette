---
name: factcheck
description: >-
  Verifies a draft against its source trails, issuing one grounding verdict
  per claim — supported, partially supported, or unsupported — and counting
  the unsupported claims before publication.
---

# Factcheck

Factcheck is the chronicle's credibility gate. runa activates it when a
`draft` exists. Factcheck examines every claim the draft asserts, checks it
against the source it cites, and produces `grounding` — the per-claim verdict
that `publish` uses to decide what may go to print.

Factcheck exists because a chronicle's worth is its grounding. It does not
write and it does not fix; it reports the truth about whether each claim is
actually supported, and to what degree.

## Behavior Contract

**Given** a `draft` and a `dispatch`,
**when** factcheck runs,
**then** it produces a `grounding` carrying one verdict for every claim in the
draft — `supported`, `partially_supported`, or `unsupported` — with
`unsupported_count` equal to the number of unsupported verdicts.

## Goal

A `grounding` record that lets `publish` gate the issue on credibility: every
draft claim judged, the verdict honest, the unsupported ones counted, and the
partially-supported ones identified so `publish` can confirm they are honestly
qualified.

## Discipline

For each `claim` in the draft, examine the source it cites — `source_locator`,
traceable to the dispatch's `source_trail` — and judge how far that source
supports the claim's `statement`:

- **`supported`** — the source fully supports the statement as asserted.
- **`partially_supported`** — the source supports the statement only in part,
  or only indirectly. The verdict's `note` states what the source does and
  does not establish. A partially-supported verdict is the factcheck signal
  that the claim belongs in the issue only if the draft declared it
  `qualified` with stated limits — `publish` enforces that pairing.
- **`unsupported`** — the source does not support the statement. Counted in
  `unsupported_count`. Must not be published.

Judge the claim against its source, not against the claim's declared
confidence — factcheck verifies grounding independently of what `write`
asserted. A claim `write` marked `firm` that the source only partially
supports earns a `partially_supported` verdict; the mismatch is exactly what
factcheck exists to catch. Factcheck does not repair the draft; reporting a
`partially_supported` or `unsupported` verdict is factcheck working correctly,
not failing. `unsupported_count` must equal the count of `unsupported`
verdicts — partially-supported verdicts are not counted there.

## Red and Green Signals

- **Green (mechanical):** the `grounding` validates — verdict structure and
  the three-value status enum are schema-enforced.
- **Red (mechanical):** a malformed `grounding`; a status outside the enum.
- **The grounding signals:** `unsupported_count > 0`, and any
  `partially_supported` verdict, are values inside a *valid* artifact. runa
  cannot reject them — a correct factcheck of a flawed or hedged draft
  legitimately reports them. The *gates* on those signals live in `publish`'s
  contract. This is methodological by design.
- **Red (methodological):** a verdict missing for a draft claim; a dishonest
  `supported` verdict on a claim the source only partially supports; an
  `unsupported` claim graded `partially_supported` to ease its path to print.

## Delivering the grounding

```
grounding({
  instance_id: "<draft.issue_id>",
  issue_id: "<draft.issue_id>",
  claim_verdicts: [
    { claim_id: "...", status: "supported", checked_against: "..." },
    { claim_id: "...", status: "partially_supported", checked_against: "...",
      note: "what the source does and does not establish" }
  ],
  unsupported_count: 0
})
```
