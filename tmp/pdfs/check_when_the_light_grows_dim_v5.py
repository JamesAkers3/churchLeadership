"""Verify the approved exact Scripture replacement and unchanged remaining v4 text."""

from hashlib import sha256
from itertools import combinations
from pathlib import Path
import re

import pdfplumber
from pypdf import PdfReader

ROOT = Path('/Users/jamesakers/Desktop/PERSONAL/James New Endeavor')
NEW = ROOT / 'output/pdf/when-the-light-grows-dim-v5.pdf'
OLD = ROOT / 'output/pdf/archive/when-the-light-grows-dim-v4.pdf'
PRESERVED = {
    'output/pdf/when-the-light-grows-dim-v1.pdf': 'f2800ae7eca84030926d380656683430fce9e4cc02d94c3b2f84191cbf16c468',
    'output/pdf/when-the-light-grows-dim-v2.pdf': '38c3fbf08c642160c15f7e45886eb85f81fdb7e20f3434f9351f9361d1c57692',
    'output/pdf/when-the-light-grows-dim-v3.pdf': '2888d14b24a42fe23785849c027d79f6f48c352a3758ffba0f7b0e6b7e228ac8',
    'output/pdf/when-the-light-grows-dim-talking-sheet-v1.pdf': '78d4b96e2f265f23382767f0cac0a172263ad9e3b4cae745ba0fcda0cdf7fa3a',
    'docs/strategy/when-the-light-grows-dim-framework.md': 'c493cfc4091b2ba24b4bb048579ba301c9fd1e17eded12ad1a14aafa0152c80c',
    'docs/strategy/assets/jesus-care-photomosaic-concept-v1.png': '32a92040fc57db7131cb876474bfbc946f505084057c0ab3391d7155c359fad5',
    'docs/strategy/assets/jesus-care-photomosaic-concept-v2.png': '81277ac1167af8766c0ca22ff6ec81f5002f2f1945b4674862f3e0299942a93b',
}
PRESERVED.update({
    "output/pdf/a-pastor-can-be-known-and-still-unsupported-v8.pdf": "fb4f38b80f0143a4252944c1bc29f1ab46df806938fc9ae338ab33c8e6269f3c",
    "output/pdf/christ-at-the-center-1-3-12-v2.pdf": "daac52b1209e7ced45335c218de9ff7ac7b214cbd2de6e2dce164f94fcdc107e",
    "output/pdf/christ-at-the-center-1-3-12-v3.pdf": "014c463b828c1d0f80dc6fce5053effa2ff14a6fe3d90567b13046c4a71fe2c5",
    "output/pdf/christ-at-the-center-1-3-12-v4.pdf": "68d5acb34ec071daa357ae51cc28f09e215caee20965b0d53e12a3e2a31234fa",
    "output/pdf/christ-at-the-center-1-3-12-v5.pdf": "76dccd4bdad6b8b7f8bd63a31fb43f6b00895767829e777dda91b810bcf7f995",
    "output/pdf/christ-at-the-center-1-3-12-v6.pdf": "32ed96b76dce811c001665b7c5fa82c585bd6f98a66e4827effb5d82fa73baf9",
    "output/pdf/christ-at-the-center-1-3-12-v7.pdf": "ae7fcbf6ed72e9c8210b6aedeb729622a4cec2d6b4f0e3fc8b5ffe38191116e0",
    "output/pdf/from-passion-to-impact-v8.pdf": "8b68836907991ea39cd04c8f3fe5e3410d46c9df12924a24eeabbc6d8a907176",
    "output/pdf/is-this-still-serving-the-calling-v1.pdf": "e41bb5d3510685c4af020b96614a171d190e777820770b19409d686e5b68298e",
    "output/pdf/is-this-still-serving-the-calling-v2.pdf": "76ed057754f0e51d84f950619110d14c92f0db812b3f4da8be80dce58431e022",
    "output/pdf/is-this-still-serving-the-calling-v3.pdf": "eb51638d0ebc49ba0766be4f5c33712ce0b5e580613f94bccb91a226567a739f",
    "output/pdf/is-this-still-serving-the-calling-v4.pdf": "0b93903c71abb63832c4543f33a25b6d361a0d71a17a3857e1f6b32a513e8618",
    "output/pdf/rooted-flourishing-multiplying-life-v8.pdf": "c77b640105533f2bd2153dd1636fcb0d8103b7bd58e55e6de0451240885b1c1b",
    "output/pdf/the-formation-gap-v3.pdf": "b1062725a0d198de66370f89b463ecd13544611c52020e659a74f9619f691ed2",
    "output/pdf/when-the-light-grows-dim-talking-sheet-v1.pdf": "78d4b96e2f265f23382767f0cac0a172263ad9e3b4cae745ba0fcda0cdf7fa3a",
    "output/pdf/when-the-light-grows-dim-v1.pdf": "f2800ae7eca84030926d380656683430fce9e4cc02d94c3b2f84191cbf16c468",
    "output/pdf/when-the-light-grows-dim-v2.pdf": "38c3fbf08c642160c15f7e45886eb85f81fdb7e20f3434f9351f9361d1c57692",
    "output/pdf/when-the-light-grows-dim-v3.pdf": "2888d14b24a42fe23785849c027d79f6f48c352a3758ffba0f7b0e6b7e228ac8",
    "output/pdf/when-the-light-grows-dim-v4.pdf": "9830109286b2c482cb48c9a71ac364632897ea9c95b79aceea0ea01a33f9cd23"
})


def tokens(path):
    return re.findall(r"\w+|[^\w\s]", PdfReader(path).pages[0].extract_text())


def check():
    quote = '“Come with me by yourselves to a quiet place and get some rest.”'
    old_paraphrase = (
        'When the disciples returned, Jesus heard what they had done and taught. '
        'They had not had time to eat. He invited them to come away and rest.'
    )
    old_label, new_label = 'MARK 6:30-32 / PARAPHRASE', 'MARK 6:31 / NIV / EXCERPT'
    old_text = ' '.join(PdfReader(OLD).pages[0].extract_text().split())
    assert old_text.count(old_paraphrase) == 1 and old_text.count(old_label) == 1
    expected = old_text.replace(old_paraphrase, quote).replace(old_label, new_label)
    assert tokens(NEW) == re.findall(r"\w+|[^\w\s]", expected), 'Unexpected wording change.'
    new_text = ' '.join(PdfReader(NEW).pages[0].extract_text().split())
    assert new_text.count(quote) == 1 and new_text.count(new_label) == 1
    assert 'PARAPHRASE' not in new_text and old_paraphrase not in new_text
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
        preserved_path = ROOT / path
        if not preserved_path.exists() and preserved_path.parent == ROOT / 'output/pdf':
            preserved_path = ROOT / 'output/pdf/archive' / preserved_path.name
        assert sha256(preserved_path.read_bytes()).hexdigest() == expected, path
    print('PASS: exact approved NIV excerpt/label, all other v4 words unchanged; one Letter page; zero images/annotations/links.')
    print('PASS: qualified evidence, capitalization, no visible version, bounds and no word/divider collisions.')
    print(f'PASS: {len(PRESERVED)} earlier PDF/framework/mosaic hashes unchanged.')
    print(f'v5 SHA-256: {sha256(NEW.read_bytes()).hexdigest()}')


if __name__ == '__main__':
    check()
