# Datasets

The NHIS offers several research databases that differ in population, sampling, and variable names. Each has its own page with the same sections, namely sample design, versions, tables, linkage, and known issues.

1. Sample Database

    - [National Sample Cohort](nsc.md) (표본코호트DB)
    - [Health Screening Cohort](heals.md) (건강검진코호트DB)
    - [Senior Cohort](senior.md) (노인코호트DB)
    - [Low-Risk Sample Dataset](low-risk.md) (저위험 표본데이터셋)

2. Customized Database
    - [Customized Research DB](customized.md) (맞춤형연구DB)

The documents each page follows, and the conflicts found between them, are listed on the [sources and versions](sources.md) page. The NHISS portal also lists an educational sample research DB (교육용 표본연구DB), which is not documented here.

## Comparison

The table compares the four ready-made samples on the features that most often decide which one fits a study.

| | National Sample Cohort | Health Screening Cohort | Senior Cohort | Low-Risk Sample Dataset |
|---|---|---|---|---|
| 한글 | 표본코호트DB | 건강검진코호트DB | 노인코호트DB | 저위험 표본데이터셋 |
| Current release | 2.2 | Manual version 2.3 | 2.0 | Single release |
| Population | Enrolled throughout 2006, all ages | Aged 40 to 79 and screened in 2002 or 2003 | Aged 60 to 80 and enrolled in 2008 | Used medical care in 2014 to 2023 |
| Sample | 1,000,000, about 2 percent | 514,866, 10 percent | 511,953, 8 percent | 1,000,000 |
| Sampling | Stratified | Simple random | Stratified | Random |
| Refreshment | Newborns every year | None | 60-year-olds every year | None |
| Years | 2002-2023 | 2002-2023 | 2002-2023 | 2014-2023 |
| Age | Birth year | Age in years | Age in years | Birth year |
| Residence | District (시군구) | Province (시도) | Province (시도) | Province (시도) |
| Claims | Full claims | Full claims | Full claims | Annual days by diagnosis group |
| Health screening | General | General, life-transition, and oral | General | Selected results |
| Long-term care | 2008-2023 | No | 2008-2023 | No |
| Person identifier | `RN_INDI` | `PERSON_ID` | `PERSON_ID` | `RN_INDI` |

## Variable name crosswalk

The National Sample Cohort renamed most variables when it was rebuilt in 2017, while the Health Screening and Senior cohorts kept the older names. The crosswalk maps the main variables, using the Korean labels of the manuals.

| Concept | 한글 | National Sample Cohort | Health Screening Cohort | Senior Cohort |
|---|---|---|---|---|
| Reference year | 기준년도 | `STD_YYYY` | `STND_Y` | `STND_Y` |
| Person identifier | 개인고유번호, 개인일련번호 | `RN_INDI` | `PERSON_ID` | `PERSON_ID` |
| Claim identifier | 청구고유번호, 청구일련번호 | `RN_KEY` | `KEY_SEQ` | `KEY_SEQ` |
| Provider identifier | 요양기관고유번호, 요양기관식별대체번호 | `RN_INST` | `YKIHO_ID` | `YKIHO_ID` |
| Age | 출생연도, 연령 | `BTH_YYYY` (birth year) | `AGE` | `AGE` |
| Date of death | 사망연월, 사망일자 | `DTH_YYYYMM` (year and month) | `DTH_MDY` | `DTH_MDY` |
| Cause of death | 사망원인 | `COD1`, `COD2` | `DTH_CODE1`, `DTH_CODE2` | `DTH_CODE1`, `DTH_CODE2` |
| Residence | 시군구, 시도코드 | `SGG` (district) | `SIDO` (province) | `SIDO` (province) |
| Insurance type | 가입자격 구분, 가입자구분 | `GAIBJA_TYPE` | `IPSN_TYPE_CD` | `IPSN_TYPE_CD` |
| Premium decile | 보험료 10분위, 보험료분위 | `CTRB_Q10` | `CTRB_PT_TYPE_CD` | `CTRB_PT_TYPE_CD` |
| Disability severity | 장애중증도 | `DSB_SVRT_CD` | `DFAB_GRD_CD` | `DFAB_GRD_CD` |
| Disability type | 장애유형 | `DSB_TYPE_CD` | `DFAB_PTN_CD` | `DFAB_PTN_CD` |
| Start date of care | 요양개시일자 | `MDCARE_STRT_DT` | `RECU_FR_DT` | `RECU_FR_DT` |
| Medical specialty | 진료과목코드 | `MCARE_SUBJ_CD` | `DSBJT_CD` | `DSBJT_CD` |
| Primary diagnosis | 주상병 | `SICK_SYM1` | `MAIN_SICK` | `MAIN_SICK` |
| Secondary diagnosis | 부상병 | `SICK_SYM2` | `SUB_SICK` | `SUB_SICK` |
| Diagnosis code in the diagnosis table | 상병기호 | `MCEX_SICK_SYM` | `SICK_SYM` | `SICK_SYM` |
| Diagnosis type in the diagnosis table | 상병분류구분 | `SICK_CLSF_TYPE` | `SICK_DIV_TYPE_CD` | `SICK_DIV_TYPE_CD` |
| Days of care | 요양일수 | `MDCARE_DD_CNT` | `RECN` | `RECN` |
| Days of visits or inpatient days | 입내원일수 | `VSHSP_DD_CNT` | `VSCN` | `VSCN` |
| Total covered cost after review | 심결요양급여비용총액 | `ED_RC_TOT_AMT` | `EDEC_TRAMT` | `EDEC_TRAMT` |
| Patient cost sharing after review | 심결본인부담금 | `EDC_SBA` | `EDEC_SBRDN_AMT` | `EDEC_SBRDN_AMT` |
| Insurer payment after review | 심결보험자부담금 | `EDC_INSUR_BRDN_AMT` | `EDEC_JBRDN_AMT` | `EDEC_JBRDN_AMT` |

A shared concept does not guarantee a shared coding. For example, `SGG` and `SIDO` differ in geographic detail, and the disability and premium variables were regrouped at different times in different databases.

## Page template

A new dataset page should use the following sections, leaving out a section when the information is not yet known.

- **Overview.** What population the database covers and what it is typically used for.
- **Sample design.** How the sample was drawn, including the base year, strata, and sampling fraction.
- **Versions.** Each release, its years of coverage, and what changed between releases.
- **Tables.** The tables in the database, with Korean and English names and their unit of observation.
- **Linkage.** How tables link to one another, with the Korean and English names of each identifier.
- **Known issues.** Pitfalls specific to this database.
