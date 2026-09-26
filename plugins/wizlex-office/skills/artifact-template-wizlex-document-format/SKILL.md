---
name: artifact-template-wizlex-document-format
description: "Create a document using the Wizlex Document Format template and its retained reference file. Use when the user selects this template, names Wizlex Document Format, or explicitly invokes $artifact-template-wizlex-document-format. Create professional Wizlex Word documents using the approved purple brand system, cover page, typography, headers, footers, tables, and content hierarchy."
---

# Wizlex Document Format

Create a document from this template. Keep the reference file unchanged. The distributed reference is sanitized: its content, author, address, and contact fields are placeholders. Replace them with user-provided information for each document; never treat sample text as factual content.

## Workflow

1. Read `artifact-template.json` and resolve its paths relative to this skill directory.
2. If running in Codex with the Documents plugin available, use its reference/template workflow. Otherwise use the host agent's document tools and [references/portable-workflow.md](references/portable-workflow.md). A Codex-specific plugin is not required in other agents.
3. Treat the user's prompt and available sources as the content input. Do not invent facts merely to fill a template slot.
4. Clone or import the reference instead of replacing its visual system with generic defaults.
5. Render and verify the finished document, then return the final artifact. If the environment cannot render DOCX, report that limitation and identify the output as an unverified draft rather than claiming visual verification.

## Fidelity

Preserve page setup, sections, styles, lists, tables, headers, footers, and recurring page elements.

User instructions control requested content and explicit deviations. The retained reference controls layout and formatting where the user has not requested a change.
