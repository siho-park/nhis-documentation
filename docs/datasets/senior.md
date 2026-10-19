# Senior Cohort (노인코호트DB)

The Senior Cohort (NHIS-Senior, 노인코호트DB) follows an 8 percent sample of people aged 60 to 80 in 2008 and adds a sample of new 60-year-olds every year. It links eligibility, claims, health screening, provider, and long-term care insurance records, with claims from 2002 to 2023 and long-term care records from 2008 to 2023. The NHIS built it for research on the risk factors and prognosis of diseases of old age, and it offers a much larger sample of older people than the sample cohort.

!!! info "Source"
    This page follows the NHIS user manual for the database (노인코호트DB 사용자 매뉴얼), version 1.4, which describes release 2.0 with data through 2023.

## Sample design

The current release samples older adults enrolled in 2008 and refreshes the sample with each new cohort of 60-year-olds, with the design below.

- **Population (모집단).** People aged 60 to 80 in January 2008 who held health insurance or Medical Aid eligibility throughout that year, a total of 6,399,533 people.
- **Sampling (표본추출).** An 8 percent sample stratified by sex, single year of age, area type, and premium decile.[^strat]
- **Sample (표본).** 511,953 people.
- **Refreshment (신규대상자).** From 2009, an 8 percent sample of the people turning 60 is added every year, between 34,423 and 72,977 people a year.
- **Exclusions (제외).** Foreigners are excluded because they are likely to leave the cohort.

Each member's origin is recorded in `SMPL_GRP_TYPE` (표본형태 구분, sample type), which is 1 for the 2008 sample and 2 for members added from 2009.

### Records before entry

Refreshment members enter the data ten years before the year they were sampled, so the eligibility table contains people in their fifties. The table grows from 664,193 people in 2002 to 1,124,873 in 2023, and only 332,385 of the people in 2023 belong to the 2008 sample. Analyses of older adults therefore need to restrict each year to the relevant ages, rather than use every record in the eligibility table.

The 2008 sample is observed retrospectively from 2002 to 2007 and had to remain enrolled through 2008. Its first deaths therefore appear in 2009, and its records before 2008 exclude people who died before 2008.

## Versions

Release 2.0 is a new sample of a different population, not an extension of release 1.0.

| | Release 1.0 | Release 2.0 |
|---|---|---|
| Provided | December 2015 to September 2021 | September 2021 to present |
| Population | Aged 60 and older in December 2002, about 5.5 million | Aged 60 to 80 in January 2008, about 6.4 million |
| Sample | 558,147, or 10 percent | 511,953, or 8 percent, plus 8 percent of each new cohort of 60-year-olds |
| Sampling | Simple random | Stratified by sex, age, area type, and premium decile |
| Years | 2002-2015, retrospective | 2002-2023, retrospective and prospective |
| Masked diagnoses | 114 codes | 3,116 codes |
| Long-term care | Includes the doctor's opinion form (의사소견서) | Doctor's opinion form discontinued |
| Severe disability | Grades 1 and 2 | Grades 1 to 3 |

## Tables

Claims come as one file per table and year, as in `NHIS_SENIOR_GY20_T1_2010`, while the other tables come as one or a few files.

| Table | 한글 | Files | Unit of observation | Years | Variables |
|---|---|---|---|---|---|
| Eligibility | 자격 DB | `NHIS_SENIOR_JK` | Person and year | 2002-2023 | 13 |
| Claims | 진료 DB | `NHIS_SENIOR_GY20_T1_2002` to `NHIS_SENIOR_GY30_T3_2023` | Claim, line item, diagnosis, or prescribed drug | 2002-2023 | 7 to 25 per table |
| General health screening | 일반건강검진 | `NHIS_SENIOR_GJ` (3 files) | Screening | 2002-2023 | 85 for 2002 to 2017, 123 for 2018 to 2023 |
| Providers | 요양기관 DB | `NHIS_SENIOR_YK` | Provider and year | 2002-2023 | 13 |
| Long-term care | 노인장기요양 DB | `NHIS_SENIOR_T01`, `T02`, `T04`, `T05` | Application, claim, or facility | 2008-2023 | 12 to 81 per table |

### Claims tables

