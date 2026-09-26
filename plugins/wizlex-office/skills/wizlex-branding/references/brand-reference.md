# Wizlex website reference

Observed on September 26, 2026 at [wizlex.com](https://www.wizlex.com/). These are website-derived observations and practical production defaults, not a formally approved comprehensive brand manual. A newer official brand guide supplied by the user takes precedence; check the live website for changes on every task.

## Official logo

The same full-color horizontal SVG appears in the homepage header and footer. Its viewBox is `0 0 1020.6 144` (approximately 7.0875:1). The symbol is magenta and purple; the widely spaced WIZLEX wordmark is purple. All lettering is vector artwork. The bundled SVG preserves the original bytes and metadata. The accompanying 3062-pixel-wide transparent PNG is a direct rasterization for apps that cannot accept SVG.

Source: [official horizontal color SVG](https://cdn.prod.website-files.com/689d96ba2b48bedab74d4965/689d98e808abfa786df711d0_WIZLEX%20Logo%20Horizontal%20Color.svg). Discover its current replacement through the homepage, not by guessing filenames.

| Color | Value | Evidence and use |
| --- | --- | --- |
| Logo purple | `#6E2C90` | Original SVG `.cls-1` fill; preserve exactly |
| Logo magenta | `#D11A6E` | Original SVG `.cls-2` fill; preserve exactly |
| Website text | `#151515` | Stylesheet `--black` and computed body text |
| Website background | `#FFFFFF` | Stylesheet `--white` and computed body background |
| Website gray | `#EEEFF0` | Stylesheet `--gray` |
| Website accent | `#D82480` | Stylesheet `--accent` |
| Website accent 2 | `#882480` | Stylesheet `--accent2` |
| Website accent 3 | `#6C3094` | Stylesheet `--accent3` |

Do not recolor the logo to match the nearby website accent values. Use logo colors for identity-led graphics and the observed UI palette when closely matching the website; keep each source explicit.

## Typography and visual direction

The site's body and headings use **Satoshi, sans-serif**. Its stylesheet declares regular 400, medium 500, light 300, and italic faces. No font files are redistributed in this kit. Use Satoshi when available with appropriate usage rights; otherwise use a neutral sans-serif such as Arial and disclose the fallback. Never use any font to reconstruct the wordmark.

The live homepage uses white space, large dark sans-serif headlines, selective magenta/purple emphasis, thin dividing lines, strong rectangular content regions, and workplace/people photography. These observations guide new marketing assets; they are not fixed rules for every format. Create or use appropriately licensed imagery rather than bundling the website's third-party photographs or client logos.

The site's messaging emphasizes practical technology services and helping businesses bring ideas into use. Write clear, direct copy about the requested service or benefit. Verify claims for each assignment rather than copying historical website metrics.

## Practical defaults, not official specifications

- Keep at least half the displayed logo height clear on each side where space permits; increase space when the layout allows it. No official clear-space specification was found in the inspected sources.
- Keep the mark on white or a quiet light surface and preserve the original aspect ratio. Do not invent monochrome, stacked, symbol-only, or dark-mode variants.
- Establish one clear headline, short supporting copy, and an optional call to action. Let the logo identify the asset without overwhelming its content.
- Check the final export at its intended size, especially narrow mobile layouts. There is no verified universal minimum pixel width.

The retained Wizlex Word template has its own styling. Use that skill for document formatting and this skill for current logo verification and identity consistency.

## Source maintenance

`assets/brand-source.json` includes the exact observed stylesheet URL and content hash. The checker reports byte-level differences; a hash change is a reason to inspect, not proof of a substantive brand change. When the official logo changes, download its original file, visually compare it with the site's own use, regenerate raster derivatives, and update hashes and this reference. Never replace it with a generated lookalike.
