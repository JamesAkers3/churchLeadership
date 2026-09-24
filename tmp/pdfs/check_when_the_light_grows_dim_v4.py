"""Content, preservation and page-structure checks for the image-free draft."""

from hashlib import sha256
from itertools import combinations
from pathlib import Path
import re

import pdfplumber
from pypdf import PdfReader

ROOT = Path('/Users/jamesakers/Desktop/PERSONAL/James New Endeavor')
NEW = ROOT / 'output/pdf/when-the-light-grows-dim-v4.pdf'
OLD = ROOT / 'output/pdf/when-the-light-grows-dim-v3.pdf'
PRESERVED = {
    'output/pdf/when-the-light-grows-dim-v1.pdf': 'f2800ae7eca84030926d380656683430fce9e4cc02d94c3b2f84191cbf16c468',
    'output/pdf/when-the-light-grows-dim-v2.pdf': '38c3fbf08c642160c15f7e45886eb85f81fdb7e20f3434f9351f9361d1c57692',
    'output/pdf/when-the-light-grows-dim-v3.pdf': '2888d14b24a42fe23785849c027d79f6f48c352a3758ffba0f7b0e6b7e228ac8',
    'output/pdf/when-the-light-grows-dim-talking-sheet-v1.pdf': '78d4b96e2f265f23382767f0cac0a172263ad9e3b4cae745ba0fcda0cdf7fa3a',
    'docs/strategy/when-the-light-grows-dim-framework.md': 'c493cfc4091b2ba24b4bb048579ba301c9fd1e17eded12ad1a14aafa0152c80c',
    'docs/strategy/assets/jesus-care-photomosaic-concept-v1.png': '32a92040fc57db7131cb876474bfbc946f505084057c0ab3391d7155c359fad5',
    'docs/strategy/assets/jesus-care-photomosaic-concept-v2.png': '81277ac1167af8766c0ca22ff6ec81f5002f2f1945b4674862f3e0299942a93b',
}


def tokens(path):
    return re.findall(r"\w+|[^\w\s]", PdfReader(path).pages[0].extract_text())


def check():
    assert tokens(NEW) == tokens(OLD), 'Word content or reading sequence changed.'
    reader = PdfReader(NEW)
    assert len(reader.pages) == 1
    page = reader.pages[0]
    assert tuple(map(float, page.mediabox)) == (0.0, 0.0, 612.0, 792.0)
    assert not page.get('/Annots'), 'Unexpected annotations/links.'
    text = page.extract_text()
    assert not re.search(r'\bv\d+\b', text, re.I), 'Visible version label.'
    assert not re.search(r'\bpastors?\b', text), 'Pastor title lost capitalization.'
    for phrase in [
        'frequently or sometimes.', '507 U.S. senior Protestant Pastors.',
        'not a diagnosis;', 'declined over the past decade.',
        'You can begin privately, with someone you trust.',
    ]:
        assert phrase in text, phrase
    with pdfplumber.open(NEW) as pdf:
        page = pdf.pages[0]
        assert not page.images, 'Image-free draft still contains an image.'
        words = page.extract_words()
        for word in words:
            assert 41 <= word['x0'] < word['x1'] <= 571, word
            assert 30 <= word['top'] < word['bottom'] <= 757, word
        for a, b in combinations(words, 2):
            overlap_x = min(a['x1'], b['x1']) - max(a['x0'], b['x0'])
            overlap_y = min(a['bottom'], b['bottom']) - max(a['top'], b['top'])
            assert not (overlap_x > 0.5 and overlap_y > 0.5), (a, b)
        for edge in page.edges:
            if edge['orientation'] != 'v' or abs(edge['x0'] - edge['x1']) > 0.1:
                continue
            for word in words:
                assert not (
                    word['x0'] < edge['x0'] < word['x1'] and
                    min(word['bottom'], edge['bottom']) > max(word['top'], edge['top'])
                ), ('Vertical divider intersects text', word)
    for path, expected in PRESERVED.items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    print('PASS: exact v3 word sequence; one Letter page; zero images/annotations/links.')
    print('PASS: qualified evidence, capitalization, no visible version, bounds and no word/divider collisions.')
    print(f'PASS: {len(PRESERVED)} earlier PDF/framework/mosaic hashes unchanged.')
    print(f'v4 SHA-256: {sha256(NEW.read_bytes()).hexdigest()}')


if __name__ == '__main__':
    check()