Claims use the same three groups as the [Health Screening Cohort](heals.md#claims-tables), with hemodialysis outpatient claims (form 15) added to the medical group.

| Table | 한글 | Unit of observation | Variables |
|---|---|---|---|
| 20t, claims | 명세서 | Claim | 24 (25 for pharmacy) |
| 30t, treatment details | 진료내역 | Line item on a claim | 16 (20 for dental and Korean medicine) |
| 40t, diagnoses | 상병내역 | Diagnosis on a claim | 7 |
| 60t, prescriptions | 처방전교부상세내역 | Drug on a prescription filled outside the provider | 12 |

### Long-term care tables

The long-term care tables cover every applicant in each year, including people found ineligible and dismissed applications, but excluding duplicates and people who died.

| Table | 한글 | Content | Variables |
|---|---|---|---|
| T01 | 장기요양 신청 및 판정결과 | Applications and assessed care grades | 21 |
| T02 | 인정욕구조사사항 | Needs assessment survey on physical, cognitive, behavioral, nursing, and rehabilitation needs | 81 |
| T04 | 청구명세서 | Long-term care claims | 12 |
| T05 | 장기요양기관 기본현황 | Long-term care facilities | 25 |

## Linkage

The eligibility, claims header, screening, and long-term care tables carry the person identifier, while the claims detail tables reach a person through the claim identifier.

| Variable | 한글 | English | Links |
|---|---|---|---|
| `PERSON_ID` | 개인일련번호 | Person identifier | Eligibility, claims header (20t), screening, and long-term care |
| `KEY_SEQ` | 청구일련번호 | Claim identifier | 20t, 30t, 40t, and 60t of the same claim group |
| `YKIHO_ID` | 요양기관식별대체번호 | Provider identifier | Claims header (20t) and providers |
| `MPRSC_ISSUE_ADMIN_ID` | 처방전발행기관식별대체번호 | Prescribing provider identifier | Pharmacy claims header (T3 20t) to the prescribing provider |
| `PERSON_SEQ` | 장기요양 결합키 | Long-term care application key | T01, T02, and T04[^ltckey] |
| `LTC_YKIHO_ID` | 장기요양기관기호 일련번호 | Long-term care facility identifier | T04 and T05 |

Pharmacy claims link to the prescribing provider's claim in the same way as in the [Health Screening Cohort](heals.md#linkage).

## Known issues

The following features of the database commonly lead to errors, beyond the records before entry described above.

- **Cause of death may not be available.** The manual lists `DTH_CODE1` and `DTH_CODE2` (사망원인1, 사망원인2, cause of death) and describes them as linked from the national statistics agency, but two other NHIS sources say the opposite. The NHISS portal's description of this database states that cause of death is not included. The NHIS guide to new applications (version 4.0, September 2024) likewise states that only the National Sample Cohort and the Health Screening Cohort include it. Applicants who need cause of death should confirm with the NHIS before applying.
- **Medical Aid claims before 2006.** Claims filed under Medical Aid before January 1, 2006 are excluded, while claims for earlier care that were filed after that date are included.
- **Long-term care begins in July 2008.** Long-term care insurance started in July 2008, so the 2008 records cover half a year.
- **Care grades changed in 2014.** The grade system expanded from three grades to five in July 2014, and a cognitive support grade (인지지원등급) was added later. `GJU_RCGT_GRADE_CD` (등급판정인정등급코드, assessed care grade) is therefore not comparable across these changes.
- **Long-term care claims can be split.** A facility can bill one person's care on several claims, so total days and costs of care must be summed by person.
- **Some long-term care claims have no facility.** Claims for visiting-nurse orders under short-term care do not match any facility in T05.
- **Long-term care facilities are not providers.** Long-term care facilities are separate institutions from the medical providers in the provider table, and they are described only in T05.
- **Province only.** Residence is recorded only as `SIDO` (시도코드, province), with 17 provinces.
- **The income decile is a premium decile.** The manual calls `CTRB_PT_TYPE_CD` an income decile (소득분위), but it is the same premium decile used in the other cohorts, computed for households and running from 0 for Medical Aid to 10.
- **Sensitive diagnoses are masked.** Diagnosis codes on the list of 3,116 sensitive codes show only their first letter and an underscore.
- **Claims are cut off at a submission date.** Claims for care in 2023 include those submitted through April 2025, so any later submissions are missing.
- **Bundled and per diem payment hides detail.** Claims paid by diagnosis-related group (포괄수가제) or at per diem rates, as in long-term care hospitals, report little detail on individual services and drugs.
- **Variable names differ from the sample cohort.** The database uses the same naming convention as the Health Screening Cohort. The [crosswalk](index.md#variable-name-crosswalk) maps the main variables.

[^strat]: The manual is inconsistent on this point. Its comparison of releases and the NHISS portal describe stratified sampling, while its sample design section describes simple random sampling.

[^ltckey]: The manual's table of join keys names this key `LTC_MGNNU_SEQ_NO` (장기요양신청_일련번호), while its code examples and notes use `PERSON_SEQ`.
