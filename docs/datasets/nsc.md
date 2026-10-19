# National Sample Cohort (표본코호트DB)

The National Sample Cohort (NHIS-NSC, 표본코호트DB) follows a 2 percent sample of the Korean population from 2002 to 2023. It links eligibility, premium, claims, health screening, death, provider, and long-term care records for about one million people drawn from the 2006 population. The sample covers all ages and includes Medical Aid beneficiaries, which makes it the standard NHIS database for population-level research, and the NHIS reports that it supports more than 300 projects every year.

!!! info "Source"
    This page follows the NHIS user manual for the database (표본코호트DB 사용자 매뉴얼), version 1.5 of May 2026, which describes release 2.2 with data through 2023.

## Sample design

The current release samples people enrolled throughout 2006, a change from the 2002 population used by the first release. The NHIS moved the base year because it began processing Medical Aid claims in 2006, so a 2006 sample has complete claims for every member from that year forward.

The main sample is a stratified draw from the 2006 population, with the design below.

- **Population (모집단).** Korean nationals with health insurance or Medical Aid eligibility for all of 2006, a total of 48,222,537 people.
- **Strata (층화).** The 2,142 strata cross sex, 17 age groups, 3 area types, and 21 insurance and premium groups. Age groups are five-year bands from age 1 to 79 plus a group for 80 and older. Area types are large cities (대도시), small and medium cities (중소도시), and rural areas (농어촌), and the insurance and premium groups are Medical Aid plus ten premium deciles each for self-employed and employee insured.
- **Sample (표본).** 1,000,000 people, or 2.1 percent of the population.

### Supplementary samples

Two kinds of supplementary samples are added to the main sample, and every member's sample type is recorded in `SMPL_TYPE_CD` (표본구분, sample type). The person identifier `RN_INDI` (개인고유번호, person identifier) encodes the same information through its range.

| Sample | 한글 | `SMPL_TYPE_CD` | `RN_INDI` range | Members in 2006 | Members in 2023 |
|---|---|---|---|---:|---:|
| Main sample | 2006년 전국민 표본 | 1 | 1 to 1,000,000 | 1,000,000 | 902,203 |
| Missing-premium supplement | 2006년 정상적 보험료 결측군 추가표본 | 2 | 1,000,001 to 2,000,000 | 11,638 | 10,635 |
| Newborn supplement | 신생아 추가 표본 | 3 | 2,000,001 to 3,000,000 | 9,355 | 157,531 |
| Newborn missing-premium supplement | 신생아 정상적 보험료 결측군 추가표본 | 4 | 3,000,001 to 4,000,000 | 215 | 5,212 |
| Total | 합계 | | | 1,021,208 | 1,075,581 |

The missing-premium supplement covers people whose premium is legitimately missing in the administrative records. Examples include career soldiers and members of the longshore workers' union, whose premiums are not levied on individuals, and workers on long-term leave, whose premiums are billed afterward.

The newborn supplements add a sample of each birth cohort from 2006 onward, drawn with the same design as the main sample.[^newborn] Without them, the main sample is a closed cohort that ages every year and shrinks from 1,000,000 members in 2006 to 902,203 in 2023. Studies that need a representative cross-section of a later year therefore need the newborn supplements, while studies that follow the 2006 population need the main and missing-premium samples.

### Retrospective years

The years 2002 to 2005 are observed retrospectively for people enrolled throughout 2006, and they differ from later years in three ways.

- **No deaths.** Every member survived to 2006, so the data contain no deaths from 2002 to 2005. The main sample also has no deaths in 2006, and the 7 deaths recorded that year are all newborns.
- **Survivor selection.** People who died or emigrated before 2006 are absent, so the 2002 to 2005 data are not a sample of the population alive in those years.
- **No Medical Aid claims.** Claims of Medical Aid beneficiaries are missing for 2002 to 2005, because the NHIS began processing them only in 2006.

## Versions

The database was rebuilt on a new sample in 2017 and has been extended several times since then. Code written for release 1.0 needs revision for later releases, because the rebuild changed the tables, the identifiers, and the age variable.

| Release | Date | Years | Base population | Main changes |
|---|---|---|---|---|
| 1.0 | July 2014 | 2002-2013[^v1] | 2002 | First release |
| 2.0 | June 2017 | 2002-2015 | 2006 | New sample, birth year instead of age group, separate birth and death table, person identifier on every claims table, stronger de-identification, analysis on a remote server |
| 2.1 | April 2021 | 2002-2019 | 2006 | Years 2016 to 2019 added, disability severity regrouped |
| 2.2 | September 2021 | 2002-2019 | 2006 | Long-term care tables added |
| 2.2 update | January 2026 | 2002-2023 | 2006 | Years 2020 to 2023 added, with equivalized premium quintiles and household income and property percentiles |
| 2.2 update | May 2026 | 2002-2023 | 2006 | Cause of death linked from the national statistics agency (국가데이터처, formerly Statistics Korea) |

