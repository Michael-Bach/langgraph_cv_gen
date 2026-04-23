# CV Templates and Tailoring Guide

## Template: LaTeX moderncv (Banking Style)

**Compile with:** pdflatex (not xelatex)

## Document Structure

```latex
\documentclass[11pt,a4paper,sans]{moderncv}
\moderncvstyle{banking}
\moderncvcolor{blue}

\usepackage[utf8]{inputenc}
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}
\usepackage[scale=0.77]{geometry}

\name{[FIRST_NAME]}{[LAST_NAME]}
\address{[YOUR_ADDRESS]}{}{}
\phone[mobile]{[YOUR_PHONE]}
\email{[YOUR_EMAIL]}
\extrainfo{\href{[YOUR_LINKEDIN_URL]}{LinkedIn}, \href{[YOUR_GITHUB_URL]}{GitHub}}

\begin{document}
\makecvtitle

% 1. Profile statement (tailored per role)
% 2. Core competencies / Skills
% 3. Professional Experience (reverse chronological)
% 4. Education
% 5. Publications & Awards
% 6. References

\end{document}
```

## Page Budget — Hard 2-Page Limit

| Section | Max budget |
|---------|-----------|
| Profile statement | 3-4 lines |
| Skills | 5 items, each 1-2 lines |
| Most recent role | 4-5 bullets |
| Previous role | 2-3 bullets |
| Older roles | 2 bullets |
| Education | 2-3 entries |
| Awards | 3 entries, single line each |
| References | "Available upon request." |

**If in doubt, cut rather than squeeze.**

## Profile Statement Templates

**For technical/ML roles:**
> [YOUR_PROFILE_STATEMENT_TECHNICAL]

**For domain-specific roles:**
> [YOUR_PROFILE_STATEMENT_DOMAIN]
