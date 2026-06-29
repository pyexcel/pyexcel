# Changelog Agent Notes

I reviewed [changelog.yml](changelog.yml) and understand its structure.

## Current format
- Top-level keys:
  - `name`: package name (`pyexcel-io`)
  - `organisation`: org name (`pyexcel`)
  - `releases`: list of release entries (newest first)
- Each release contains:
  - `version`
  - `date` (currently mixed formats, e.g. `09.11.2024`, `31.1.2022`)
  - `changes`: list of change groups
- Each change group contains:
  - `action` (examples: `added`, `updated`, `fixed`, `removed`; some older entries use capitalized variants)
  - `details`: list of bullet strings

## Content patterns observed
- Issue references often use inline markers like `#115`, `pyexcel#185`, `pyexcel-ods#33`, `PR#44`.
- One release can have multiple action groups.
- Older releases include longer narrative detail lines.
- Action casing is inconsistent in historical entries (`Added`/`Updated` vs lowercase).

## Authoring rules (your convention)
- Add new unreleased changes under the highest version entry.
- If a version is not released yet, set `date: tbd`.
- For normal code updates without a known issue, use `action: updated`.
- If a feature was removed, use `action: removed`.
- If a feature was added, use `action: added`.
- For each change, append a new detail line under the matching action block's `details` list.

## Issue reference notation
- `#45` means issue 45 in the current project repository.
- `pyexcel#45` means issue 45 in the `pyexcel` repository.
- Keep these as plain inline references in changelog text (no URL expansion needed).

## Ready to apply
I will follow these rules for all future changelog updates in [changelog.yml](changelog.yml).

## pyexcel-io.yml rules
- In [pyexcel-io.yml](pyexcel-io.yml), `version` and `current_version` must always be the same (current development version).
- `release` means the latest released version.
- `copyright_year` is a range from project start year to current year.
- On version bump requests, update both `version` and `current_version` together.

## Version bump exclusions (important)
- Do **not** edit [setup.py](setup.py) for version bumps.
- Do **not** edit [setup.cfg](setup.cfg) for version bumps.
- Do **not** search [setup.cfg](setup.cfg) for version references.
- Do **not** edit [pyexcel/__init__.py](pyexcel/__init__.py) for version bumps.
- Do **not** edit [docs/source/conf.py](docs/source/conf.py) for version bumps.
- Do **not** edit [pyexcel/__version__.py](pyexcel/__version__.py) for version bumps.
- Do **not** edit [CHANGELOG.rst](CHANGELOG.rst) for version bumps.
- These files are maintained by other tooling in this repository.