## Tables

Release 2.2 has six groups of tables, delivered as 56 files that total 546.2 GB.

| Table | 한글 | Files | Unit of observation | Years | Variables |
|---|---|---|---|---|---|
| Eligibility and premium | 자격 및 보험료 테이블 | `NSC2_BNC` (3 files) | Person and year | 2002-2023 | 16 |
| Birth and death | 출생 및 사망 테이블 | `NSC2_BND` | Person | 2002-2023 | 5 |
| Claims | 진료 테이블 | 40 files, listed below | Claim, line item, diagnosis, or prescribed drug | 2002-2023 | 8 to 22 per table |
| Health screening | 건강검진 테이블 | `NSC2_G1E` (5 files) | Screening | 2002-2023 | 51, 57, or 113 by period |
| Providers | 요양기관 테이블 | `NSC2_INST` (3 files) | Provider and year | 2002-2023 | 10 |
| Long-term care | 노인장기요양 테이블 | `NSC2_T01`, `NSC2_T02`, `NSC2_T04`, `NSC2_T05` | Application, claim, or facility | 2008-2023 | 12 to 81 per table |

### Claims tables

Claims are split by claim form into four groups, and each group has up to four tables, for 13 claims tables in all. The file name combines the group letter, the table number, and the period, as in `NSC2_M20_0215` for medical claims from 2002 to 2015.

| Group | 한글 | Claim form codes, `FORM_CD` (서식코드, claim form) | Tables |
|---|---|---|---|
| Medical and public health (M) | 의과·보건기관 | 02 and 03 medical inpatient and outpatient, 07 and 08 public health inpatient and outpatient, 09 psychiatric day ward, 10 and 11 psychiatric inpatient and outpatient, 15 hemodialysis outpatient | T20, T30, T40, T60 |
| Dental (D) | 치과 | 04 and 05 dental inpatient and outpatient | T20, T30, T40, T60 |
| Korean medicine (K) | 한방 | 12 and 13 Korean medicine inpatient and outpatient | T20, T30, T40 |
| Pharmacy (P) | 약국 | 20 dispensing without prescription (약국 조제), 21 dispensing by prescription (처방 조제) | T20, T30 |

| Table | 한글 | Unit of observation | Variables |
|---|---|---|---|
| T20, claims | 명세서 | Claim | 22 |
| T30, treatment details | 진료내역 | Line item on a claim, such as a procedure, drug, or material | 17 |
| T40, diagnoses | 상병내역 | Diagnosis on a claim | 8 |
| T60, prescriptions | 처방전교부상세내역 | Drug on a prescription filled outside the provider | 13 |

### Long-term care tables

The long-term care tables cover applicants for long-term care insurance (노인장기요양보험) from its introduction in July 2008, so the 2008 data are incomplete.

| Table | 한글 | Content | Variables |
|---|---|---|---|
| T01 | 장기요양 신청 및 판정결과 | Applications and assessed care grades | 19 |
| T02 | 인정조사사항 | Items of the needs assessment survey | 81 |
| T04 | 청구명세서 | Long-term care claims | 12 |
| T05 | 장기요양기관 현황 | Long-term care facilities | 25 |

## Linkage

Every table except the two provider tables, INST and T05, carries the person identifier, so most merges use `RN_INDI` (개인고유번호, person identifier) together with a year. The identifiers below replace the original administrative numbers.

| Variable | 한글 | English | Format | Links |
|---|---|---|---|---|
| `RN_INDI` | 개인고유번호 | Person identifier | 7 digits | All tables except providers |
| `RN_KEY` | 청구고유번호 | Claim identifier | 14 digits, the claim year and month followed by an 8-digit serial number | T20, T30, T40, and T60 of the same claim group |
| `RN_INST` | 요양기관고유번호 | Provider identifier | 6 digits | T20 and the provider table |
| `RN_INDI_SEQ` | 장기요양신청 일련번호 | Long-term care application identifier | 10 digits, `RN_INDI` followed by a 3-digit application number | T01, T02, and T04 |
| `LTC_INST_ID` | 장기요양기관고유번호 | Long-term care facility identifier | The letter L followed by 6 digits | T04 and T05 |

