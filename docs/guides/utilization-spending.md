# Utilization and spending

A claim is a billing unit, so counts of claims are not counts of visits or admissions. Measures of utilization and spending need to be built from the fields of the claims table that record days of care and amounts, with attention to how claims are split.

## Outpatient visits

TODO. Whether one outpatient claim can cover several visit days, how to count visits from the days of visits field `VSHSP_DD_CNT` (입내원일수), and how pharmacy claims should be excluded from visit counts.

## Inpatient admissions

A long inpatient stay can be billed on several claims, so counting inpatient claims overstates admissions. Admissions are usually reconstructed by linking inpatient claims for the same person and provider whose dates of care are contiguous or overlap.

!!! note "To be written"
    The rule used to split long stays into several claims, the fields that identify the admission date, and a tested algorithm for reconstructing admissions.

## Spending

The amount fields record covered spending after review (`ED_RC_TOT_AMT`), divided into patient cost sharing (`EDC_SBA`) and the insurer payment (`EDC_INSUR_BRDN_AMT`). Spending that patients pay for non-covered services (비급여) is not in the data, so total spending measured from claims understates what patients actually pay.

- **Reviewed and claimed amounts.** Use the amounts after review rather than the amounts originally claimed by the provider, since only the reviewed amounts were paid.
- **Pharmacy spending.** Drugs dispensed at a pharmacy are billed on separate pharmacy claims, so dropping pharmacy claims omits most outpatient drug spending.
- **Inflation.** Amounts are in nominal won and should be deflated before comparing years.

!!! note "To be written"
    How spending for Medical Aid beneficiaries is recorded and whether it is comparable with spending for the insured.
