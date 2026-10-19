# Identifying conditions

Diagnosis codes in claims are recorded to justify payment, not to document a confirmed diagnosis. A code can appear because a condition was confirmed, because it was suspected and a test was ordered to rule it out, or because it qualifies the claim for a particular payment rule, so a single claim with a code is weak evidence that a person has the condition.

## Operational definitions

Studies with NHIS data therefore define a condition by a combination of claims rather than a single code. The definitions below are common in the literature, listed from least to most restrictive.

- **Any claim.** At least one claim with the code in any diagnosis position. This maximizes sensitivity but counts rule-out diagnoses.
- **Repeated or inpatient claims.** At least two outpatient claims, or one inpatient claim, with the code. This is the most common definition for chronic conditions.
- **Diagnosis plus treatment.** A claim with the code together with a prescription or procedure specific to the condition, such as an antidiabetic drug for diabetes.

The choice should follow a published validation study whenever one exists for the condition.

!!! note "To be written"
    A table of validated definitions by condition, with the validation study for each.

## Diagnosis position

The claim statement table (T20) stores the primary diagnosis `SICK_SYM1` and one secondary diagnosis `SICK_SYM2`, while the diagnosis table (T40) stores every diagnosis on the claim in `MCEX_SICK_SYM`. A definition based only on the claims table therefore misses conditions recorded in later positions, which matters most for chronic conditions that are rarely the reason for a visit.

## Masked diagnoses

In the National Sample Cohort, 3,116 sensitive diagnosis codes, including mental disorders, pregnancy and childbirth, and notifiable infectious diseases, show only their first letter followed by an underscore. Conditions in these groups cannot be identified from the cohort, and the NHIS directs such studies to the customized research DB, as described on the [dataset page](../datasets/nsc.md).

## Special co-payment registration

Patients with cancer and several other serious conditions can register for a reduced co-payment (산정특례), and registration requires medical confirmation. Registration records are therefore a more specific marker of these conditions than diagnosis codes alone.

!!! note "To be written"
    Where registration codes are stored in each database, the code list, and the conditions covered in each year.

## Code revisions

Diagnosis codes follow the Korean Classification of Diseases (KCD), a Korean adaptation of ICD-10 that has been revised several times. A code list written for one revision should be checked against the revision in force in each year of the data.
