# Left of Bang / Right of Bang

**A Resilience Maturity Model for Lean Security Teams**

NGO-ISAC briefing, November 5, 2026. Joseph Davis, Microsoft Security.

[View the slides](https://moffetcat.github.io/left-of-bang-right-of-bang-ngo-isac-briefing/)

[Download the PowerPoint](assets/left-of-bang-right-of-bang.pptx) | [View or download the PDF](assets/left-of-bang-right-of-bang.pdf)

The 24-slide briefing covers prevention, readiness, response, and recovery for lean security teams, with self-assessment worksheets, a sample tabletop exercise, an incident contact and decision log, and a printable maturity matrix.

The browser version includes static slide images and expandable slide text. It does not play animations or include speaker notes. The original PowerPoint is provided unchanged. PDF and browser images were exported with LibreOffice; font substitutions may differ from Microsoft PowerPoint.

This is an educational maturity model, not an audit or certification.

## Publishing

GitHub Pages serves the root of the `main` branch. No external presentation service, sign-in, or client-side dependency is needed.

## Updating the slides

Replace `assets/left-of-bang-right-of-bang.pptx`, export it as `assets/left-of-bang-right-of-bang.pdf`, then rebuild the gallery. The PDF must have one page per slide, in the same order as the PowerPoint.

On a system with Python 3, LibreOffice Impress, and Poppler (`pdftoppm`) installed:

```sh
libreoffice --headless --convert-to pdf --outdir assets assets/left-of-bang-right-of-bang.pptx
python3 tools/build_site.py
```

Commit the updated deck, PDF, slide images, and `index.html` to publish the changes.
