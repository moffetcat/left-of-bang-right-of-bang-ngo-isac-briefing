#!/usr/bin/env python3
"""Build a static slide gallery from the PowerPoint and its PDF export."""

import html
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
STEM = "left-of-bang-right-of-bang"
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}


def main():
    with zipfile.ZipFile(ASSETS / f"{STEM}.pptx") as deck:
        names = sorted(
            (n for n in deck.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
            key=lambda n: int(re.search(r"(\d+)\.xml$", n).group(1)),
        )
        slides = []
        for name in names:
            root = ET.fromstring(deck.read(name))
            paragraphs = [
                "".join(t.text or "" for t in p.findall(".//a:t", NS)).strip()
                for p in root.findall(".//a:p", NS)
            ]
            slides.append([p for p in paragraphs if p])

    with tempfile.TemporaryDirectory() as temp:
        prefix = Path(temp) / "slide"
        subprocess.run(
            ["pdftoppm", "-jpeg", "-jpegopt", "quality=90", "-scale-to", "1920",
             str(ASSETS / f"{STEM}.pdf"), str(prefix)],
            check=True,
        )
        images = sorted(prefix.parent.glob("slide-*.jpg"))
        if len(images) != len(slides):
            raise RuntimeError("The PDF page count does not match the PowerPoint slide count.")
        for number, image in enumerate(images, 1):
            shutil.copyfile(image, ASSETS / f"slide-{number:02}.jpg")

    sections = []
    options = []
    for number, paragraphs in enumerate(slides, 1):
        title = html.escape(paragraphs[0] if paragraphs else f"Slide {number}")
        options.append(f'<option value="slide-{number}">{number}. {title}</option>')
        transcript = "".join(f"<p>{html.escape(p)}</p>" for p in paragraphs)
        loading = 'fetchpriority="high"' if number == 1 else 'loading="lazy"'
        sections.append(f"""
<section id="slide-{number}" aria-labelledby="heading-{number}">
  <h2 id="heading-{number}"><span>{number} / {len(slides)}</span> {title}</h2>
  <a href="assets/slide-{number:02}.jpg" aria-label="Open slide {number} at full size">
    <img src="assets/slide-{number:02}.jpg" width="1920" height="1080"
         alt="Slide {number}: {title}. Text version below." {loading}>
  </a>
  <details><summary>Slide {number} text</summary>{transcript}</details>
</section>""")

    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Left of Bang / Right of Bang | NGO-ISAC Briefing</title>
<meta name="description" content="A resilience maturity model for lean security teams. View all 24 slides from the NGO-ISAC briefing or download the PowerPoint and PDF.">
<meta property="og:title" content="Left of Bang / Right of Bang">
<meta property="og:description" content="A Resilience Maturity Model for Lean Security Teams | NGO-ISAC Briefing">
<meta name="color-scheme" content="dark">
<style>
* { box-sizing: border-box; }
html { scroll-padding-top: 6rem; }
body { margin: 0; background: #0c1424; color: #eef3fb; font: 1rem/1.6 system-ui, sans-serif; }
a { color: #8dded8; text-underline-offset: .2em; }
a:focus-visible, select:focus-visible, summary:focus-visible { outline: 3px solid #ffc043; outline-offset: 4px; }
.skip { position: absolute; left: 1rem; top: -5rem; }
.skip:focus { top: 1rem; background: #0c1424; z-index: 3; }
header, main, footer { max-width: 1280px; margin: auto; padding: 1.5rem; }
header { padding-top: 3rem; }
.eyebrow { color: #8dded8; letter-spacing: .12em; text-transform: uppercase; }
h1 { font-size: clamp(2rem, 5vw, 3.5rem); line-height: 1.15; margin: .5rem 0 1rem; }
.subtitle { font-size: 1.25rem; }
.downloads { display: flex; flex-wrap: wrap; gap: .75rem; margin: 1.5rem 0; }
.downloads a { border: 1px solid #53718c; border-radius: .5rem; padding: .6rem 1rem; text-decoration: none; }
.downloads a:hover { background: #1d3046; }
nav { position: sticky; top: 0; z-index: 1; background: #132136; border-block: 1px solid #34465c; padding: .75rem 1.5rem; }
nav div { max-width: 1232px; margin: auto; display: flex; align-items: center; gap: .75rem; }
select { min-width: 0; max-width: 100%; flex: 1; background: #0c1424; color: #eef3fb; border: 1px solid #53718c; border-radius: .3rem; padding: .5rem; font: inherit; }
section { margin-bottom: 3rem; }
h2 { font-size: 1.1rem; font-weight: 500; }
h2 span { color: #aabdd2; display: inline-block; margin-right: .5rem; }
img { display: block; width: 100%; height: auto; border: 1px solid #34465c; border-radius: .4rem; }
details { margin-top: .75rem; color: #c9d6e6; }
summary { cursor: pointer; width: fit-content; }
details p { margin: .4rem 0; }
footer { color: #aabdd2; border-top: 1px solid #34465c; }
@media (max-width: 600px) { header, main, footer { padding-inline: 1rem; } nav { padding-inline: 1rem; } }
@media print {
  body { background: white; color: black; }
  header, nav, footer, h2, details { display: none; }
  main { padding: 0; max-width: none; }
  section { break-after: page; margin: 0; }
  img { border: 0; }
}
</style>
</head>
<body>
<a class="skip" href="#slides">Skip to slides</a>
<header>
  <p class="eyebrow">NGO-ISAC Briefing | November 5, 2026</p>
  <h1>Left of Bang / Right of Bang</h1>
  <p class="subtitle">A Resilience Maturity Model for Lean Security Teams</p>
  <p>Joseph Davis | Microsoft Security</p>
  <div class="downloads">
    <a href="assets/left-of-bang-right-of-bang.pptx" download>Download PowerPoint (.pptx)</a>
    <a href="assets/left-of-bang-right-of-bang.pdf">View / download PDF</a>
  </div>
  <p>24 slides, including worksheets and appendix tools. Scroll to browse, or jump to a slide.
  Select a slide image to open it at full size. Browser slides are static; the original PowerPoint is available above.</p>
</header>
<nav aria-label="Slide navigation"><div>
  <label for="jump">Jump to slide</label>
  <select id="jump"><option value="">Choose a slide</option>OPTIONS</select>
</div></nav>
<main id="slides">SECTIONS</main>
<footer>Educational maturity model, not an audit or certification.
<a href="https://github.com/moffetcat/left-of-bang-right-of-bang-ngo-isac-briefing">View on GitHub</a></footer>
<script>
document.getElementById('jump').addEventListener('change', function () {
  if (this.value) {
    const slide = document.getElementById(this.value);
    history.replaceState(null, '', '#' + this.value);
    slide.scrollIntoView();
    const heading = slide.querySelector('h2');
    heading.tabIndex = -1;
    heading.focus({preventScroll: true});
  }
});
</script>
</body>
</html>
"""
    page = page.replace("OPTIONS", "\n".join(options)).replace("SECTIONS", "\n".join(sections))
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    (ROOT / ".nojekyll").touch()


if __name__ == "__main__":
    main()
