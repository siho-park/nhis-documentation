# Low-Risk Sample Dataset (저위험 표본데이터셋)

The Low-Risk Sample Dataset (저위험 표본데이터셋) is a heavily aggregated sample built to widen access to NHIS data for private-sector research and development. It follows 1,000,000 randomly sampled people who used medical care between 2014 and 2023, with one record per person, year, and main diagnosis group, together with their health screening results. The NHISS portal lists it as the low-risk sample cohort (저위험 표본코호트DB) in its menu for applying for sample research databases (표본연구DB신청). The portal's pages describing each database do not yet include it, and it is absent from the NHIS guide to new applications of September 2024.

??? info "Source"
    This page follows the NHIS user manual for the dataset (저위험 표본데이터셋 사용자 매뉴얼), which is undated and covers data through 2023.

## Sample design

The sample is drawn from people who used medical care in the ten-year window, with the design below.

- **Population (모집단).** Everyone with at least one medical claim (의과 요양급여청구명세서) between 2014 and 2023, each counted once.
- **Sample (표본).** 1,000,000 people drawn at random, with `RN_INDI` (개인일련번호, person identifier) assigned at random from 1 to 1,000,000.
- **Years (기간).** Care from 2014 to 2023 and deaths from 2014 to 2024.

Because the sample is drawn from people who used care, people with no medical claims in the ten years are absent, which matters for any estimate of prevalence or utilization rates in the population. The manual reports that the sample resembles the population in its sex ratio, regional distribution, and mean age.

## Tables

The dataset has two tables, plus two lookup files for diagnosis names (`SMPL_MC_SICK_NM`) and the list of masked diagnoses (`SMPL_MC_SICK_MSK`).

| Table | 한글 | Unit of observation | Records | People | Variables |
|---|---|---|---:|---:|---:|
| `SMPL_MC` | 의료이용, medical use | Person, year, and main diagnosis group | 42,814,155[^rows] | 1,000,000 | 12 |
| `SMPL_HC` | 건강검진, health screening | Person and screening year | 2,773,017 | 678,120 | 25 |

The medical use table has the following variables.

| Variable | 한글 | English | Notes |
|---|---|---|---|
| `RN_INDI` | 개인일련번호 | Person identifier | 1 to 1,000,000 |
| `GENDER` | 성별 | Sex | 1 male, 2 female |
| `BTH_YYYY` | 출생연도 | Birth year | 1929LE for people born in 1929 or earlier |
| `DTH_YYYY` | 사망연도 | Year of death | 2014 to 2024 |
| `MDCARE_YYYY` | 수진연도 | Year of care | 2014 to 2023 |
| `SICK_SYM` | 주상병 | Main diagnosis group | KCD block, chapter, or three-character code |
| `SICK_SYM_NM` | 주상병 설명 | Name of the main diagnosis group | Provided in `SMPL_MC_SICK_NM` |
| `SIDO` | 거주지(시도) | Province of residence | 17 provinces |
| `INSUR_TYPE` | 건강보험자격 | Insurance type | 1 self-employed, 2 employee, 3 Medical Aid |
| `CTRB_VTILE` | 건강보험료 5분위 | Premium quintile | |
| `DD_ADM` | 입원일수 | Inpatient days | Annual total for the diagnosis group |
| `DD_OPD` | 외래내원일수 | Outpatient visit days | Annual total for the diagnosis group |

The screening table holds 23 measurements and questionnaire items, including height, weight, waist circumference, blood pressure, blood and urine tests, estimated kidney function, smoking, drinking, and physical activity.

## Known issues

The dataset trades detail for ease of access, and the following features limit what it can answer.

- **Diagnoses are coarse.** Only the main diagnosis is recorded, at the level of a KCD block (중분류) or, for sensitive diagnoses, a KCD chapter (대분류). Eight major cancers are kept at a finer level, namely stomach (C16), colorectal (C18-C20), liver (C22), gallbladder and biliary (C23-C24), pancreas (C25), lung (C33-C34), kidney (C64), and thyroid (C73), while breast and cervical cancer appear only at the chapter level because they are sensitive.
- **Only medical claims are included.** Dental, Korean medicine, and pharmacy claims are excluded, and the data contain no costs, dates of care, procedures, drugs, or providers.
- **Days are annual totals.** Inpatient and outpatient days are summed by year and diagnosis group and capped at the number of days in the year, so individual visits and admissions cannot be identified.
- **Screening values are rounded and top-coded.** Height, weight, and waist circumference are top-coded at 190 cm, 126 kg, and 121 cm, and several measurements are rounded to whole numbers.
- **Questionnaire items are harmonized.** Responses were recoded to be comparable across screening reforms, with drinking frequency per month converted to a weekly rate. Walking days exist only through 2017, and muscle-strengthening days only from 2018.
- **Birth year is top-coded.** `BTH_YYYY` (출생연도, birth year) is recorded as 1929LE for people aged 85 or older in 2014.
- **Triglyceride entry in the manual.** The manual's description of `G1E_TG` (트리글리세라이드, triglycerides) gives the formula for calculated LDL cholesterol, which appears to belong to `G1E_LDL` (LDL-콜레스테롤, LDL cholesterol).

[^rows]: The manual's text gives 45,814,155 medical use records, but its table gives 42,814,155, and only the second figure is consistent with its reported total of 45,587,172 records across both tables.
