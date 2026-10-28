# NHIS research databases

The NHIS releases two kinds of research data, namely ready-made sample databases and customized databases extracted for a specific study. All of them are drawn from the National Health Information Database (국민건강정보DB), which holds eligibility, claims, health screening, and death records for the whole population.

## Sample databases

The sample databases (표본연구DB) are fixed samples, and three of them follow the same people over many years. They are the usual starting point because they are cheaper and faster to obtain than a customized extract.

| Database | 한글 | Population | Sample | Years | Cohort profile |
|---|---|---|---|---|---|
| [National Sample Cohort (NHIS-NSC)](../datasets/nsc.md) | 표본코호트DB | Enrolled throughout 2006, all ages | 1,000,000 | 2002-2023 | Lee et al. (2017)[^profile] |
| [Health Screening Cohort (NHIS-HEALS)](../datasets/heals.md) | 건강검진코호트DB | Aged 40 to 79 and screened in 2002 or 2003 | 514,866 | 2002-2023 | Seong et al. (2017) |
| [Senior Cohort (NHIS-Senior)](../datasets/senior.md) | 노인코호트DB | Aged 60 to 80 and enrolled in 2008 | 511,953 | 2002-2023 | Kim et al. (2019)[^profile] |
| [Low-Risk Sample Dataset](../datasets/low-risk.md) | 저위험 표본데이터셋 | Used medical care in 2014 to 2023 | 1,000,000 | 2014-2023 | None |

The NHISS portal also lists an educational sample research DB (교육용 표본연구DB), which is not yet documented here. The [Datasets](../datasets/index.md) section compares the databases in detail.

## Customized research databases

A [customized research DB](../datasets/customized.md) (맞춤형연구DB) is extracted from the full National Health Information Database to match the population and variables of an approved research protocol. It can cover everyone who meets the study criteria rather than a sample, at the cost of a longer review and [analysis at an NHIS analysis center](using.md#analysis-centers-for-customized-dbs).

Full citations for the cohort profiles are on the [references page](../references.md).

[^profile]: These cohort profiles describe earlier releases. Lee et al. (2017) describe release 1.0 of the National Sample Cohort, drawn from the 2002 population, and Kim et al. (2019) describe release 1.0 of the Senior Cohort, drawn from people aged 60 and older in 2002.
