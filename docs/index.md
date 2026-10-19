# NHIS Data Documentation

This site is an unofficial guide to the research databases of the Korean National Health Insurance Service (NHIS, 국민건강보험공단). The NHIS releases these databases through its [data sharing service](https://nhiss.nhis.or.kr), but the documentation that comes with them is limited to short variable lists. Many variables are self-explanatory, while others mean something different from what their names suggest, and researchers usually learn these differences by trial and error.

The site collects that knowledge in one place, including variable definitions, guidance on constructing analysis samples, and known caveats. It is modeled on the documentation that the [Research Data Assistance Center (ResDAC)](https://resdac.org) provides for Medicare data and on Kyle Barron's [Medicare documentation](https://kylebarron.dev/medicare-documentation/).

## What is on this site

The site has five parts.

- [**Program and data**](overview/index.md) describes the health insurance system that generates the data, the family of NHIS research databases, and the application process.
- [**Datasets**](datasets/index.md) has one page per database, covering sample design, versions, and linkage.
- [**Variables**](variables/index.md) documents each table and variable, with Korean and English labels, value codes, and notes.
- [**Working with the data**](blog/index.md) is a series of short posts on practical issues, such as merging the tables, building an analysis sample, and the caveats that commonly lead to mistakes.
- [**Glossary**](glossary.md) translates the Korean administrative terms used in the data and the official documentation.

## Disclaimer

This site is not affiliated with or endorsed by the NHIS. Entries are written by researchers who use the data and may contain errors, so check them against the documentation that comes with your extract before relying on them.

## Contributing

Corrections, additions, and blog posts are welcome from anyone who has worked with the data, and the easiest way to send them is an email to [sihopark@kdischool.ac.kr](mailto:sihopark@kdischool.ac.kr?subject=NHIS%20Data%20Documentation). The [contributing page](about/contributing.md) explains what to include and how the codebook files are organized.

Maintained by Siho Park, KDI School of Public Policy and Management.
