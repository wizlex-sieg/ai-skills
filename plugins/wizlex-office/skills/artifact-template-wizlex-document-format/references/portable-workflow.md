# Portable document workflow

Use this workflow in Claude Code, Cursor, Copilot, or another agent without the Codex Documents plugin. Resolve all paths relative to this skill directory, not the process working directory.

1. Read `artifact-template.json`. Copy its `reference` DOCX into the user's output workspace. Keep the bundled template unchanged.
2. Inspect the copied DOCX's sections, paragraphs, tables, styles, headers, and footers. Use an available document editor or a DOCX library such as Python's `python-docx`. Do not rebuild the document from a blank default file.
3. Replace placeholder content with the user's facts. Match paragraphs to their role rather than globally replacing repeated placeholder strings. Preserve run formatting where possible; assigning an entire paragraph's text can remove its character styling. Edit existing tables and preserve cell widths, fills, and section settings. Remove unused sample sections only when appropriate to the requested document.
4. Replace author and contact placeholders only with task-specific supplied details. Do not save personal data back into the skill. If a current logo check is needed, use the branding skill when installed or check the official Wizlex site directly; do not redraw the logo.
5. Save the result as DOCX. Render it with available Word, LibreOffice, or the host's document renderer, then inspect every page image. A common local pipeline is `soffice --headless --convert-to pdf --outdir <qa-dir> <output.docx>`, followed by `pdftoppm -png <qa-dir>/<output-stem>.pdf <qa-dir>/page`. Use a writable QA directory outside the skill and quoted paths as needed for the operating system.
6. Correct clipping, overlaps, orphaned headings, broken tables, and unwanted blank pages, then render again. Deliver the DOCX and any other formats the user requested. If rendering or image inspection is unavailable, clearly identify the result as a draft with visual verification outstanding.

Requirements depend on the chosen tools: `python-docx` is needed only for that editing route; Word or LibreOffice can render DOCX; Poppler can rasterize the PDF. Use existing equivalents when available. Do not imply the skill itself supplies these applications or automatically installs them.
