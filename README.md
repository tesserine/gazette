# Gazette

Gazette is a methodology plugin for [runa](https://github.com/tesserine/runa),
a cognitive runtime for AI agents. It encodes how a *periodical chronicle* is
produced — researched, edited, written, verified, and published — into
protocols and artifact schemas that a runa instance orchestrates. It is not a
runtime or a framework; it is a methodology definition, a sibling of
[groundwork](https://github.com/tesserine/groundwork).

Where groundwork carries software from problem to merged change, Gazette
carries a historical record to a published newspaper issue, and maintains
continuity from one issue to the next.

## The shape of the methodology

One Gazette issue is one runa run. Six protocols, chained:

```
brief -> survey -> report -> edit -> write -> factcheck -> publish
                                                             |
                                                      issue + ledger
```

- **survey** establishes the issue's grounded scope and maps the source corpus.
- **report** mines the corpus into grounded story candidates.
- **edit** selects which candidates run and names what is omitted.
- **write** writes the selected candidates into reported stories.
- **factcheck** checks every claim against its source trail.
- **publish** assembles the verified issue and updates the continuity ledger.

Each protocol produces an artifact the next protocol requires. Topology
emerges from those requires/produces relationships; the manifest does not
declare it.

## Continuity

The `ledger` is the chronicle's running state — a singleton artifact,
produced by `publish`, carried by the orchestrator into the next issue's
workspace as `survey`'s continuity input. The cross-issue loop is not a runa
edge; it is an orchestrator-carried baton.

## Running an issue

One Gazette issue is one runa run in a fresh workspace.

1. Initialize a workspace on the gazette methodology (from an empty
   directory; `<gazette>` is this repository's path):

   ```sh
   runa init --methodology <gazette>/manifest.toml
   ```

2. Deliver the commission — a `brief` artifact. The worked example provides
   a valid one:

   ```sh
   mkdir -p .runa/workspace/brief
   cp <gazette>/examples/weforge-001/brief/weforge-001.json .runa/workspace/brief/
   runa scan && runa state
   ```

   `runa state` now reports `survey` READY and everything else WAITING.

3. Drive the run with your agent command (see
   [runa's CLI reference](https://github.com/tesserine/runa/blob/main/docs/cli-reference.md));
   runa chains survey → report → edit → write → factcheck → publish from
   the artifact graph:

   ```sh
   runa run --agent-command -- <agent argv>
   ```

   Success criterion: `runa run` exits `0`, and the workspace contains a
   valid `issue` artifact and the `ledger` singleton.

4. For the next issue, start a fresh workspace and carry the ledger in as
   survey's continuity input
   (`.runa/workspace/ledger/ledger.json`) before delivering the new brief.

## The artifact graph

| Protocol | Requires | Accepts | Produces | Triggered by |
|----------|----------|---------|----------|--------------|
| survey | brief | ledger | beat | brief |
| report | beat | — | dispatch | beat |
| edit | beat, dispatch | — | lineup | dispatch |
| write | lineup, dispatch | — | draft | lineup |
| factcheck | draft, dispatch | — | grounding | draft |
| publish | draft, grounding, lineup, beat | — | issue, ledger | grounding |

The schema for each artifact (in `schemas/`) names its producer and
consumers in its `description`.

## What the repo contains

| Path | Contains |
|------|----------|
| `manifest.toml` | Artifact types and protocol declarations |
| `schemas/` | JSON Schema contract for each of the eight artifact types |
| `protocols/` | Six protocol definitions, one per stage |
| `examples/weforge-001/` | A complete worked issue: brief through published issue and ledger ([guide](examples/weforge-001/README.md)) |
| `tests/` | Schema validity + example conformance gate (`python3 -m unittest discover -s tests`) |

## Reporting under imperfect archives (v0.2)

A chronicle rarely meets a tidy archive. Gazette v0.2 is built to report
honestly from an incomplete or messy record:

- **Source discovery** — `survey` follows trails outward from the brief's
  initial pointers (git history, trackers, orientations, live substrate),
  recording where each discovered source was reached from.
- **Source quality** — every source in the `corpus_map` carries an
  `assessment` of reliability, freshness, and completeness, so later
  protocols know how much weight it can bear.
- **Declared uncertainty** — a claim the record only partially supports is
  published as a `qualified` claim with its `limits` stated, never as a firm
  fact and never without a source. The grounding floor is absolute: every
  claim carries a source trail.
- **Archive gaps as news** — when the record is materially silent on
  something a reader would expect, that silence can become an `archive_gap`
  story, grounded in the evidence of absence. The newspaper reports the state
  of the archive, not only the state of the project.

This makes Gazette an observability instrument as much as a publication: its
output shows what the surrounding system preserves, misses, and cannot ground.

v0.2 ships no skills. For how a runa methodology is structured, see runa's
[methodology authoring guide](https://github.com/tesserine/runa/blob/main/docs/methodology-authoring-guide.md).

Principles: [pentaxis93/principles](https://github.com/pentaxis93/principles)
— the canonical corpus governing the ecosystem's decisions. Ecosystem
conventions and the source-of-truth map:
[tesserine/commons](https://github.com/tesserine/commons).
