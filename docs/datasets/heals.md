# Health Screening Cohort (건강검진코호트DB)

The National Health Screening Cohort (NHIS-HEALS, 건강검진코호트DB) follows about 515,000 people who received a general health screening in 2002 or 2003 at ages 40 to 79. It links their eligibility, claims, health screening, and provider records from 2002 to 2023, and its screening data are richer than those of the sample cohort, with separate tables for the life-transition and oral screenings. Because members were selected on attending a screening and the cohort is never refreshed, it describes a screened and aging population rather than the general population.

??? info "Source"
    This page follows the NHIS user manual for the database (건강검진코호트DB 사용자 매뉴얼), version 2.3, which describes data through 2023.

## Sample design

The cohort is a simple random sample of adults who attended a general health screening at the start of the 2000s, with the design below.

- **Population (모집단).** About 5.15 million people aged 40 to 79 at the end of December 2002 who held health insurance and received a general health screening in 2002 or 2003, each counted once.
- **Sampling (표본추출).** A 10 percent simple random sample.
- **Sample (표본).** 514,866 people.
- **Exclusions (제외).** Foreigners are excluded because they are likely to leave the cohort. Medical Aid beneficiaries are excluded at baseline because they were not eligible for the general screening in 2002, although members who later move to Medical Aid stay in the cohort.

The lower age bound of 40 follows the screening rules of the time. Below age 40, only heads of self-employed households and employee insured were eligible for screening, so a younger sample would not have represented its age group.

The cohort is closed, so it ages and shrinks over time. Membership falls from 514,866 in 2002 to 414,724 in 2023 through death and loss of eligibility, and every member is 61 or older by 2023.

## Versions

The manual describes the current data through 2023 but does not record earlier releases. The files are split into the periods 2002 to 2015, 2016 to 2019, and 2020 to 2023, and several variables differ in the files from 2016 onward, as listed under known issues.

## Tables

The database has 46 files in seven groups of tables.

| Table | 한글 | Files | Unit of observation | Years | Variables |
|---|---|---|---|---|---|
| Eligibility | 자격 DB | `NHIS_HEALS_JK` (3 files) | Person and year | 2002-2023 | 12 |
| Claims | 진료 DB | `NHIS_HEALS_GY20` to `NHIS_HEALS_GY60` (30 files) | Claim, line item, diagnosis, or prescribed drug | 2002-2023 | 6 to 21 per table |
| General health screening | 일반건강검진 | `NHIS_HEALS_GJ` (4 files) | Screening | 2002-2023 | Varies by period |
| Life-transition screening | 생애전환기 건강진단 | `NHIS_HEALS_LJ` (2 files) | Screening | 2007-2017 | 69 |
| Oral screening | 구강검진 | `NHIS_HEALS_GO` (3 files) | Screening | 2002-2023 | Varies by period |
| Oral life-transition screening | 구강검진 (생애) | `NHIS_HEALS_LO` | Screening | 2007-2015 | Varies by period |
| Providers | 요양기관 DB | `NHIS_HEALS_YK` (3 files) | Provider and year | 2002-2023 | 10 |

Unlike the sample cohort, the eligibility table records `AGE` (연령, age) as age in completed years at the end of each year, and death as an exact date in `DTH_MDY` (사망일자, date of death).

### Claims tables

Claims are split by claim form into three groups, which differ from the four groups of the sample cohort. File names combine the table, the period, and the group, as in `NHIS_HEALS_GY20_0215_T1`.

| Group | 한글 | Claim form codes, `FORM_CD` (서식코드, claim form) | Tables |
|---|---|---|---|
| T1, medical and public health | 의과·보건기관 | 02 and 03 medical inpatient and outpatient, 07 and 08 public health inpatient and outpatient, 09 psychiatric day ward, 10 and 11 psychiatric inpatient and outpatient | 20t, 30t, 40t, 60t |
| T2, dental and Korean medicine | 치과·한방 | 04 and 05 dental inpatient and outpatient, 12 and 13 Korean medicine inpatient and outpatient | 20t, 30t, 40t, 60t |
| T3, pharmacy | 약국 | 20 dispensing without prescription (약국 조제), 21 dispensing by prescription (처방 조제) | 20t, 30t |

