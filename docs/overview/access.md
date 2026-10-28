# Applying for data

Applications are submitted through the NHIS data sharing service (건강보험자료공유서비스) at [nhiss.nhis.or.kr](https://nhiss.nhis.or.kr). The portal handles the application, the review, and payment, but it says little about how long each stage takes or what reviewers look for, so this page records what applicants have learned.

The questions of the application appear only after logging in and starting a request, so this page lists them in advance. Most of the answers, and the research summary in particular, can then be drafted before the portal is opened and before the IRB application is written, since both must describe the same study.

!!! warning "Write the application and the IRB protocol in Korean"
    The research summary, the drug research plan, and the IRB protocol attached to the application should all be written in Korean. An application whose IRB protocol was written in English has been rejected. Researchers whose IRB approval comes from a review board abroad, or was written in English, should prepare Korean versions of the documents before applying.

!!! info "Sources"
    This page follows the NHIS guide to new applications (사용자매뉴얼1, 연구용DB 신규신청 방법, version 4.0, September 2024), the NHIS notice on researcher extraction of customized DBs (맞춤형 DB 제공 방식 변경 안내, July 2025), the customized DB request form of 2026, and the portal as seen by applicants in 2026. The portal changes from time to time, so the wording of a question may differ slightly from the wording here.

## Steps of an application

An application is entered on the portal under 연구과제, 연구DB 신청, in six steps. Steps 1 to 4 and step 6 are the same for the sample and customized databases, and step 5 applies to customized DBs only.

| Step | 한글 | Content |
|---|---|---|
| 1 | 신청서류 작성 | Applicant type, research type, requests to the NHIS, and linkage with data of other institutions |
| 2 | IRB서류 첨부 및 사용기간 설정 | IRB approval notice and protocol, and the period of data use |
| 3 | 연구과제요약서 작성 | Research summary, which the review committee reads, and the drug or medical device plan if needed |
| 4 | 연구원 등록 | Principal investigator, co-investigators, and research assistants |
| 5 | 데이터셋 추출 방식 설정 | Extraction method, study population, tables, and variables, described on the [customized DB page](../datasets/customized.md#building-the-extract) |
| 6 | 본인인증 및 신청 완료 | Identity verification by every registered researcher |

## Step 1. Application documents

The first screen classifies the project and collects requests to the NHIS.

| Question | 한글 | Options and notes |
|---|---|---|
| Applicant type | 신청자 유형 | Government ministry (정부부처), public institution (공공기관), public research institution (공공연구기관), or other research such as private companies (기타연구, 민간기업). Universities and hospitals choose public research institution. |
| Part-time expert | 비상근전문위원 참여여부 | Yes only when the principal investigator is designated as an NHIS big data research expert (빅데이터 연구 전문위원) |
| Research type | 연구유형 | Policy research, academic research, thesis, joint research, scientific research, or other research (기타연구). The next table describes each type except other research, which the guide does not describe. |
| Special research | 특수연구구분 | General (일반), or COVID-19 (코로나) for the COVID-19 database |
| Requests and other notes | 요청사항/기타 | Free text of up to 4,000 bytes. Customized DB applications must state who will extract the data, the preferred extraction site (Wonju or Seoul), and whether that person has extracted NHIS data before. |
| Linkage with other institutions | 타기관 연계여부 | Customized DB policy research only, with a clear legal basis and a phone consultation before applying |

The research type determines the documents to attach.

| Research type | 한글 | Purpose and required documents |
|---|---|---|
| Policy research | 정책연구 | A policy research report. Attach the research contract and supporting documents, and the commissioning agency must send an official letter to the NHIS before the review. |
| Academic research | 학술연구 | Journal articles. Additional use (추가활용) gives a new project number, without a new extract, to the same principal investigator for further results within the scope already approved. |
| Thesis | 학위논문 | A thesis or dissertation. Attach a certificate of enrollment issued within three months of the application. |
| Joint research | 공동연구 | Research under an agreement with the NHIS, such as a memorandum of understanding. An agreement signed with another NHIS department requires that department to send an official letter to the big data office (빅데이터연구개발실). |
| Scientific research | 과학적연구 | Research applying scientific methods, such as technology development and demonstration, basic and applied research, and privately funded research. Attach a scientific research use plan (과학적 연구 활용계획서). |

Since September 2025, customized DBs are provided only through researcher extraction (연구자 추출), in which the researcher builds the extract in SAS on an NHIS computer during a fixed window after approval. The title of such a project starts with `[연구자 추출]`, as in `[연구자 추출] 심방세동 환자의 후유증 분석 연구`, and this applies to additional use as well. First-time extractors must work in Wonju and attend training on the first day, while Seoul is open only to researchers who have extracted before.

## Step 2. IRB documents and period of use

The application needs the approval notice (IRB 결과통지서) from an institutional review board or from the public institutional review board (공용기관생명윤리위원회), together with the research protocol (IRB 연구계획서) submitted to that board. The notice must carry the seal of the issuing institution or the signature of its head, and an application whose documents cannot be verified is returned. The protocol should be in Korean, since an application with an English protocol has been rejected.

The period of data use is set on the same screen and can be reset when the fee notice is issued. The analysis tool is chosen here for a sample database and after approval for a customized DB.

The title, the principal investigator, and the study on the portal must match the IRB documents. Writing the research summary before the IRB protocol therefore saves a second round of edits, because the protocol can reuse the same text.

## Step 3. Research summary

The research summary (연구과제요약서) is the text the data provision review committee reads, since the summary entered on the portal is placed on the committee agenda as written. It is written in Korean, and the guide asks for detailed prose and names three kinds of summaries that are sent back for revision.

- A list of variables or diagnosis codes from which the study cannot be understood
- A summary without a clear theoretical basis for the planned research
- An outline-style summary that needs further explanation

The summary has the fields below. Free-text fields are limited in bytes, as explained after the table.

| Field | 한글 | Limit | What the NHIS asks for |
|---|---|---|---|
| Research type | 연구타입 | Checkbox | Drug research (약제연구) or medical device research (치료재료연구), each opening its own plan. Drug research is required for the prescription table (T60). |
| Title | 연구명 | 500 characters | The same title as on the IRB approval notice and protocol, with `[연구자 추출]` in front for customized DBs |
| Requested years | 요청년도 | Menu | The years of data requested, which must match the years chosen in step 5. The 2024 guide allowed years up to 2023, and the 2026 request form allows years up to 2024. |
| Requested data | 요청자료 | Buttons | Eligibility (자격DB), claims (진료DB), screening (검진DB), providers (요양기관DB), death (사망DB), and other (기타). The cause-of-death database (통계청사망원인DB) and any additional table, such as the cancer screening DB, are written under other. |
| Research topic | 연구주제(대상질환) | 4,000 bytes | The topic and the target diseases. The guide's model answer is a single line listing the diseases and the test studied. |
| Research purpose | 연구목적 | 4,000 bytes | The background of the study, its hypotheses, and what it aims to achieve |
| Study population | 자료추출을 위한 대상자 정의 | 4,000 bytes | The definition of the study population, identical to the one set on the portal or in the Excel request form, with codes and years |
| Research content | 연구내용 | 4,000 bytes | What will be done with the requested data, including the background, hypotheses, and operational definitions of the study population and variables. Policy research with linked data also describes the linked data here or under methods. |
| Research methods | 연구방법 | 4,000 bytes | The theoretical and statistical methods for testing the hypotheses with the requested data, and the reason for each additional table, written as `OO DB 요청사유` followed by the reason and the planned use |
| Expected outcomes and uses | 기대효과/활용방안 | 4,000 bytes | The expected results and how they will be used |
| Funding source | 연구비지원 출처 | 4,000 bytes | The exact source of funding, or 해당 없음 when there is none |

The portal adds three notes above these fields. The database has no income variable, and premium quantiles are offered in its place. A project that requests the cause-of-death database must also apply on the Statistics Korea website after the NHIS approval. The research content and methods should be written in detail.

The guide's model answers come from a study of claims for next-generation sequencing tests. Its research content is a numbered outline of the planned analyses, with the variables of each, and its research methods are prose paragraphs that take the analyses one at a time.

The summary must stay within what the NHIS provides, so it cannot rely on variables the database does not hold, such as income or education level. Each additional table needs its own stated reason under research methods, and listing its variables does not count as a reason.

### Byte limits

The counters under each field count bytes, not characters. A Hangul character counts as 3 bytes, and a space, digit, or Latin letter as 1, which is the same as the UTF-8 encoding. Dense Korean prose averages a little over 2 bytes per character once spaces are included, so a 4,000-byte field holds about 1,700 characters and a 2,000-byte field about 850.

Drafting the answers in a word processor and counting them before pasting avoids having to cut text on the portal. In Python, `len(text.encode("utf-8"))` gives the count. The guide does not say how line breaks are counted, so it is safer to leave a margin of a hundred bytes or so.

## Drug research plan

A request for prescription details (T60) requires a drug research plan (약제연구 활용계획서) and a drug list in the NHIS template (약제목록 서식). The template and an example of how to fill it in are downloaded from the drug list guide button (약제목록 작성 안내) at the bottom of the plan. A file that does not follow the template cannot be uploaded, and drugs missing from the plan or the list are not provided.

The NHIS asks for only the drugs related to the topic, requested at the coarsest level the study allows, such as groups or the first four digits of the ingredient code. A project that does not request T60 must untick the table in step 5.

The plan opens with screening questions about single-listed drugs (단독등재 약제), meaning ingredients with a single supplier at the level of the first four digits of the ingredient code. Each answer sends the applicant to a different item.

| Item | Question | If yes | If no |
|---|---|---|---|
| 1 | Does the request include single-listed drugs? | 2-1 | 3-3 |
| 2-1 | Are single-listed drugs to be grouped so that no single company's information is exposed? | 3-3 | 3-1 |
| 3-1 | Do single-listed drugs affect the analysis of results, because they are used to analyze effectiveness or safety? | 3-2 | 3-3 |
| 3-2 | Can a summary of a prior meta-analysis of the requested single-listed drugs be submitted? | 3-3 | 3-3 |

Grouping means requesting a single-listed drug together with other ingredient codes so that every group has at least two suppliers. For item 3-1, the form explains that the answer is yes when the drug is an independent variable that affects the outcome and no when the drug only defines the study population or covariates. The template for the meta-analysis summary is posted on the portal notice board (고객지원, 공지사항, 논문 요약서 서식).

Item 3-3 consists of four text fields, two of which have half the usual limit.

| Field | 한글 | Limit | Required content |
|---|---|---|---|
| Drug status | 약제현황 | 4,000 bytes | The requested drugs and the reason for each, at least by therapeutic class, described in general terms rather than as a list of ingredient codes |
| Other information | 기타사항 | 4,000 bytes | The request unit, by default the first four digits of the ingredient code or a grouping proposed by the researcher, with a reason for five digits or more, and whether single-listed products fall within it |
| Research scope | 연구범위 | 2,000 bytes | The background, hypotheses, and scope of the drug research |
| Analysis and use plan | 분석 및 활용계획 | 2,000 bytes | How each drug will be used (as a covariate, to define a disease, to select the study population, or to analyze effectiveness), and whether and at what level (class, group, or ingredient) drugs will be compared in their association with outcomes |

A study that does not compare drugs in their association with outcomes says so in the analysis and use plan with a fixed sentence, 약제와 결과변수와의 연관성 비교분석을 시행하지 않는다. The plan for medical device research (치료재료연구 활용계획서) follows a similar format and is not covered here.

## Step 4. Researchers

The principal investigator must be a Korean national living in Korea and must be the person named as principal investigator on the IRB approval notice. For a thesis, the student registers as principal investigator, and the advisor named on the IRB notice registers as co-investigator. Every researcher added to the project needs an account on the portal.

## Step 6. Identity verification and submission

The application is not submitted until every registered researcher verifies their identity by both mobile phone and email, and the verification must be repeated for each application. The application is submitted automatically when the last researcher finishes, and its status changes to awaiting receipt (접수대기).

When NHIS staff receive the application, the status changes to awaiting review (검토대기). If anything must be supplemented before the review, the status becomes supplement requested (보완요청), and the applicant revises the application from the project list (나의과제) and submits it again. For customized DBs under researcher extraction, the review committee meets twice a month, and an approved application changes to awaiting construction (자료구축대기). What follows approval, from connecting to the data to exporting results, is described on the [Using the data](using.md) page.
