# Using the data

Researchers never receive NHIS microdata, because every analysis runs on NHIS servers. The sample databases can be reached remotely from the researcher's own computer, while a customized DB opens only on a computer at an NHIS analysis center. In both cases, results leave the NHIS servers only after they pass the export review (반출 심사), described at the end of this page.

!!! info "Sources"
    This page follows the [NHISS portal](https://nhiss.nhis.or.kr) as seen in October 2026, namely its pages on the research process (연구진행 절차안내), remote analysis (가상화연구분석 안내), and the analysis centers (분석센터소개), and its frequently asked questions (자주묻는 질문). It also draws on the National Sample Cohort manual (version 1.5), the NHIS guide to new applications (사용자매뉴얼1, version 4.0, September 2024), and press reports on the Low-Risk Sample Dataset from July 2026.

## Where each database is analyzed

All databases are analyzed in a virtual research room, and they differ in where the room can be opened. A virtual research room (가상화 연구룸) is a virtual computer on NHIS servers, assigned to one approved project, that holds the project's data and the statistical software chosen for it.

| Database | 한글 | Where the room is opened | Longest use of a room |
|---|---|---|---|
| [National Sample Cohort](../datasets/nsc.md) | 표본코호트DB | The researcher's own computer, by remote access | 6 months |
| [Health Screening Cohort](../datasets/heals.md) | 건강검진코호트DB | The researcher's own computer, by remote access | 6 months |
| [Senior Cohort](../datasets/senior.md) | 노인코호트DB | The researcher's own computer, by remote access | 6 months |
| [Low-Risk Sample Dataset](../datasets/low-risk.md) | 저위험 표본데이터셋 | Remote access, according to press reports[^lowrisk] | Not stated |
| [Customized Research DB](../datasets/customized.md) | 맞춤형연구DB | A computer at an NHIS analysis center | 1 year |

The sample databases share one remote route, which the portal describes on its research process page. The NHIS delivers the data through its remote research analysis system (원격연구분석시스템), and the researcher connects to the room over a VPN from their own computer. The manual of the National Sample Cohort dates this route to release 2.0 of 2017, which introduced online analysis on a remote server. The longest use of a room comes from the portal's FAQ of October 2024, which sets the limits so that rooms circulate among projects.

## Remote access to the sample databases

A sample database is opened from the researcher's own computer after a short setup on the portal. Once the project is approved, the fee is paid, and the security documents (보안관련 서류) are submitted, the NHIS provides the data in a virtual research room. The portal's FAQ then describes the connection in three steps, taken after the researcher sets the start date of the room. First, the researcher sets a password and mobile phone number for the room on the portal, under 가상화연구분석, 가상화, 가상화 비밀번호 변경. Second, the researcher installs the security programs offered on the portal (보안프로그램 설치), including the SSL VPN agent (Axgate). Finally, the researcher opens the VPN agent from the icon it places on the desktop and logs in to the room with the ID and password.

## Analysis centers for customized DBs

A customized DB opens only on a computer at one of the NHIS big data analysis centers. These centers (빅데이터 분석센터) are the NHIS counterpart of a research data center, where the researcher logs in to the project's virtual research room after staff check their identity. The extract itself is built beforehand on an NHIS computer in Wonju or Seoul, as described on the [Applying for data](access.md#step-1-application-documents) page.

Using a center requires a reservation, and the NHIS bars researchers who miss reservations or break the rules. The centers open from 9:00 to 18:00 on weekdays except public holidays, and seats are reserved on the portal under 가상화연구분석, 분석센터이용, 분석센터예약 from 9:00 two weeks before the day of use. A reservation can be canceled on the portal until 8:00 on the day of use, and a reservation that is neither canceled nor used counts as a no-show. Two no-shows bar every researcher on the project from the centers for one week, and three no-shows bar them for two weeks.

The NHIS operating rules (국민건강정보자료 제공 운영지침) set the conduct inside a center, and the portal's FAQ summarizes them as follows.

- **Identity.** Researchers show an ID card and sign the entry log (출입관리대장) on entering and leaving.
- **Cameras.** Security stickers go on the front and back cameras of phones, tablets, and laptops, and staff check them when the researcher leaves.
- **Devices.** Tablets, laptops, USB drives, and external hard drives cannot be used inside the center.
- **Files.** Files needed for the analysis are brought into the room in advance through an import request, described [below](#files-in-and-results-out).

Breaking the rules on identity, cameras, devices, or disturbing others bars the researcher from the centers for one week the first time, one month the second time, and permanently the third time. Analysis aimed at identifying a person, sharing an account, or exporting intermediate results without approval can instead lead to the cancellation of the data provision.

### List of analysis centers

The current list of centers, with addresses and phone numbers, is on the [NHISS portal](https://nhiss.nhis.or.kr) under 가상화연구분석, 분석센터소개. The portal opens its pages only through its own menus, so the list cannot be linked directly from this site. In October 2026, the portal listed the 14 centers below, matching the count in its FAQ.[^research]

| Center | 한글 | Location |
|---|---|---|
| Wonju headquarters | 빅데이터 원주(본부) 분석센터 | NHIS headquarters, Wonju |
| Seoul | 빅데이터 분석센터(서울) | Post Tower, Jung-gu, Seoul |
| Busan regional headquarters | 부산지역본부 분석센터 | Buk-gu, Busan |
| Daegu regional headquarters | 대구지역본부 분석센터 | Dalseo-gu, Daegu |
| Gwangju regional headquarters | 광주지역본부 분석센터 | Seo-gu, Gwangju |
| Jeonju Bukbu branch | 전주북부 분석센터 | Wansan-gu, Jeonju |
| Daejeon regional headquarters | 대전지역본부 분석센터 | Sejong |
| Cheongju Seobu branch | 청주서부 분석센터 | Heungdeok-gu, Cheongju |
| Gyeongin regional headquarters | 경인지역본부 분석센터 | Paldal-gu, Suwon |
| NHIS Ilsan Hospital | 일산병원 분석센터 | Ilsandong-gu, Goyang |
| Seoul National University Hospital | 서울대병원 분석센터 | Jongno-gu, Seoul |
| Yonsei University Health System | 연세의료원 분석센터 | Seodaemun-gu, Seoul |
| Seoul National University | 서울대학교 분석센터 | Gwanak-gu, Seoul |
| Korea University Medical Center | 고려대의료원 분석센터 | Seongbuk-gu, Seoul |

At least one of the centers at universities and hospitals is open only to its own researchers. The Yonsei center admits only [Yonsei faculty, staff, and researchers](https://dhc.severance.healthcare/dhc/analysiscenter02.do), and the rules of the other university and hospital centers have not been checked for this page.

## Being in Korea

Both access routes require the researcher to be physically in Korea while working with the data. Remote access to the sample databases works only from within Korea, and a customized DB opens only inside an analysis center. The principal investigator must also be a Korean national living in Korea, according to the portal's guide to remote analysis. A researcher based abroad can therefore work with the data only during a stay in Korea.

## Period of use and fees

A project is charged by the length of its period of use, within an approval of up to two years. The review committee sets the approval period (자료이용 승인기간), and an extension, granted in one-year units, must be requested before the approval expires. Within that period, the applicant chooses the period of use (사용기간) on the application and can reset it when the fee notice is issued. A project that is not finished when its period of use ends can request, before the end date, either an extension of the period or the storage of its files (연구자료보관). Since October 2024, storage costs 1,000 won per GB per month, for up to 50 GB and up to 12 months, renewable within the approval period.

The fee for the period of use follows the schedule below for a customized DB, and sample databases pay half.

| Period of use | Fee for a customized DB |
|---|---|
| Less than one week | 50,000 won per day |
| One week to less than one month | 225,000 won per week, plus 50,000 won for each remaining day |
| One month or more | 700,000 won per month, plus the weekly and daily fees for the remaining weeks and days |

A project with more than 200 GB of data also pays 10,000 won for each additional GB, and the principal investigator pays all fees on the portal within two weeks of the notice. Payment is by credit card or bank transfer, and a fee cannot be refunded once it is paid.

## Files in and results out

Nothing enters or leaves a virtual research room except through a request on the portal. Files needed for the analysis, such as code, are brought in through an import request (자료반입신청), which should be made before the session that needs them. Results, including intermediate output during the project, leave only through an export request (자료반출신청) and must pass the export review (반출 심사) before release. At the end of the project, the NHIS takes back the room and deletes the data.

[^lowrisk]: [Press reports](https://akomnews.com/67640) of the second pilot, which began in June 2026, say that the dataset is provided over the NHIS remote network (원격망) to academic researchers and to companies doing research in the public interest. An application needs only a form and a pledge (신청서, 확약서), followed by an internal review, and the fee is waived during the pilot. The portal lists the dataset among the applications for sample research databases but does not describe its access route or the longest use of its room.

[^research]: The portal also lists a center named 빅데이터 분석센터(리서치) without an address or phone number, which the table leaves out.
