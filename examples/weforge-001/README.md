# Worked example: weforge-001

One complete Gazette issue, artifact by artifact — the input brief and every
artifact each protocol produces, through the published issue and the
continuity ledger. The directory layout mirrors a runa workspace
(`<artifact_type>/<instance_id>.json`), so any artifact here can seed a real
run.

**Content is illustrative; structure is normative.** The corpus, the
outage, and the journal are synthetic. What the example demonstrates is
real: every claim carries a source, a qualified claim's limits are visible
to the reader, an archive gap is reported as news, no candidate is silently
dropped, and the deferred candidate becomes a ledger thread for issue 002.

## The flow

| Protocol | Reads | Writes | In this example |
| --- | --- | --- | --- |
| (commission) | — | [`brief/weforge-001.json`](brief/weforge-001.json) | The editorial commission: chronicle WeForge's founding period |
| survey | brief (+ prior ledger) | [`beat/weforge-001.json`](beat/weforge-001.json) | Three assessed sources (one discovered by trail-following) and one **material corpus gap** |
| report | beat | [`dispatch/weforge-001.json`](dispatch/weforge-001.json) | Four grounded candidates: three developments and one `archive_gap` |
| edit | beat, dispatch | [`lineup/weforge-001.json`](lineup/weforge-001.json) | Three selected; one **deferred with a thread id**, not silently dropped |
| write | lineup, dispatch | [`draft/weforge-001.json`](draft/weforge-001.json) | Six claims; `weforge-001-c2-k2` is **qualified with stated `limits`** |
| factcheck | draft, dispatch | [`grounding/weforge-001.json`](grounding/weforge-001.json) | One verdict per claim; the qualified claim is `partially_supported`; `unsupported_count: 0` |
| publish | draft, grounding, lineup, beat | [`issue/weforge-001.json`](issue/weforge-001.json) + [`ledger/ledger.json`](ledger/ledger.json) | The published issue surfaces the qualified claim per story; the ledger opens the `weforge-ci-growth` thread |

Things to notice:

- **The grounding floor.** Every dispatch candidate and every draft claim
  carries a source trail — including the archive-gap story, whose trail
  cites the *evidence of absence* (an issue closed without resolution, a
  journal silent for the recovery window).
- **Qualified, not laundered.** The claim the record only partially
  supports is published hedged, with its limits in
  `issue.published_stories[].qualified_claims` where a reader can see them.
- **The archive gap is news.** `weforge-001-c3` reports what the record
  failed to preserve, and `coverage_report.archive_gaps_reported` accounts
  for it.
- **Continuity.** The deferred candidate's thread reappears in
  `ledger.open_threads`; the next issue's survey inherits it.

## Validation

```sh
python3 -m unittest discover -s tests   # from the repository root
```

`tests/test_schemas.py` validates every artifact here against its schema
and asserts the coherence properties above (claim coverage, qualified-claim
surfacing, no silent drops, thread carry-forward).
