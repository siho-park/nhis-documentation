---
date: 2026-10-19
authors:
  - siho
categories:
  - Getting started
slug: building-an-analysis-sample
---

# Building an analysis sample

Most projects with NHIS data follow people over time, so the first real task is a panel with one row per person and year. The key decision is where that panel comes from. It should be built from the eligibility table, not from the claims tables, because people who use no care in a year have no claims and would otherwise vanish from the sample.

<!-- more -->

## Why the claims are the wrong place to start

A panel built from the claims contains only people who used care, which distorts almost any average computed from it. A person with no visits in a year has no claims in that year, so the person-year is missing rather than recorded as zero. Average spending per person computed from such a panel describes people who saw a provider and overstates spending in the population.

The eligibility and premium table BNC (자격 및 보험료) avoids this problem, because it has one row per person per year whether or not the person used care. Starting from BNC keeps the people who used no care in the sample, with zeros for their outcomes.

## Three steps to a person-year panel

The construction has three steps, and each step works on a different part of the data. The post on [how the tables fit together](01-how-the-tables-fit-together.md) explains the merge keys used along the way.

First, define the population and the observation window in the eligibility table BNC. Restrictions on age, sex, region, insurance type, and years are applied here, and the year and month of death `DTH_YYYYMM` (사망연월) in the birth and death table BND (출생 및 사망) determine the last year in which a person is at risk.

Second, compute outcomes in the claims tables at the claim level, such as an indicator for a diagnosis or the amount paid. Then collapse them to the person and year, using the person identifier `RN_INDI` (개인고유번호) and either the reference year `STD_YYYY` (기준연도) or the year of the start date of care `MDCARE_STRT_DT` (요양개시일자).

Finally, merge the person-year outcomes onto the eligibility panel and fill the person-years without a match with zeros. A missing person-year at this stage means that the person used no covered care, not that the data are missing, and the post on [non-covered services](03-non-covered-services.md) explains why the word covered matters.

## Choices that shape the sample

Two further choices change who is in the sample and how their outcomes compare, and both are worth stating in the paper.

- **Left censoring.** The data begin in 2002, so a condition first observed in 2002 may have begun earlier. Studies of new cases usually exclude people with the condition in a washout period at the start of the data.
- **Deaths.** Outcomes in the year of death cover only part of the year, so annual outcomes in that year are not comparable with those of survivors unless they are scaled by time at risk.
