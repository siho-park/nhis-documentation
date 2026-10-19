---
date: 2026-10-19
authors:
  - siho
categories:
  - Measurement
slug: visits-admissions-and-spending
---

# Counting visits, admissions, and spending

A claim is a billing unit, so a count of claims is not a count of visits or admissions. Measures of utilization and spending need to account for how care is split into claims, and the splitting differs by setting and has changed over time.

<!-- more -->

## Outpatient visits

Counts of outpatient claims can change even when the number of visits does not. In the National Sample Cohort, outpatient billing moved from one claim per month to one claim per visit day, a change extended to hospitals in 2011, as noted on the [dataset page](../../datasets/nsc.md#known-issues). The claim statement table T20 (명세서) also records the days of visits or inpatient days on each claim in `VSHSP_DD_CNT` (입내원일수).

Drugs dispensed at a pharmacy are billed on separate pharmacy claims, apart from the visit that generated the prescription. Counting pharmacy claims as visits therefore counts the same visit twice.

## Inpatient admissions

A long inpatient stay can be billed on several claims, so counting inpatient claims overstates admissions. Admissions are usually reconstructed by linking inpatient claims for the same person and provider whose dates of care are contiguous or overlap.

## Spending

The amount fields of the claim statement table measure covered spending after review, which differs from the amount the provider originally claimed. The total covered cost after review `ED_RC_TOT_AMT` (심결요양급여비용총액) is divided into patient cost sharing `EDC_SBA` (심결본인부담금) and the insurer payment `EDC_INSUR_BRDN_AMT` (심결보험자부담금).

- **Reviewed and claimed amounts.** Use the amounts after review rather than the amounts originally claimed by the provider, since only the reviewed amounts were paid.
- **Pharmacy spending.** Drugs dispensed at a pharmacy are billed on separate pharmacy claims, so dropping pharmacy claims omits most outpatient drug spending.
- **Inflation.** Amounts are in nominal won and should be deflated before comparing years.
- **Non-covered services.** Spending on non-covered services (비급여) is not in the data at all, as the post on [non-covered services](03-non-covered-services.md) explains.
