---
date: 2026-10-19
authors:
  - siho
categories:
  - Caveats
slug: five-pitfalls-to-check-before-you-start
---

# Five pitfalls to check before you start

Some features of the NHIS data are easy to miss, because nothing in the variable names reveals them. The larger caveats have their own posts, on [non-covered services](03-non-covered-services.md), [diagnosis codes](04-identifying-conditions.md), [counting visits and admissions](05-visits-admissions-spending.md), and [people without claims](02-building-an-analysis-sample.md). This post collects five smaller ones that are worth checking before the analysis begins.

<!-- more -->

## The premium decile is not an income decile

Premiums are computed from wages for employee insured and from income and property for self-employed insured, and dependents take the decile of the person they depend on. The same decile therefore corresponds to different incomes across insurance types. The [National Sample Cohort page](../../datasets/nsc.md#known-issues) describes further features of [`CTRB_Q10`](../../variables/nsc/bnc/ctrb_q10.md) (보험료분위 10분위, premium decile), including the shifts after the 2018 and 2022 premium reforms.

## Variable names change across releases

Different releases of the same database use different names for many variables, so code written for one release does not run on another without changes. Check the release before reusing code from a paper or a colleague.

## Identifiers do not link across databases

Each release has its own pseudonymized person identifier, so the same person cannot be followed from one database to another. The data also cannot be linked to external sources without a separate approval. See [`RN_INDI`](../../variables/nsc/bnc/rn_indi.md) (개인고유번호, person identifier) in the National Sample Cohort.

## Diagnosis and district codes change over time

Diagnosis codes follow successive revisions of the Korean Classification of Diseases, and district codes change when administrative boundaries are redrawn. Both need a crosswalk before comparisons across years. The [district code list](../../variables/nsc/codes/sgg.md) of the National Sample Cohort, for example, lists the districts of Gangwon under province code 42 and again under 51, the code of 강원특별자치도 (Gangwon Special Self-Governing Province) from 2023.

## Results must pass export review

Nothing leaves the analysis environment without passing the NHIS export review (반출 심사), which applies rules on minimum cell sizes. Plan the tables and figures in advance, since each export request takes time. See [Applying for data](../../overview/access.md).
