"""Exercise documentation failures on temporary Markdown fixtures."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location(
    "check_notes", Path(__file__).resolve().parents[1] / "scripts/check_notes.py"
)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class DocumentationChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def errors(self):
        return checker.check_repository(self.root)[0]

    def test_local_links_anchors_and_encoded_names(self):
        self.write("README.md", "# Home\n[Page](notes/a%20b.md#same-1)\n[Home](#home)\n")
        self.write("notes/a b.md", "# Page\n## Same\n## Same\n")
        self.assertEqual(self.errors(), [])

    def test_missing_file_and_anchor_are_reported(self):
        self.write("README.md", "# Home\n[Missing](missing.md)\n[Anchor](#absent)\n")
        errors = self.errors()
        self.assertEqual(len(errors), 2)
        self.assertIn("missing target", errors[0])
        self.assertIn("missing heading anchor", errors[1])

    def test_code_samples_do_not_create_links_or_titles(self):
        self.write("README.md", "# Home\n````markdown\n# Example\n[Example](missing.md)\n```\n````\n`[Example](missing.md)`\n")
        self.assertEqual(self.errors(), [])

    def test_unclosed_fence_and_extra_title(self):
        self.write("README.md", "# Home\n# Extra\n```python\nprint('example')\n")
        errors = self.errors()
        self.assertEqual(len(errors), 2)
        self.assertTrue(any("unclosed code fence" in error for error in errors))

    def test_reference_links_and_repository_boundary(self):
        self.write("README.md", "# Home\n[reference]: missing.md\n[Escape](../outside.md)\n")
        errors = self.errors()
        self.assertTrue(any("missing target" in error for error in errors))
        self.assertTrue(any("leaves repository" in error for error in errors))

    def test_external_links_are_not_fetched(self):
        self.write("README.md", "# Home\n[Web](https://example.org/missing#anchor)\n[Email](mailto:example@example.org)\n")
        self.assertEqual(self.errors(), [])


if __name__ == "__main__":
    unittest.main()
