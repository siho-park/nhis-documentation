# Code examples

The snippets on this page are short, self-contained examples of common tasks. They use the variable names of the [National Sample Cohort 2.2](../variables/nsc/index.md), with `t40` standing for the appended diagnosis files (`NSC2_M40`, `NSC2_D40`, and `NSC2_K40` for all periods) and `bnc` for the eligibility and premium files. File names and storage types should be adjusted to match your extract.

!!! warning "Not yet tested"
    These examples have not yet been run against the data. Please report any errors.

## Flagging a condition in a person-year panel

This example flags person-years with at least two claims carrying a diabetes code (KCD E10 to E14) in any diagnosis position, and merges the flag onto the eligibility panel so that people without claims get a zero.

=== "Stata"

    ```stata
    * Diagnosis table, one row per diagnosis on a claim
    use RN_INDI RN_KEY MDCARE_STRT_DT MCEX_SICK_SYM using "t40.dta", clear
    keep if inlist(substr(MCEX_SICK_SYM, 1, 3), "E10", "E11", "E12", "E13", "E14")

    * Count distinct claims per person-year
    gen STD_YYYY = substr(MDCARE_STRT_DT, 1, 4)
    duplicates drop RN_INDI RN_KEY, force
    bysort RN_INDI STD_YYYY: gen n_claims = _N
    by RN_INDI STD_YYYY: keep if _n == 1
    gen diabetes = n_claims >= 2
    keep RN_INDI STD_YYYY diabetes
    tempfile dm
    save `dm'

    * Merge onto the eligibility panel and fill zeros
    use "bnc.dta", clear
    merge 1:1 RN_INDI STD_YYYY using `dm', keep(master match) nogenerate
    replace diabetes = 0 if missing(diabetes)
    ```

=== "SAS"

    ```sas
    proc sql;
      /* Count distinct claims per person-year */
      create table dm as
      select RN_INDI,
             substr(MDCARE_STRT_DT, 1, 4) as STD_YYYY,
             (count(distinct RN_KEY) >= 2) as diabetes
      from t40
      where substr(MCEX_SICK_SYM, 1, 3) in ('E10', 'E11', 'E12', 'E13', 'E14')
      group by 1, 2;

      /* Merge onto the eligibility panel and fill zeros */
      create table panel as
      select a.*, coalesce(b.diabetes, 0) as diabetes
      from bnc as a
      left join dm as b
        on a.RN_INDI = b.RN_INDI and a.STD_YYYY = b.STD_YYYY;
    quit;
    ```

=== "R"

    ```r
    library(data.table)

    t40 <- fread("t40.csv", colClasses = "character")
    bnc <- fread("bnc.csv", colClasses = list(character = c("RN_INDI", "STD_YYYY")))

    # Count distinct claims per person-year
    dm <- t40[substr(MCEX_SICK_SYM, 1, 3) %in% sprintf("E%d", 10:14)]
    dm <- unique(dm[, .(RN_INDI, RN_KEY, STD_YYYY = substr(MDCARE_STRT_DT, 1, 4))])
    dm <- dm[, .(diabetes = as.integer(.N >= 2)), by = .(RN_INDI, STD_YYYY)]

    # Merge onto the eligibility panel and fill zeros
    panel <- merge(bnc, dm, by = c("RN_INDI", "STD_YYYY"), all.x = TRUE)
    panel[is.na(diabetes), diabetes := 0L]
    ```

The flag counts claims, not visits, and does not distinguish inpatient from outpatient claims. The [identifying conditions](identifying-conditions.md) guide discusses stricter definitions.
