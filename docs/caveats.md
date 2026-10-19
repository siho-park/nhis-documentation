# Caveats

This page collects features of the data that commonly lead to mistakes. Each caveat links to the page where it is discussed in detail, and new caveats are welcome through the [contributing process](about/contributing.md).

## Non-covered services are missing

<span class="status status-unverified">Unverified</span> Claims record only services covered by insurance (급여). Services that patients pay for entirely out of pocket (비급여) are not billed to the insurer and do not appear, so spending and utilization measured from claims understate the total, by different amounts across conditions and provider types. See [Utilization and spending](guides/utilization-spending.md).

## A diagnosis code is not a diagnosis

<span class="status status-unverified">Unverified</span> Codes are recorded to justify payment and include suspected conditions that were later ruled out. A single claim with a code overstates prevalence, which is why most studies require repeated claims or an accompanying treatment. See [Identifying conditions](guides/identifying-conditions.md).

## A claim is not a visit or an admission

<span class="status status-unverified">Unverified</span> A claim is a billing unit. Long inpatient stays are billed on several claims, and pharmacy dispensing is billed separately from the visit that generated the prescription. See [Utilization and spending](guides/utilization-spending.md).

## People without claims do not appear in the claims tables

<span class="status status-unverified">Unverified</span> A sample built from the claims tables contains only people who used care. Build the panel from the eligibility table and fill zeros for person-years without claims. See [Constructing an analysis sample](guides/sample-construction.md).

## The premium decile is not an income decile

<span class="status status-unverified">Unverified</span> Premiums are computed from wages for employee insured and from income and property for self-employed insured, and dependents take the decile of the person they depend on. The same decile therefore corresponds to different incomes across insurance types. See [`CTRB_Q10`](variables/nsc/bnc/ctrb_q10.md) in the National Sample Cohort.

## Variable names change across releases

<span class="status status-unverified">Unverified</span> Different releases of the same database use different names for many variables, so code written for one release does not run on another without changes. Check the release before reusing code from a paper or a colleague.

## Identifiers do not link across databases

<span class="status status-unverified">Unverified</span> Each release has its own pseudonymized person identifier, so the same person cannot be followed from one database to another, and the data cannot be linked to external sources without a separate approval. See [`RN_INDI`](variables/nsc/bnc/rn_indi.md) in the National Sample Cohort.

## Diagnosis and district codes change over time

<span class="status status-unverified">Unverified</span> Diagnosis codes follow successive revisions of the Korean Classification of Diseases, and district codes change when administrative boundaries are redrawn. Both need a crosswalk before comparisons across years. The [district code list](variables/nsc/codes/sgg.md) of the National Sample Cohort, for example, lists the districts of Gangwon under province code 42 and again under 51, the code of 강원특별자치도 (Gangwon Special Self-Governing Province) from 2023.

## Results must pass export review

<span class="status status-unverified">Unverified</span> Nothing leaves the analysis environment without passing the NHIS export review (반출 심사), which applies rules on minimum cell sizes. Plan the tables and figures in advance, since each export request takes time. See [Applying for data](overview/access.md).
