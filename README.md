# Wizlex AI Skills

Two reusable skills, available together as the **Wizlex Office** Codex plugin or separately as individual skills.

| Skill | Purpose | Download |
| --- | --- | --- |
| [Wizlex Invoice Generator](plugins/wizlex-office/skills/wizlex-invoice-generator/SKILL.md) | Generate PDF freelancer invoices with user-provided billing details. | [Individual skill ZIP](packages/wizlex-invoice-generator.zip) |
| [Wizlex Document Format](plugins/wizlex-office/skills/artifact-template-wizlex-document-format/SKILL.md) | Create branded Word documents using the retained reference template. | [Individual skill ZIP](packages/artifact-template-wizlex-document-format.zip) |
| [Wizlex Office plugin](plugins/wizlex-office/.codex-plugin/plugin.json) | Both skills in one plugin. | [Plugin ZIP](packages/wizlex-office.zip) |

## Install the plugin

With Codex CLI installed and Git authenticated to this private repository:

```sh
codex plugin marketplace add https://github.com/wizlex-sieg/ai-skills.git
codex plugin add wizlex-office@personal
```

The repository's marketplace identifier is `personal`. Start a new Codex task after installation to load the skills. If you already have a different marketplace named `personal`, use the individual skill installation below to avoid a name conflict.

You can also clone the repository and register the local checkout:

```sh
git clone https://github.com/wizlex-sieg/ai-skills.git
codex plugin marketplace add ./ai-skills
codex plugin add wizlex-office@personal
```

The plugin ZIP contains the plugin directory and its manifest. The repository checkout includes the marketplace manifest used by the commands above.

## Install an individual skill

Download the corresponding ZIP from the table, then extract its skill folder into `$CODEX_HOME/skills` (normally `~/.codex/skills`, or `%USERPROFILE%\.codex\skills` on Windows). Each extracted folder must contain `SKILL.md` directly. Back up any existing folder with the same name before replacing it. Start a new task after installation.

Alternatively, ask Codex's skill installer to install one of these repository paths:

```text
plugins/wizlex-office/skills/wizlex-invoice-generator
plugins/wizlex-office/skills/artifact-template-wizlex-document-format
```

Both paths are complete, independent skill folders. Install either the plugin or the individual skills to avoid duplicate discovery.

## Requirements and usage

**Invoices:** Python 3.10 or later and ReportLab. If your runtime does not already include ReportLab, install the bundled requirements:

```sh
python -m pip install -r plugins/wizlex-office/skills/wizlex-invoice-generator/requirements.txt
```

Example prompt: `Use $wizlex-invoice-generator to invoice Wizlex for the September project milestone: PHP 25,000, dated September 26, 2026.` The skill asks for missing billing data and calculates the total from line items. See its [input schema](plugins/wizlex-office/skills/wizlex-invoice-generator/references/input-schema.md) for direct script usage and profile overrides. PDF rendering and visual inspection require an available PDF renderer in the agent's environment.

**Documents:** The Codex Documents plugin is a separate prerequisite; it is not bundled here. The skill invokes that plugin's template workflow to edit and render the retained DOCX.

Example prompt: `Use $artifact-template-wizlex-document-format to create a project proposal from this outline.`

## Retained assets

The invoice layout and Wizlex document styling are retained, with personal information replaced by placeholders. The invoice reference uses fictional sample billing data. The Word reference uses placeholder content, author, address, and contact fields; embedded custom XML, discarded content, metadata, and the original thumbnail have been removed. The preview is regenerated from the sanitized document.

Before making a real invoice, supply all billing and bank fields through a private input JSON outside the repository. Never commit completed invoices, private profiles, or real bank details. The document skill likewise requires user-provided content and contact information for each output.

## Build the packages

The canonical skill sources live under `plugins/wizlex-office/skills/`, so the plugin and standalone archives share the same files.

```sh
python scripts/build_packages.py
```

This regenerates the three ZIP files under `packages/` and their SHA-256 checksums. Python bytecode and cache directories are excluded.
