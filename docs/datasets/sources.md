# Sources and versions

Every dataset page and codebook entry on this site rests on an NHIS document, and this page records which version of each is followed. When the NHIS publishes a newer document, the older one is kept here as superseded so that readers can tell which description applies to their extract.

## Documents followed

The documents below were collected from the [NHISS portal](https://nhiss.nhis.or.kr) in October 2026. Dates are those printed in the documents or their file names, and a document with no printed date is marked as undated.

| Database | Document | 한글 | Version and date | Used for |
|---|---|---|---|---|
| National Sample Cohort | Table layout | 표본코호트DB 레이아웃 | Ver 1.5, May 2026, data for 2002 to 2023 | [Codebook](../variables/nsc/index.md) |
| National Sample Cohort | User manual | 표본코호트DB 사용자매뉴얼 | 1.5, May 2026 | [Dataset page](nsc.md) and codebook notes |
| National Sample Cohort | Summary statistics | 표본코호트DB 통계표 | March 2025 | Not yet used |
| Health Screening Cohort | User manual | 건강검진코호트DB 사용자 매뉴얼 | 2.3, undated | [Dataset page](heals.md) and [codebook](../variables/heals/index.md) |
| Senior Cohort | User manual | 노인코호트DB 매뉴얼 | 1.4, undated[^senior] | [Dataset page](senior.md) and [codebook](../variables/senior/index.md) |
| Low-Risk Sample Dataset | User manual | 저위험 표본데이터셋 매뉴얼 | Undated, data for 2014 to 2023 | [Dataset page](low-risk.md) and [codebook](../variables/lowrisk/index.md) |
| Customized Research DB | Column layouts | 맞춤형 자료 제공 컬럼 레이아웃 and six companion files | September 10, 2026 | [Codebook](../variables/custom/index.md) |
| Customized Research DB | Application form | 맞춤형 자료 요청서 | July 22, 2026 | [Dataset page](customized.md) |
| All databases | Guide to new applications | 사용자매뉴얼1, 연구용DB 신규신청 방법 | 4.0, September 2024 | [Customized Research DB](customized.md) and [Senior Cohort](senior.md) pages |

The six companion layouts of the customized DB cover providers, long-term care, general health screening, cancer screening, the cancer screening questionnaire, and infant and child screening.

## Superseded documents

The documents below were also collected but are older than a document listed above, so the site does not follow them.

| Document | Date | Replaced by |
|---|---|---|
| 표본코호트DB 2.2 레이아웃 | September 2021, data through 2019 | The NSC table layout of May 2026, which covers the same release with data through 2023 despite the version number missing from its file name |
| 맞춤형 자료 제공 컬럼 레이아웃 | August 7, 2024 | The customized DB layout of September 10, 2026 |
| 장기요양 자료 제공 컬럼 레이아웃 | July 31, 2024 | The long-term care layout of September 10, 2026 |

The changes between the 2024 and 2026 layouts of the customized DB are listed on the [Customized Research DB](customized.md#versions-of-the-layouts) page.

## Conflicts between sources

Where NHIS documents disagree, the site states both versions and marks the entry rather than choosing silently. The conflicts found so far are listed below.

- **Cause of death in the Senior Cohort.** The Senior manual lists two cause-of-death variables, while the portal and the 2024 guide to new applications state that the database has none. See the [Senior Cohort](senior.md#known-issues) page.
- **Sampling of the Senior Cohort.** The Senior manual describes stratified sampling in one section and simple random sampling in another. See the [Senior Cohort](senior.md) page.
- **Family history in the National Sample Cohort, 2018 to 2023.** The layout file codes these questions 1 and 2, while the manual text and the customized DB layout code them 0 and 1. The five variables are marked Disputed, as in [`Q_FHX_HTN`](../variables/nsc/g1e/q_fhx_htn.md).
- **Triglycerides in the Low-Risk Sample Dataset.** The manual gives the formula for calculated LDL cholesterol under triglycerides. See the [Low-Risk Sample Dataset](low-risk.md#known-issues) page.
- **Requestable years for the customized DB.** The 2024 guide allows requests through 2023, and the 2026 application form allows requests through 2024. The site follows the 2026 form.

## Corrections in the codebook

The layout files and manuals are written to be read as printed tables, so a few cells do not survive a mechanical import. The importer corrects the cases below, and each affected variable page carries a note that describes the correction.

- **Admission route.** The cohort manuals list the two digits of the admission route separately, and the codebook lists the combined codes 11 to 32 with the labels of the customized DB layout, as in [`HSPTZ_PATH_TYPE`](../variables/nsc/t20/hsptz_path_type.md).
- **Shared description cells.** In the 2018 to 2023 screening layout of the National Sample Cohort, one description cell spans several rows, such as the unit and missing-value rule of six blood tests. The description is applied to every row it spans, as in [`G1E_VA_LT`](../variables/nsc/g1e/g1e_va_lt.md).
- **Year markers.** Notes such as 2018년 or 2019부터 적용 next to a code list are applied to the years of the entry, and a cell that lists two code sets for different years is split into two periods.
- **Codes outside their row.** The codes of the 2002 to 2008 past-history questions in the National Sample Cohort sit in one shared note, and they are attached to each of the nine variables.
- **Codes that do not apply.** The layout repeats yes and no codes for the free-text field [`Q_AWR_DZ`](../variables/nsc/g1e/q_awr_dz.md), and these are omitted.
- **Duplicate codes.** Six variables list one code with two meanings in the same years, as in [`GOE_JDG`](../variables/heals/go2/goe_jdg.md). These are reproduced as printed with a note, since the documents give no way to tell which meaning applies.

The importer does not invent codes the documents leave out. The long-term care assessment items (T02) of the National Sample Cohort and the Senior Cohort, for example, refer to the response categories of the assessment form printed in the manual, and their numeric codes are not documented.

[^senior]: The manual refers to the national statistics agency as 국가데이터처, the name that Statistics Korea took in October 2025, so it was written after that date.
