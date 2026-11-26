# House rules: typed tests, zero/boundary cases, and narrow exception assertions
# [GOOGLE-PYTHON] [MYPY]; isolated resources and assertion helpers [PY-UNITTEST].

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from batch_plan import BatchPlan
from plan_reader import PlanError, PlanFormatError, PlanReadError, read_plan


class PlanReaderTest(unittest.TestCase):
    def test_default_and_zero_limits(self) -> None:
        self.assertEqual(BatchPlan(label="Preview").limit, 100)
        self.assertEqual(BatchPlan(label="Preview", limit=0).limit, 0)
        self.assertEqual(BatchPlan(label="Preview", limit=1000).limit, 1000)

    def test_invalid_labels(self) -> None:
        for label in ("", "   ", "x" * 81):
            with self.subTest(label=label), self.assertRaises(ValueError):
                BatchPlan(label=label)

    def test_invalid_limits(self) -> None:
        for limit in (-1, 1001):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                BatchPlan(label="Preview", limit=limit)
        with self.assertRaises(TypeError):
            BatchPlan(label="Preview", limit=True)

    def test_reads_zero_limit(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "plan.txt"
            path.write_text("Preview\n0\n", encoding="utf-8")
            self.assertEqual(read_plan(path), BatchPlan(label="Preview", limit=0))

    def test_rejects_wrong_line_counts(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "plan.txt"
            for text in ("", "Preview\n", "Preview\n2\nextra\n"):
                path.write_text(text, encoding="utf-8")
                with self.subTest(text=text), self.assertRaises(PlanFormatError):
                    read_plan(path)

    def test_preserves_format_error_causes(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "plan.txt"
            for text in ("Preview\nseveral\n", "Preview\n-1\n", " \n2\n"):
                path.write_text(text, encoding="utf-8")
                with self.subTest(text=text):
                    with self.assertRaises(PlanFormatError) as caught:
                        read_plan(path)
                    self.assertIsInstance(caught.exception.__cause__, ValueError)
                    self.assertIsInstance(caught.exception, PlanError)

    def test_preserves_read_error_cause(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaises(PlanReadError) as caught:
                read_plan(Path(directory) / "missing.txt")
            self.assertIsInstance(caught.exception.__cause__, FileNotFoundError)

    def test_rejects_invalid_utf8(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "plan.txt"
            path.write_bytes(b"\xff\n1\n")
            with self.assertRaises(PlanFormatError) as caught:
                read_plan(path)
            self.assertIsInstance(caught.exception.__cause__, UnicodeError)