| Table | 한글 | Unit of observation | Variables |
|---|---|---|---|
| 20t, claims | 명세서 | Claim | 20 (21 for pharmacy) |
| 30t, treatment details | 진료내역 | Line item on a claim | 14 (18 for dental and Korean medicine) |
| 40t, diagnoses | 상병내역 | Diagnosis on a claim | 6 |
| 60t, prescriptions | 처방전교부상세내역 | Drug on a prescription filled outside the provider | 11 |

### Screening tables

General screening covers 2002 to 2023, and from 2018 it absorbs the life-transition screening (생애전환기 건강진단) given at ages 40 and 66, which has its own table for 2007 to 2017. Oral screening has a general table and a life-transition table through 2015, and a combined table from 2014.

## Linkage

Only the eligibility, claims header, and screening tables carry the person identifier, so the claims detail tables reach a person through the claim identifier.

| Variable | 한글 | English | Links |
|---|---|---|---|
| `PERSON_ID` | 개인일련번호 | Person identifier | Eligibility, claims header (20t), and screening |
| `KEY_SEQ` | 청구일련번호 | Claim identifier | 20t, 30t, 40t, and 60t of the same claim group |
| `YKIHO_ID` | 요양기관식별대체번호 | Provider identifier | Claims header (20t) and providers |
| `MPRSC_ISSUE_ADMIN_ID` | 처방전발행기관식별대체번호 | Prescribing provider identifier | Pharmacy claims header (T3 20t) to the prescribing provider |

Pharmacy claims can be linked to the claim of the provider that wrote the prescription. The manual matches `PERSON_ID` (개인일련번호, person identifier), `MPRSC_ISSUE_ADMIN_ID` (처방전발행기관식별대체번호, prescribing provider identifier) against `YKIHO_ID` (요양기관식별대체번호, provider identifier), and `TOT_PRES_DD_CNT` (총처방일수, total days prescribed). Drugs dispensed without a prescription have no prescribing provider to match.

## Known issues

The following features of the database commonly lead to errors.

- **Selection on screening.** Members attended a screening in 2002 or 2003, so they differ from adults who do not attend, and estimates do not generalize to all adults aged 40 to 79 without adjustment.
- **Closed cohort.** No members are added, so later years describe an older population only, and the youngest members are 61 by 2023.
- **Medical Aid claims before 2006.** Claims filed under Medical Aid before January 1, 2006 are excluded, while claims for earlier care that were filed after that date are included.
- **Province only.** Residence is recorded only as `SIDO` (시도코드, province), with 17 provinces, so district-level analysis is not possible.
- **Premium deciles are household measures.** `CTRB_PT_TYPE_CD` (보험료분위, premium decile) runs from 0 for Medical Aid to 10, and every member of a household shares the decile of the household. A missing category appears only from 2016.
- **Variables change in the files from 2016.** `GNL_NM_CD` (일반명코드, generic name code) is dropped and `DIV_CD` (분류코드, item code) takes its place. The severe category of `DFAB_GRD_CD` (장애중증도코드, disability severity) widens from grades 1 and 2 to grades 1 to 3, and notifiable infectious diseases (법정감염병) become masked.
- **Sensitive diagnoses are masked, with exceptions.** Diagnosis codes on the list of 3,116 sensitive codes show only their first letter and an underscore. Codes needed to interpret screening results stay unmasked, namely acute hepatitis (B16, B17), dementia (F00-F03), and depressive and mood disorders (F32-F34, F38, F39).
- **Screening layouts change in 2009 and 2018.** The 2009 and 2018 reforms changed the tests, the questionnaire, and the variable names, so multi-year analyses need to check that each variable measures the same thing over time.
- **Screenings are not annual.** Members can skip a screening in an eligible year or attend in another year, so the screening tables do not form a balanced annual panel.
- **Implausible screening values are already missing.** Test results outside the manual's plausibility ranges were set to missing before release.
- **Medical Aid screenings before 2012.** The NHIS screened Medical Aid beneficiaries only from 2012, but people listed for screening before they moved to Medical Aid can still appear in earlier years.
- **Missing causes of death.** Some deaths have no cause because the death record did not link to the national cause-of-death data, for example after a correction to the resident registration number.
- **Providers appear only in years with claims.** The provider table includes a provider only in years when a cohort member used it.
- **Bundled and per diem payment hides detail.** Claims paid by diagnosis-related group (포괄수가제) or at per diem rates, as in long-term care hospitals, report little detail on individual services and drugs.
- **Variable names differ from the sample cohort.** The database uses an older naming convention, so code written for the sample cohort does not run without renaming. The [crosswalk](index.md#variable-name-crosswalk) maps the main variables.
