import pytest
from filer import Filer, AdvancedFiler

def test_line_generator(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("Line1\nLine2")
    fh = Filer(str(file))
    assert list(fh.line_generator()) == ["Line1", "Line2"]

def test_add_files(tmp_path):
    f1 = tmp_path / "f1.txt"
    f2 = tmp_path / "f2.txt"
    f1.write_text("A\nB")
    f2.write_text("C\nD")
    fh1 = Filer(str(f1))
    fh2 = Filer(str(f2))
    combined = fh1 + fh2
    with open(combined.filename) as f:
        assert f.read().strip() == "A\nB\nC\nD"

def test_average(tmp_path):
    f = tmp_path / "nums.txt"
    f.write_text("10\n20\n30")
    afh = AdvancedFiler(str(f))
    assert afh.average() == 20.0
