# NHIS Data Documentation

Source for an unofficial documentation site for the research databases of the Korean National Health Insurance Service (NHIS). The site is built with [MkDocs](https://www.mkdocs.org) and the [Material](https://squidfunk.github.io/mkdocs-material/) theme and is published with GitHub Pages.

## Repository layout

```text
codebook/                 variable documentation as YAML, one folder per dataset
  nsc/, heals/, senior/, lowrisk/, custom/
    _dataset.yml          dataset title, years, and source documents
    _codes.yml            shared code lists
    <table>.yml           one file per table
docs/                     hand-written pages
scripts/gen_codebook.py   turns codebook/ into the Variables section at build time
tools/importer/           reads the NHIS layout files and manuals into codebook/
tools/translations.tsv    English translations of every Korean string in the codebook
overrides/                theme overrides (the draft banner)
mkdocs.yml                site configuration and navigation
```

The Variables section is generated from `codebook/` on every build, with one page per variable. Edit the YAML files, never the generated pages, which exist only in the build output. The field reference is in `docs/about/contributing.md`.

## Re-importing the NHIS documentation

The NHIS documentation files are kept in `database/`, which is not committed (see `.gitignore`). When the NHIS publishes a new layout or manual, place it there, update the file names in `tools/importer/run.py` if needed, and run the steps below from the repository root.

```bash
python tools/importer/run.py database ir                      # parse layouts and manuals into ir/*.json
python tools/importer/strings.py ir tools/translations.tsv todo.tsv   # list Korean strings without a translation
python tools/importer/romanize_sgg.py ir/nsc.json tools/translations.tsv   # district names
python tools/importer/build_codebook.py ir tools/translations.tsv codebook
```

The second step writes the untranslated strings to `todo.tsv`. Add their translations to `tools/translations.tsv` (Korean, a tab, then English) before running the third step, which stops if any string is missing. Variables marked `verified` or `keep: true` in `codebook/` are not overwritten.

## Previewing locally

```bash
pip install -r requirements.txt
mkdocs serve
```

The site is then served at `http://127.0.0.1:8000` and rebuilds when a file changes. Because this folder sits in Dropbox, create any virtual environment outside it so that Dropbox does not sync the installed packages.

## Publishing

Pushing to the `main` branch runs `.github/workflows/deploy.yml`, which builds the site in strict mode and publishes it to the `gh-pages` branch. The repository settings set GitHub Pages to deploy from the `gh-pages` branch, and the site is served at https://siho-park.github.io/nhis-documentation/.
