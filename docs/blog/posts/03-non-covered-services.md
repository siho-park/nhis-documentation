---
date: 2026-10-19
authors:
  - siho
categories:
  - Caveats
slug: non-covered-services-are-missing
---

# Non-covered services are missing from the claims

The NHIS claims record only the care that insurance pays for, and this limit shapes every measure of spending and utilization. Services that patients pay for entirely out of pocket are never billed to the insurer, so they leave no trace in the data.

<!-- more -->

## Covered and non-covered services

Korean health insurance divides medical services into two groups, and only one of them produces claims. Covered services (급여) are billed to the insurer, and the patient pays a share of the cost. Non-covered services (비급여) are paid for entirely by the patient, so they are not billed to the insurer and do not appear in the claims.

## What the claims can and cannot measure

Spending measured from the claims is covered spending, which falls short of what patients actually spend on care. The claim statement table T20 (명세서) records the total covered cost after review `ED_RC_TOT_AMT` (심결요양급여비용총액), divided into patient cost sharing `EDC_SBA` (심결본인부담금) and the insurer payment `EDC_INSUR_BRDN_AMT` (심결보험자부담금). None of these amounts include spending on non-covered services.

Utilization measured from the claims is understated for the same reason. A service paid for entirely out of pocket generates no claim, so it is missing from counts of services as well as from spending.

The patient cost sharing variable needs particular care in the write-up. `EDC_SBA` records what patients paid toward covered services only, while total out-of-pocket spending also includes everything paid for non-covered services. `EDC_SBA` is therefore a lower bound on out-of-pocket spending rather than a measure of it.

## Why the gap matters for comparisons

The gap varies across conditions, provider types, and years, which matters more than its average size. A comparison across any of these dimensions mixes differences in care with differences in the share of care that is non-covered. A trend in covered spending, for example, can reflect services moving into or out of coverage rather than a change in the care people receive.

## What to do in practice

Three habits keep the gap from distorting the results.

- **Name the measure precisely.** Describe outcomes as covered spending or covered utilization, in the text and in the titles of tables and figures.
- **Report cost sharing for what it is.** Describe `EDC_SBA` as patient cost sharing for covered services, not as total out-of-pocket spending.
- **Check comparisons for differences in coverage.** When comparing conditions, provider types, or years, consider whether the non-covered share is likely to differ between the groups, since the claims cannot measure that difference.