## Known issues

The following features of the database commonly lead to errors, beyond the retrospective years described above.

- **Sensitive diagnoses are masked.** Diagnosis codes in T20 and T40 that belong to a list of 3,116 sensitive codes show only their first letter and an underscore, so A15 appears as A_. The list combines special diagnoses (공단 특수상병) and notifiable infectious diseases (법정감염병), including all mental and behavioral disorders (F00-F99), pregnancy and childbirth (O00-O99), congenital anomalies (Q00-Q99), and cancers of the breast and genital organs (C50-C63). Research on these conditions requires a [customized research DB](customized.md).
- **Sensitive procedures are masked.** Fee codes in T30 for genitourinary, breast, and obstetric procedures, including cesarean sections and abortions, are masked in the same way.
- **Excluded diagnoses are dropped.** T40 omits diagnoses that the provider marked as excluded once the final diagnosis was confirmed (배제상병), so `SICK_CLSF_TYPE` (상병분류구분코드, diagnosis type) takes only the values 1 for primary and 2 for secondary. The variable is populated only from 2004.
- **Claim counts change around 2011.** Outpatient billing moved from one claim per month to one claim per visit day, a change extended to hospitals in 2011, so the number of claims changes even where the number of visits does not.
- **Premium deciles shift after the 2018 and 2022 reforms.** Premium reforms in July 2018 and September 2022 expanded the group paying the minimum premium, which bunches self-employed insured into the lowest decile. In the manual's tables, the first self-employed decile grows from 15,757 members in 2018 to 58,379 in 2019, and by 2023 the second to fourth self-employed deciles are empty.
- **Premium deciles are relative to insurance type and household.** `CTRB_Q10` (보험료 10분위, premium decile) is computed separately for employee and self-employed insured, and every person on the same insurance card shares the decile of the household.
- **Premiums lag income.** `CTRB_Q10` for 2023 reflects 2022 income and property, while `INC_FML_EQ100` (균등화가구소득 100분위, equivalized household income percentile) for 2023 reflects 2023 income. The premium decile is also measured at the start of the year, and the household percentiles at the end.
- **Property percentiles are mostly missing before 2006.** Values of `PRP_FML_EQ100` (균등화가구재산 100분위, equivalized household property percentile) are largely missing for reference years 2005 and earlier, because the 2006 tax reform redefined property tax items.
- **District codes are harmonized within years and partly merged.** `SGG` (시군구, district) is converted to the code valid on January 1 of each year, and invalid codes are replaced with the nearest valid code, so codes still differ across years when boundaries change. Four small counties are merged into neighbors, namely Ongjin into Ganghwa, Yanggu into Hwacheon, Yeongyang into Cheongsong, and Ulleung into Uljin.
- **Birth year is top-coded.** `BTH_YYYY` (출생연도, birth year) is recorded as 1921LE for people born in 1921 or earlier, so the variable is stored as text and age is censored at 85 in 2006.
- **Disability severity was regrouped.** `DSB_SVRT_CD` (장애중증도구분, disability severity) counts grades 1 to 3 as severe from release 2.1, compared with grades 1 and 2 in release 2.0.
- **Life-transition screenings are not included.** The screening table holds general health screenings only. People aged 40 and 66 were screened under the separate life-transition program (생애전환기 건강진단) from 2007 to 2017, so their screenings at those ages are missing for those years.
- **Screening content changes in 2009 and 2018.** The screening table has 51 variables for 2002 to 2008, 57 for 2009 to 2017, and 113 for 2018 to 2023, and questionnaire items and response categories changed with each reform. Fasting glucose replaced pre-meal glucose in 2010, and Medical Aid beneficiaries appear in the screening data only from 2012.
- **Drugs are identified by ingredient, not product.** Product codes were removed in release 2.0, so drugs are identified by `GNL_NM_CD` (일반명코드, generic name code) and `EFMDC_CLSF_NO` (약효분류번호, efficacy classification number).
- **Per diem payment hides detail.** Long-term care hospitals (요양병원) and public health centers paid at per diem rates report little detail on individual services and drugs.
- **Rare conditions have few cases.** Because the sample has about one million members, the NHIS advises applicants to check case counts before proposing a study of a rare condition.

[^newborn]: The manual's text says newborn sampling began in 2007, but its tables include 9,597 newborns born in 2006. Its count of newborns by birth year also sums to 147,548, fewer than the 162,743 newborn-supplement members it reports for 2023, and the manual does not explain either difference.

[^v1]: Years for release 1.0 are from Lee et al. (2017). The current manual does not document release 1.0.
