# Contributing

Contributions from researchers who have used the data are what make this site useful. A correction to a single value code saves the next user the same afternoon of detective work.

## Suggesting a correction

The simplest way to suggest a change is an email to [sihopark@kdischool.ac.kr](mailto:sihopark@kdischool.ac.kr?subject=NHIS%20Data%20Documentation). Please include the link to the page, the change you propose, and its source if there is one, such as a manual, a published paper, or your own experience with the data.

## Writing a post

Researchers who have worked with the data are welcome to write a post for [Research notes](../blog/index.md). A post can be short and cover a single pitfall, a way of constructing a variable, or a lesson from the application or export process. Send the draft by email to [sihopark@kdischool.ac.kr](mailto:sihopark@kdischool.ac.kr?subject=NHIS%20Data%20Documentation%20post) in any format, such as Word, Google Docs, or plain text, together with your name and affiliation as they should appear on the post. The draft is then formatted for the site and published under your name.

## Using GitHub

Contributors who use GitHub can also suggest a change there directly.

- **Open an issue.** Describe the problem or the missing information in a [GitHub issue](https://github.com/siho-park/nhis-documentation/issues).
- **Edit the page.** Every page has an edit button at the top right that opens its source file on GitHub, where you can propose the change as a pull request. On a variable page, the button opens the file for the whole table, and the fields of each entry are described [below](#how-the-variable-pages-are-built).

## What not to post

Never post individual-level records, screenshots of the analysis environment, or statistics computed from the data that have not passed the NHIS export review (반출 심사). Describing the structure of a variable, its codes, and its pitfalls is fine, but numbers from the data should be limited to results that have already been cleared for release, such as published tables.

## How the variable pages are built

The variable pages are generated from YAML files in the `codebook/` folder of the repository, with one folder per dataset and one file per table. Editing a variable means editing its entry in the YAML file, and the pages are rebuilt automatically.

```text
codebook/
  nsc/
    _dataset.yml    dataset title, years, and source documents
    _codes.yml      shared code lists, such as district codes
    bnc.yml         eligibility and premium table
    t20.yml         claim statement table
    ...
```

The YAML files are produced by the importer in `tools/importer/`, which reads the NHIS layout files and manuals, applies the corrections in `curate.py`, and adds the English translations kept in `tools/translations.tsv`. The importer can be run again when the NHIS publishes new documentation, and it leaves alone any variable whose status is `verified` or that carries `keep: true`.

### Table fields

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Short identifier, equal to the file name without `.yml` |
| `title`, `title_ko` | yes | English and Korean table names |
| `variables` | yes | List of variable entries |
| `files` | no | File names as delivered by the NHIS |
| `unit` | no | Unit of observation |
| `group` | no | `basic` or `additional`, for the customized research DB |
| `source` | no | Source document of the table layout |
| `description` | no | Free text shown above the variable list |
| `order` | no | Position on the dataset page |

### Variable fields

| Field | Required | Meaning |
|---|---|---|
| `name` | yes | Variable name as it appears in the data |
| `label_ko`, `label_en` | yes | Korean label from the official documentation and an English translation |
| `status` | yes | `documented`, `verified`, `unverified`, or `disputed`, used by the importer and not shown on the site |
| `verified_by`, `verified_on` | if verified | Name of the person who checked the entry and the date, as `YYYY-MM-DD` |
| `type`, `years` | no | Storage type and the years in which the variable exists |
| `notes` | no | List of notes in English, shown in a box at the top of the page |
| `periods` | no | One entry per span of years in which the documentation describes the variable the same way |
| `related` | no | Links to other variables, written `VAR`, `table.VAR`, or `dataset.table.VAR` |
| `keep` | no | `true` to protect a hand-edited entry from the importer |

Each period has `years`, `label_ko`, and `label_en`, and optionally a `description` and `notes` (lists of items with `en` and `ko`), `codes` (a list with `code`, `label_ko`, and `label_en`), and `code_list` (the name of a list in `_codes.yml`).

## Previewing the site locally

The site is built with [MkDocs](https://www.mkdocs.org) and the [Material](https://squidfunk.github.io/mkdocs-material/) theme. Install the requirements and start the local server, which rebuilds the site whenever a file changes.

```bash
pip install -r requirements.txt
mkdocs serve
```

The site is then available at `http://127.0.0.1:8000`.
