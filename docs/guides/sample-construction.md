# Constructing an analysis sample

Most projects need a panel of people observed over time with outcomes measured from claims. The panel should be built from the eligibility table, not from the claims tables, because people who use no care in a year have no claims and would otherwise vanish from the sample.

## Building a person-year panel

The construction has three steps.

First, define the population and observation window from the eligibility table, which has one row per person per year. Restrictions on age, sex, region, insurance type, and years are applied here, and the year and month of death in the birth and death table determine the last year in which a person is at risk.

Second, compute outcomes from the claims tables at the claim level, such as an indicator for a diagnosis or the amount paid, and collapse them to the person-year using the person identifier `RN_INDI` and the reference year `STD_YYYY`, or the year of the start date of care `MDCARE_STRT_DT`.

Finally, merge the person-year outcomes onto the eligibility panel and fill unmatched person-years with zeros, since a missing person-year means no covered care rather than missing data.

## Choices that affect the sample

- **Left censoring.** The data begin in 2002, so a condition first observed in 2002 may have begun earlier. Studies of new cases usually exclude people with the condition in a washout period at the start of the data.
- **Deaths.** Outcomes in the year of death cover only part of the year, so annual outcomes in that year are not comparable with those of survivors unless they are scaled by time at risk.
- **Attrition.** TODO. How emigration and loss of eligibility appear in each database.

!!! note "To be written"
    Worked examples for an incident disease cohort and an event-study panel around a screening or policy change.
