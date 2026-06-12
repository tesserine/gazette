"""Schema validity and example conformance gate.

Every schema must be a valid JSON Schema against its declared draft, and
every artifact in examples/ must validate against the schema named by its
parent directory. A schema typo or a drifting example fails here instead
of shipping.
"""

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
EXAMPLES_DIR = ROOT / "examples"

ARTIFACT_TYPES = [
    "brief",
    "beat",
    "dispatch",
    "lineup",
    "draft",
    "grounding",
    "issue",
    "ledger",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class SchemaTests(unittest.TestCase):
    def test_manifest_artifact_types_each_have_a_schema(self) -> None:
        manifest = (ROOT / "manifest.toml").read_text(encoding="utf-8")
        for artifact_type in ARTIFACT_TYPES:
            with self.subTest(artifact_type=artifact_type):
                self.assertIn(f'name = "{artifact_type}"', manifest)
                self.assertTrue(
                    (SCHEMA_DIR / f"{artifact_type}.schema.json").is_file(),
                    f"schemas/{artifact_type}.schema.json is missing",
                )

    def test_every_schema_file_is_covered_by_the_artifact_type_list(self) -> None:
        on_disk = sorted(p.name for p in SCHEMA_DIR.glob("*.schema.json"))
        expected = sorted(f"{t}.schema.json" for t in ARTIFACT_TYPES)
        self.assertEqual(expected, on_disk)

    def test_schemas_are_valid_against_their_declared_draft(self) -> None:
        for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
            with self.subTest(schema=path.name):
                schema = load_json(path)
                self.assertEqual(
                    schema.get("$schema"),
                    "https://json-schema.org/draft/2020-12/schema",
                )
                Draft202012Validator.check_schema(schema)


class ExampleConformanceTests(unittest.TestCase):
    def example_artifacts(self):
        for example in sorted(EXAMPLES_DIR.iterdir()):
            if not example.is_dir():
                continue
            for artifact in sorted(example.glob("*/*.json")):
                yield example.name, artifact.parent.name, artifact

    def test_examples_exist_to_validate(self) -> None:
        self.assertNotEqual([], list(self.example_artifacts()))

    def test_every_example_artifact_validates_against_its_schema(self) -> None:
        for example, artifact_type, path in self.example_artifacts():
            with self.subTest(example=example, artifact=f"{artifact_type}/{path.name}"):
                self.assertIn(
                    artifact_type,
                    ARTIFACT_TYPES,
                    f"{path} sits under unknown artifact type {artifact_type}",
                )
                schema = load_json(SCHEMA_DIR / f"{artifact_type}.schema.json")
                Draft202012Validator(schema).validate(load_json(path))


class WorkedExampleCoherenceTests(unittest.TestCase):
    """The weforge-001 example demonstrates the methodology's load-bearing
    properties; these tests keep them demonstrated."""

    EXAMPLE = EXAMPLES_DIR / "weforge-001"

    def artifact(self, artifact_type: str, instance: str) -> dict:
        return load_json(self.EXAMPLE / artifact_type / f"{instance}.json")

    def test_grounding_covers_every_draft_claim(self) -> None:
        draft = self.artifact("draft", "weforge-001")
        grounding = self.artifact("grounding", "weforge-001")
        draft_claims = {
            claim["claim_id"]
            for story in draft["stories"]
            for claim in story["claims"]
        }
        verdict_claims = {v["claim_id"] for v in grounding["claim_verdicts"]}
        self.assertEqual(draft_claims, verdict_claims)

    def test_unsupported_count_matches_unsupported_verdicts(self) -> None:
        grounding = self.artifact("grounding", "weforge-001")
        unsupported = [
            v for v in grounding["claim_verdicts"] if v["status"] == "unsupported"
        ]
        self.assertEqual(len(unsupported), grounding["unsupported_count"])

    def test_example_shows_a_qualified_claim_with_visible_limits(self) -> None:
        draft = self.artifact("draft", "weforge-001")
        qualified = [
            claim
            for story in draft["stories"]
            for claim in story["claims"]
            if claim["confidence"] == "qualified"
        ]
        self.assertNotEqual([], qualified)
        for claim in qualified:
            self.assertTrue(claim.get("limits"), f"{claim['claim_id']} lacks limits")
        issue = self.artifact("issue", "weforge-001")
        surfaced = {
            qc["claim_id"]
            for story in issue["published_stories"]
            for qc in story.get("qualified_claims", [])
        }
        for claim in qualified:
            self.assertIn(claim["claim_id"], surfaced)

    def test_example_shows_an_archive_gap_story(self) -> None:
        issue = self.artifact("issue", "weforge-001")
        gap_stories = [
            s for s in issue["published_stories"] if s["kind"] == "archive_gap"
        ]
        self.assertNotEqual([], gap_stories)
        self.assertEqual(
            sorted(s["candidate_id"] for s in gap_stories),
            sorted(issue["coverage_report"]["archive_gaps_reported"]),
        )

    def test_no_dispatch_candidate_is_silently_dropped(self) -> None:
        dispatch = self.artifact("dispatch", "weforge-001")
        lineup = self.artifact("lineup", "weforge-001")
        candidates = {c["candidate_id"] for c in dispatch["candidates"]}
        selected = {s["candidate_id"] for s in lineup["selected"]}
        omitted = {o["candidate_id"] for o in lineup["omitted"]}
        self.assertEqual(candidates, selected | omitted)
        self.assertEqual(set(), selected & omitted)

    def test_ledger_carries_the_deferred_thread(self) -> None:
        lineup = self.artifact("lineup", "weforge-001")
        ledger = load_json(self.EXAMPLE / "ledger" / "ledger.json")
        deferred_threads = {
            o["thread_id"] for o in lineup["omitted"] if o["disposition"] == "deferred"
        }
        open_threads = {t["thread_id"] for t in ledger["open_threads"]}
        self.assertTrue(deferred_threads <= open_threads)


if __name__ == "__main__":
    unittest.main()
