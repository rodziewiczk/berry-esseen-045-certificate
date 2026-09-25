import re
from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReleaseMetadataTests(unittest.TestCase):
    def test_release_version_is_consistent(self):
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        version = project["project"]["version"]
        dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
        compose = (ROOT / "compose.yaml").read_text(encoding="utf-8")
        citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")

        self.assertIn(f'org.opencontainers.image.version="{version}"', dockerfile)
        self.assertIn(f"berry-esseen-045-verifier:{version}", compose)
        self.assertRegex(citation, rf"(?m)^version: {re.escape(version)}$")

    def test_container_inputs_and_ci_actions_are_immutable(self):
        dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/tests.yml").read_text(encoding="utf-8")

        self.assertRegex(dockerfile, r"(?m)^# syntax=[^\s]+@sha256:[0-9a-f]{64}$")
        self.assertRegex(dockerfile, r"(?m)^FROM [^\s]+@sha256:[0-9a-f]{64}$")
        self.assertIn("--require-hashes", dockerfile)
        uses = re.findall(r"(?m)^\s*uses:\s*([^\s#]+)", workflow)
        self.assertTrue(uses)
        self.assertTrue(all(re.fullmatch(r"[^@]+@[0-9a-f]{40}", item) for item in uses))

    def test_documented_compose_commands_rebuild_the_image(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        commands = re.findall(r"(?m)^docker compose run .+$", readme)
        self.assertTrue(commands)
        self.assertTrue(all(" --build " in f" {command} " for command in commands))


if __name__ == "__main__":
    unittest.main()
