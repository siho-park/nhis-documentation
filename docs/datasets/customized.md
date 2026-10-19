# Customized Research DB (맞춤형연구DB)

A customized research DB (맞춤형연구DB) is extracted from the full National Health Information Database (국민건강정보DB) for one approved study. It can include everyone who meets the study criteria rather than a sample, within limits set by the NHIS, which makes it the route for rare conditions, small areas, and sensitive diagnoses that the cohort databases mask.

!!! info "Sources"
    This page follows the customized DB application form (맞춤형 자료 요청서) of 2026, the column layouts of the customized DB dated September 10, 2026, the NHIS guide to new applications (사용자매뉴얼1, 연구용DB 신규신청 방법, version 4.0, September 2024), and the [NHISS portal](https://nhiss.nhis.or.kr). Every table and variable is documented in the [codebook](../variables/custom/index.md).

## Building the extract

The applicant first defines the study population and then chooses the tables and variables to extract. The portal divides the application into six steps.

| Step | 한글 | Content |
|---|---|---|
| 1 | 연구신청 | Research application |
| 2 | 구축방식선택 | Choice of how the extract is built |
| 3 | 분석주제설정 | Research topic |
| 4 | 대상자조건설정 | Conditions that define the study population |
| 5 | 추출변수설정 | Tables and variables to extract |
| 6 | 최종확인 | Final confirmation |

The extract can be built in three ways (자료추출방식), and the choice determines who turns the request into code.

- **Standard extraction (기본추출).** NHIS staff build the extract from an Excel request form that the applicant downloads, fills in, and uploads.
- **Automated extraction (자동화추출).** The applicant sets the conditions and variables on the portal, and the extract is built exactly as set there.
- **Researcher extraction (연구자추출).** The researcher visits NHIS headquarters and builds the extract in person, after uploading the same Excel form and marking the project title with [연구자추출].

Whichever way is chosen, the definition of the study population in the research summary (연구과제요약서) must match the one on the portal or in the request form, and the requested years and tables must also match.

## Defining the study population

The request form defines the population by inclusion conditions and up to two exclusion conditions, and each condition combines the items below.

| Item | 한글 | Example in the form |
|---|---|---|
| Years | 연도 | 2009 |
| Diagnosis codes | 상병코드 | `C22`, including its subcodes |
| Diagnosis position | 주상병 / 부상병 | Primary only, primary and the first secondary, or primary and all secondary diagnoses |
| Special co-payment codes | 산정특례 특정기호구분 | `V193`, `V194` |
| Type of care | 의과 / 한방 / 치과 / 약국 | Medical care only |
| Setting | 입원 / 외래 | Inpatient only |
| Fee codes | 행위수가코드 | `Q7221`, following the fee codes of the Health Insurance Review and Assessment Service |
| Drug ingredient codes | 약제주성분코드 | `130801ASY` |

The form also allows a separate definition of cases and controls, with the example of a control group five times the size of the case group drawn from the general population. Lists of more than 50 codes go on a separate sheet, and the NHIS may revise a population that exceeds 10 million people or an extract that is too large.

The claims of the population can be extracted in two ways, and the form asks for exactly one of them.

- **Matching claims only.** Only the claims that meet the conditions, such as the claims with a liver cancer code in 2010 to 2012.
- **All claims of the population.** Every claim of the people selected, such as all claims from 2008 to 2014 of people treated for liver cancer in 2009.

## Tables

The 2026 form divides the tables into basic tables, which any project can request, and additional tables, which the review committee grants only when the application states why each is needed. Data can be requested for 2002 to 2024, and each delivered file is named by its table and year, as in `BFC_2002`.

| Table | 한글 | Group | First year | Codebook |
|---|---|---|---|---|
| Eligibility and premiums (BFC) | 자격 및 보험료 | Basic | 2002 | [BFC](../variables/custom/index.md#bfc) |
| Death (DTH) | 사망 | Basic | 2002 | [DTH](../variables/custom/index.md#dth) |
| Claim statements (T20) | 명세서 | Basic | 2002 | [T20](../variables/custom/index.md#t20) |
| Treatment details (T30) | 진료내역 | Basic | 2002 | [T30](../variables/custom/index.md#t30) |
| Diagnoses (T40) | 상병내역 | Basic | 2002 | [T40](../variables/custom/index.md#t40) |
| Prescriptions (T60) | 처방전교부상세 | Basic, with a drug use plan | 2002 | [T60](../variables/custom/index.md#t60) |
| General health screening, eligible population, results, and questionnaire | 일반1차검진 대상자, 결과, 문진 | Basic | 2002 | [G1E_OBJ](../variables/custom/index.md#g1e_obj), [G1E_RST](../variables/custom/index.md#g1e_rst), [GQ_RST](../variables/custom/index.md#gq_rst) |
| Healthcare providers | 요양기관 | Additional | 2002 | [INST](../variables/custom/index.md#inst) |
| Long-term care | 장기요양 | Additional | 2008 | [Four tables](../variables/custom/index.md#ltc_rcgt) |
| Cancer screening | 암 검진 | Additional | 2002, with cervical cancer from 2005 and lung cancer from 2019 | [Six cancers and the questionnaire](../variables/custom/index.md#cst) |
| Infant and child screening | 영유아 검진 | Additional | 2007 | [Eligible population and rounds 0 to 7](../variables/custom/index.md#inf_tgt) |
| Mother and newborn linkage | 산모-신생아 자료 | Additional | Through 2024 | [Linkage](../variables/custom/index.md#mother_child) |

A request for the prescription table (T60) must include a drug use plan (약제활용계획서) and a list of the drugs needed, and drugs missing from the list are not provided.[^drugs] Additional tables are requested by naming them under other requested data (요청자료-기타) and explaining, in the research methods, why each table is needed and how it will be used.

## How the extract differs from the cohort databases

The customized DB uses its own names and contains several fields that the cohort databases coarsen or omit.

- **Identifiers.** People are identified by `INDI_DSCM_NO` (개인식별아이디), and the claims tables are linked by `CMN_KEY` (공통키).
- **Diagnoses.** The claim statement table carries five diagnosis positions, `SICK_SYM1` to `SICK_SYM5`.
- **Residence and premiums.** The eligibility table records the district of actual residence (`RVSN_ADDR_CD`, 실거주주소코드), the premium amount (`CALC_CTRB_FD`), a premium vigintile (`CALC_CTRB_VTILE_FD`), and the six-digit industry of the workplace (`INDTP_CD`).
- **Death.** The death table gives the date of death (`DTH_ASSMD_DT`, 사망일자) but not its cause.

Cause of death requires a separate request for the cause-of-death database of the national statistics agency (통계청사망원인DB), entered under other requested data. The 2024 application guide states that only the National Sample Cohort and the Health Screening Cohort include cause of death, so the other databases do not. The same guide gives income level and education level as examples of variables the NHIS does not provide.

## Versions of the layouts

The NHIS publishes the column layouts of the customized DB as Excel files on the portal (고객지원, 자료실, 맞춤형 레이아웃). The layouts of September 10, 2026 replace those of 2024, which differ in the points below.

- **Claim statements.** T20 gained the provider type code (`YOYANG_CLSFC_CD`, 요양기관종별코드), for 28 variables.
- **Providers.** The provider table moved from the main layout file to its own file (요양기관 자료 제공 컬럼 레이아웃).

The layouts for general health screening, cancer screening and its questionnaire, and infant and child screening were consulted only in their 2026 versions.

The application form of 2026 lets applicants request data through 2024, while the 2024 application guide allowed requests through 2023.

## Analysis environment

Researchers analyze customized extracts at NHIS analysis centers (분석센터). The cohort manuals add that research on the diagnoses and procedures they mask can be carried out without masking in designated analysis rooms, using customized data.

## Still to be documented

!!! note "To be written"
    The fees, the time from application to access, and whether remote analysis is possible.

[^drugs]: The guide asks applicants to request drugs at the coarsest level that serves the study, such as groups or the first four digits of the ingredient code.
