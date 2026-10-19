---
date: 2026-10-19
authors:
  - siho
categories:
  - Measurement
slug: identifying-conditions
---

# Identifying conditions from diagnosis codes

A diagnosis code on a claim looks like a diagnosis, but it is recorded to justify payment rather than to confirm a condition. A code can appear because a condition was confirmed, because it was suspected and a test was ordered to rule it out, or because it qualifies the claim for a particular payment rule. A single claim with a code is therefore weak evidence that a person has the condition.

<!-- more -->

## Common definitions

Studies with NHIS data therefore define a condition by a combination of claims rather than by a single code. The definitions below are common in the literature, listed from least to most restrictive.

- **Any claim.** At least one claim with the code in any diagnosis position. This maximizes sensitivity but counts rule-out diagnoses.
- **Repeated or inpatient claims.** At least two outpatient claims, or one inpatient claim, with the code. This is the most common definition for chronic conditions.
- **Diagnosis plus treatment.** A claim with the code together with a prescription or procedure specific to the condition, such as an antidiabetic drug for diabetes.

The choice should follow a published validation study whenever one exists for the condition.

## Where the diagnoses are stored

A definition based only on the claim statement table misses diagnoses recorded in later positions on the claim. The claim statement table T20 (명세서) stores the primary diagnosis `SICK_SYM1` (주상병) and one secondary diagnosis `SICK_SYM2` (부상병), while the diagnosis table T40 (상병내역) stores every diagnosis on the claim in `MCEX_SICK_SYM` (요양급여상병기호). The difference matters most for chronic conditions, which are rarely the reason for a visit.

## Masked diagnoses

Some conditions cannot be identified in the National Sample Cohort at all, because their codes are masked. In the cohort, 3,116 sensitive diagnosis codes, including mental disorders, pregnancy and childbirth, and notifiable infectious diseases, show only their first letter followed by an underscore. The NHIS directs studies of these conditions to the customized research DB, as described on the [dataset page](../../datasets/nsc.md).

## Special co-payment registration

For cancer and several other serious conditions, registration for a reduced co-payment offers a more specific marker than diagnosis codes. Patients with these conditions can register for a reduced co-payment (산정특례), and registration requires medical confirmation.

## Code revisions

Diagnosis codes follow the Korean Classification of Diseases (KCD), a Korean adaptation of ICD-10 that has been revised several times. A code list written for one revision should be checked against the revision in force in each year of the data.
