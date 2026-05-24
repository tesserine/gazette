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

## What the repo contains

| Path | Contains |
|------|----------|
| `manifest.toml` | Artifact types and protocol declarations |
| `schemas/` | JSON Schema contract for each of the eight artifact types |
| `protocols/` | Six protocol definitions, one per stage |

v1 ships no skills. For how a runa methodology is structured, see runa's
[methodology authoring guide](https://github.com/tesserine/runa/blob/main/docs/methodology-authoring-guide.md).
