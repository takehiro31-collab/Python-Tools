import tempfile
import unittest
from pathlib import Path

from organize import organize


class OrganizeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = Path(self.tmp.name)
        for name in ["photo.JPG", "memo.pdf", "data.csv", "song.mp3", "unknown.xyz", ".DS_Store"]:
            (self.folder / name).write_text("x")
        (self.folder / "既存フォルダ").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_dry_run_moves_nothing(self):
        self.assertEqual(organize(self.folder), 5)
        self.assertTrue((self.folder / "photo.JPG").exists())
        self.assertFalse((self.folder / "画像").exists())

    def test_run_sorts_by_type(self):
        organize(self.folder, run=True)
        self.assertTrue((self.folder / "画像" / "photo.JPG").exists())
        self.assertTrue((self.folder / "文書" / "memo.pdf").exists())
        self.assertTrue((self.folder / "表計算" / "data.csv").exists())
        self.assertTrue((self.folder / "音楽" / "song.mp3").exists())
        self.assertTrue((self.folder / "その他" / "unknown.xyz").exists())
        self.assertTrue((self.folder / ".DS_Store").exists())
        self.assertTrue((self.folder / "既存フォルダ").is_dir())

    def test_same_name_is_not_overwritten(self):
        (self.folder / "画像").mkdir()
        (self.folder / "画像" / "photo.JPG").write_text("old")
        organize(self.folder, run=True)
        self.assertEqual((self.folder / "画像" / "photo.JPG").read_text(), "old")
        self.assertTrue((self.folder / "画像" / "photo (2).JPG").exists())


if __name__ == "__main__":
    unittest.main()
