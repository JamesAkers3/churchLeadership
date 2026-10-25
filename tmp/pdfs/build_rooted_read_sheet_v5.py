"""Build the post-QA Rooted companion revision."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs/strategy/rooted-read-sheet-v5.md"
OUTPUT = ROOT / "output/pdf/rooted-flourishing-multiplying-life-read-sheet-v5.pdf"
MAP = ROOT / "tmp/pdfs/rooted-read-sheet-v5-content-map.json"

spec = spec_from_file_location("rooted_v4", ROOT / "tmp/pdfs/build_rooted_read_sheet_v4.py")
v4 = module_from_spec(spec)
spec.loader.exec_module(v4)

v4.SOURCE = SOURCE
v4.OUTPUT = OUTPUT
v4.MAP = MAP
v4.VERSION = "v5"


if __name__ == "__main__":
    v4.build()
