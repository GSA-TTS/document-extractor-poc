# Document Extractor

This document uses [`threatdown`](https://threatdown.xyz) to help create the final document.

Run `npx threatdown ./THREAT_MODEL.template.md --output ./THREAT_MODEL.md` to create it.  Don't forget to run this
command and commit the final document.

Do not edit `THREAT_MODEL.md` directly.

## Introduction

The threat model is intended to ensure that the application is developed with security built-in from the beginning and
in an ongoing way.  By documenting potential threats and assets, along with countermeasures and mitigation actions
explicitly, better and more informed decisions can be made for improved security.

This document is stored in revision control along with the application code so that it is highly visible and accessible
to the individuals doing development and deployment and can be modified in concert with the code.

## Entry Points

1. Website.  Users interact with our application through the website.  Anyone can interact with the website.
2. API.  Users can interact with the API through the website or directly.
3. AWS console.  AWS credentials can be used to log into the AWS console directly and access data, code, and
   configuration.
4. S3 bucket document bucket.  The S3 bucket stores the documents and is written to by the application.

## Assets

1. The code itself.
2. The website.
3. Documents uploaded to the application.
4. The extracted data from the documents.

## Threats

<!-- ```threatdown
__Make the application unavailable__
- Harness a botnet and throw a bunch of traffic at the website or API.
  - [x] AWS has built-in DDOS mitigations.
  - [ ] Pay for AWS Shield Advaced that provides additional protections.
- Change the code to become inoperable.
  - Have access to GitHub.
    - [x] GSA requires a user have a GSA e-mail, which requires a background check.
    - [x] GitHub accounts in the GSA GitHub organization requires two-factor authentication.
    - [x] main branch is protected and requires a code review approval from another person before code is accepted.
  - Have access to AWS to change code or other configuration.
    - [x] Protected by two-factor authentication and only specific individuals are given access.
- Suppy chain attack to make the larger application inoperable.
  - [x] We use well known dependencies distributed through well known distribution channels like PyPi and NPM.
  - [ ] Improve dependabot to automatically update dependencies.
  - [ ] Do SCA scanning.
``` -->
```mermaid
flowchart TD
  A0{Make the application unavailable}:::objective
    A0---B1(((OR))):::booleanOr
      B1---C1(Harness a botnet and throw a bunch of traffic at the website or API.):::condition
        C1---D1(((OR))):::booleanOr
          D1-- mitigated by ---E1(AWS has built-in DDOS mitigations.):::condition
          D1-. mitigated by .-E2(Pay for AWS Shield Advaced that provides additional protections.):::condition
      B1---C2(Change the code to become inoperable.):::condition
        C2---D2(((OR))):::booleanOr
          D2---E3(Have access to GitHub.):::condition
            E3---F1(((OR))):::booleanOr
              F1-- mitigated by ---G1(GSA requires a user have a GSA e-mail, which requires a background check.):::condition
              F1-- mitigated by ---G2(GitHub accounts in the GSA GitHub organization requires two-factor authentication.):::condition
              F1-- mitigated by ---G3(main branch is protected and requires a code review approval from another person before code is accepted.):::condition
          D2---E4(Have access to AWS to change code or other configuration.):::condition
            E4-- mitigated by ---F2(Protected by two-factor authentication and only specific individuals are given access.):::condition
      B1---C3(Suppy chain attack to make the larger application inoperable.):::condition
        C3---D3(((OR))):::booleanOr
          D3-- mitigated by ---E5(We use well known dependencies distributed through well known distribution channels like PyPi and NPM.):::condition
          D3-. mitigated by .-E6(Improve dependabot to automatically update dependencies.):::condition
          D3-. mitigated by .-E7(Do SCA scanning.):::condition
  classDef objective fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef condition fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef assumption fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef booleanAnd fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  classDef booleanOr fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  style E1 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E2 stroke:#4a3dff,stroke-width:2px
  style G1 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style G2 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style G3 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style F2 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E5 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E6 stroke:#4a3dff,stroke-width:2px
  style E7 stroke:#4a3dff,stroke-width:2px
  linkStyle 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18 stroke:#4a3dff,stroke-width:2px
```


<!-- ```threatdown
__Steal the raw, uploaded documents__
- Access the S3 bucket.
  - Have access to AWS.
    - [x] Protected by two-factor authentication and only specific individuals are given access.
  - [x] Public access is completely disabled on the bucket.
  - [x] Set a lifecycle policy to delete documents after a period of time.
- Change the code to exfiltrate the raw document.
  - Have access to GitHub.
    - [x] GSA requires a user have a GSA e-mail, which requires a background check.
    - [x] GitHub accounts in the GSA GitHub organization requires two-factor authentication.
    - [x] main branch is protected and requires a code review approval from another person before code is accepted.
- Suppy chain attack to exfiltrate the raw document.
  - [x] We use well known dependencies distributed through well known distribution channels like PyPi and NPM.
  - [ ] Improve dependabot to automatically update dependencies.
  - [ ] Do SCA scanning.
- Set a UUID in the frontend or call the API with UUID to get an S3 pre-signed URL.
  - [x] UUIDs are hard to guess because the range of values is so large
    > This is not good enough at all.  Someone could brute force the numbers and eventually encounter a document which will be devastating.  This must be fixed before real data is used.
  - [ ] Add AuthN/AuthZ so only allowed people are able to call the API with a UUID associated with them.
  - [ ] Add API trottling to slow down the brute force checking of a bunch of UUIDs.
``` -->
```mermaid
flowchart TD
  A0{Steal the raw, uploaded documents}:::objective
    A0---B1(((OR))):::booleanOr
      B1---C1(Access the S3 bucket.):::condition
        C1---D1(((OR))):::booleanOr
          D1---E1(Have access to AWS.):::condition
            E1-- mitigated by ---F1(Protected by two-factor authentication and only specific individuals are given access.):::condition
          D1-- mitigated by ---E2(Public access is completely disabled on the bucket.):::condition
          D1-- mitigated by ---E3(Set a lifecycle policy to delete documents after a period of time.):::condition
      B1---C2(Change the code to exfiltrate the raw document.):::condition
        C2---D2(Have access to GitHub.):::condition
          D2---E4(((OR))):::booleanOr
            E4-- mitigated by ---F2(GSA requires a user have a GSA e-mail, which requires a background check.):::condition
            E4-- mitigated by ---F3(GitHub accounts in the GSA GitHub organization requires two-factor authentication.):::condition
            E4-- mitigated by ---F4(main branch is protected and requires a code review approval from another person before code is accepted.):::condition
      B1---C3(Suppy chain attack to exfiltrate the raw document.):::condition
        C3---D3(((OR))):::booleanOr
          D3-- mitigated by ---E5(We use well known dependencies distributed through well known distribution channels like PyPi and NPM.):::condition
          D3-. mitigated by .-E6(Improve dependabot to automatically update dependencies.):::condition
          D3-. mitigated by .-E7(Do SCA scanning.):::condition
      B1---C4(Set a UUID in the frontend or call the API with UUID to get an S3 pre-signed URL.):::condition
        C4---D4(((OR))):::booleanOr
          D4-- mitigated by ---E8(UUIDs are hard to guess because the range of values is so large):::condition
          D4-. mitigated by .-E9(Add AuthN/AuthZ so only allowed people are able to call the API with a UUID associated with them.):::condition
          D4-. mitigated by .-E10(Add API trottling to slow down the brute force checking of a bunch of UUIDs.):::condition
  classDef objective fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef condition fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef assumption fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef booleanAnd fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  classDef booleanOr fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  style F1 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E2 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E3 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style F2 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style F3 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style F4 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E5 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E6 stroke:#4a3dff,stroke-width:2px
  style E7 stroke:#4a3dff,stroke-width:2px
  style E8 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E9 stroke:#4a3dff,stroke-width:2px
  style E10 stroke:#4a3dff,stroke-width:2px
  linkStyle 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22 stroke:#4a3dff,stroke-width:2px
```


<!-- ```threatdown
__Steal the extracted data__
- Access the DynamoDB table.
  - Have access to AWS.
    - [x] Protected by two-factor authentication and only specific individuals are given access.
- Change the code to exfiltrate the extracted data.
  - Have access to GitHub.
    - [x] GSA requires a user have a GSA e-mail, which requires a background check.
    - [x] GitHub accounts in the GSA GitHub organization requires two-factor authentication.
    - [x] main branch is protected and requires a code review approval from another person before code is accepted.
- Suppy chain attack to exfiltrate the extracted data.
  - [x] We use well known dependencies distributed through well known distribution channels like PyPi and NPM.
  - [ ] Improve dependabot to automatically update dependencies.
  - [ ] Do SCA scanning.
- Set a UUID in the frontend or call the API with UUID to get the extracted data.
  - [x] UUIDs are hard to guess because the range of values is so large
    > This is not good enough at all.  Someone could brute force the numbers and eventually encounter a document which will be devastating.  This must be fixed before real data is used.
  - [ ] Add AuthN/AuthZ so only allowed people are able to call the API with a UUID associated with them.
  - [ ] Add API trottling to slow down the brute force checking of a bunch of UUIDs.
``` -->
```mermaid
flowchart TD
  A0{Steal the extracted data}:::objective
    A0---B1(((OR))):::booleanOr
      B1---C1(Access the DynamoDB table.):::condition
        C1---D1(Have access to AWS.):::condition
          D1-- mitigated by ---E1(Protected by two-factor authentication and only specific individuals are given access.):::condition
      B1---C2(Change the code to exfiltrate the extracted data.):::condition
        C2---D2(Have access to GitHub.):::condition
          D2---E2(((OR))):::booleanOr
            E2-- mitigated by ---F1(GSA requires a user have a GSA e-mail, which requires a background check.):::condition
            E2-- mitigated by ---F2(GitHub accounts in the GSA GitHub organization requires two-factor authentication.):::condition
            E2-- mitigated by ---F3(main branch is protected and requires a code review approval from another person before code is accepted.):::condition
      B1---C3(Suppy chain attack to exfiltrate the extracted data.):::condition
        C3---D3(((OR))):::booleanOr
          D3-- mitigated by ---E3(We use well known dependencies distributed through well known distribution channels like PyPi and NPM.):::condition
          D3-. mitigated by .-E4(Improve dependabot to automatically update dependencies.):::condition
          D3-. mitigated by .-E5(Do SCA scanning.):::condition
      B1---C4(Set a UUID in the frontend or call the API with UUID to get the extracted data.):::condition
        C4---D4(((OR))):::booleanOr
          D4-- mitigated by ---E6(UUIDs are hard to guess because the range of values is so large):::condition
          D4-. mitigated by .-E7(Add AuthN/AuthZ so only allowed people are able to call the API with a UUID associated with them.):::condition
          D4-. mitigated by .-E8(Add API trottling to slow down the brute force checking of a bunch of UUIDs.):::condition
  classDef objective fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef condition fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef assumption fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef booleanAnd fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  classDef booleanOr fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  style E1 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style F1 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style F2 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style F3 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E3 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E4 stroke:#4a3dff,stroke-width:2px
  style E5 stroke:#4a3dff,stroke-width:2px
  style E6 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E7 stroke:#4a3dff,stroke-width:2px
  style E8 stroke:#4a3dff,stroke-width:2px
  linkStyle 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19 stroke:#4a3dff,stroke-width:2px
```


<!-- ```threatdown
__Vandalize the website__
- Access the S3 bucket.
- Change the code to vandalize the website.
  - Have access to GitHub.
    - [x] GSA requires a user have a GSA e-mail, which requires a background check.
    - [x] GitHub accounts in the GSA GitHub organization requires two-factor authentication.
    - [x] main branch is protected and requires a code review approval from another person before code is accepted.
- Suppy chain attack to vandalize the resulting website.
  - [x] We use well known dependencies distributed through well known distribution channels like PyPi and NPM.
  - [ ] Improve dependabot to automatically update dependencies.
  - [ ] Do SCA scanning.
``` -->
```mermaid
flowchart TD
  A0{Vandalize the website}:::objective
    A0---B1(((OR))):::booleanOr
      B1---C1(Access the S3 bucket.):::condition
      B1---C2(Change the code to vandalize the website.):::condition
        C2---D1(Have access to GitHub.):::condition
          D1---E1(((OR))):::booleanOr
            E1-- mitigated by ---F1(GSA requires a user have a GSA e-mail, which requires a background check.):::condition
            E1-- mitigated by ---F2(GitHub accounts in the GSA GitHub organization requires two-factor authentication.):::condition
            E1-- mitigated by ---F3(main branch is protected and requires a code review approval from another person before code is accepted.):::condition
      B1---C3(Suppy chain attack to vandalize the resulting website.):::condition
        C3---D2(((OR))):::booleanOr
          D2-- mitigated by ---E2(We use well known dependencies distributed through well known distribution channels like PyPi and NPM.):::condition
          D2-. mitigated by .-E3(Improve dependabot to automatically update dependencies.):::condition
          D2-. mitigated by .-E4(Do SCA scanning.):::condition
  classDef objective fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef condition fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef assumption fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  classDef booleanAnd fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  classDef booleanOr fill:#4a3dff,color:#ffffff,stroke:#ffffff,stroke-width:2px
  style F1 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style F2 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style F3 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E2 stroke:#4a3dff,stroke-width:2px,fill:#0c0b0e,color:#ffffff,stroke:#3e3b4e,stroke-width:2px
  style E3 stroke:#4a3dff,stroke-width:2px
  style E4 stroke:#4a3dff,stroke-width:2px
  linkStyle 0,1,2,3,4,5,6,7,8,9,10,11,12 stroke:#4a3dff,stroke-width:2px
```
