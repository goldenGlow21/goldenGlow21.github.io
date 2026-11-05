"""Tests for tools/post.py. Run with: python -m unittest discover tools"""

import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from post import PostError, create, parse_tags, publish

KST = timezone(timedelta(hours=9))
DAY_ONE = datetime(2026, 11, 5, 21, 30, 0, tzinfo=KST)
DAY_TWO = datetime(2026, 11, 8, 9, 0, 0, tzinfo=KST)


class PostToolTest(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)

    def tearDown(self):
        self._dir.cleanup()

    def test_new_post_is_named_by_date_and_slug(self):
        path = create(self.root, "first-note", "First", [], False, DAY_ONE)
        self.assertEqual(path, self.root / "_posts" / "2026-11-05-first-note.md")

    def test_new_post_front_matter_quotes_title_and_lists_tags(self):
        path = create(self.root, "a", 'Title: "quoted"', ["tag1", "tag2"],
                      False, DAY_ONE)
        text = path.read_text(encoding="utf-8")
        self.assertIn('title: "Title: \\"quoted\\""\n', text)
        self.assertIn('tags: ["tag1", "tag2"]\n', text)
        self.assertIn("date: 2026-11-05 21:30:00 +0900\n", text)

    def test_korean_title_is_written_unescaped(self):
        path = create(self.root, "a", "한글 제목", [], False, DAY_ONE)
        self.assertIn('title: "한글 제목"', path.read_text(encoding="utf-8"))

    def test_draft_goes_to_drafts_without_date_in_name(self):
        path = create(self.root, "wip", "WIP", [], True, DAY_ONE)
        self.assertEqual(path, self.root / "_drafts" / "wip.md")

    def test_invalid_slug_is_rejected(self):
        for slug in ["Upper", "has space", "trailing-", "a--b", "한글", ""]:
            with self.subTest(slug=slug), self.assertRaises(PostError):
                create(self.root, slug, "t", [], False, DAY_ONE)

    def test_slug_used_by_a_post_on_another_day_is_rejected(self):
        create(self.root, "dup", "t", [], False, DAY_ONE)
        with self.assertRaises(PostError):
            create(self.root, "dup", "t", [], False, DAY_TWO)

    def test_slug_used_by_a_draft_is_rejected(self):
        create(self.root, "dup", "t", [], True, DAY_ONE)
        with self.assertRaises(PostError):
            create(self.root, "dup", "t", [], False, DAY_ONE)

    def test_longer_slug_with_same_suffix_is_not_a_conflict(self):
        create(self.root, "my-notes", "t", [], False, DAY_ONE)
        create(self.root, "notes", "t", [], False, DAY_ONE)

    def test_publish_moves_draft_and_sets_todays_date(self):
        create(self.root, "wip", "WIP", ["x"], True, DAY_ONE)
        path = publish(self.root, "wip", DAY_TWO)
        self.assertEqual(path, self.root / "_posts" / "2026-11-08-wip.md")
        self.assertFalse((self.root / "_drafts" / "wip.md").exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("date: 2026-11-08 09:00:00 +0900\n", text)
        self.assertNotIn("2026-11-05", text)

    def test_publish_without_draft_fails(self):
        with self.assertRaises(PostError):
            publish(self.root, "missing", DAY_ONE)

    def test_publish_draft_without_date_line_fails_and_keeps_draft(self):
        drafts = self.root / "_drafts"
        drafts.mkdir()
        (drafts / "nodate.md").write_text("---\ntitle: t\n---\n", encoding="utf-8")
        with self.assertRaises(PostError):
            publish(self.root, "nodate", DAY_ONE)
        self.assertTrue((drafts / "nodate.md").exists())

    def test_parse_tags_drops_blanks_and_spaces(self):
        self.assertEqual(parse_tags(" tag1, ,tag2 ,"), ["tag1", "tag2"])
        self.assertEqual(parse_tags(""), [])


if __name__ == "__main__":
    unittest.main()
