# Cover Letter Templates and Tailoring Guide

## Template: Custom cover.cls (XeLaTeX)

**Compile with:** XeLaTeX (not pdflatex)

## Document Structure

```latex
\documentclass[]{cover}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\rfoot{Page \thepage \hspace{0pt}}
\thispagestyle{empty}
\renewcommand{\headrulewidth}{0pt}
\begin{document}

\namesection{}{\Huge{[YOUR_NAME]}}{
  \href{mailto:[YOUR_EMAIL]}{[YOUR_EMAIL]} | [YOUR_PHONE] |
  \urlstyle{same}\href{[YOUR_LINKEDIN_URL]}{LinkedIn}
}

\currentdate{\today}
\lettercontent{Dear [Name/Team],}

\lettercontent{[Opening paragraph - role, connection to background, 2-3 sentences]}

\lettercontent{[Body paragraph]
\begin{itemize}
    \item [Concrete achievement/skill 1]
    \item [Concrete achievement/skill 2]
    \item [Concrete achievement/skill 3]
\end{itemize}
[Connection to company]}

\lettercontent{[Personal fit paragraph, 2-3 sentences]}

\lettercontent{I look forward to hearing from you.}

\begin{flushright}
\closing{Kind regards,\\}
\signature{[YOUR_NAME]}
\end{flushright}
\end{document}
```

## Length — Hard 1-Page Limit
- **Word budget: 250-300 words** of body text
- Language matches the job posting (en/da/other)
- No em-dashes, no clichés, forward-looking framing

## Key Commands
| Command | Purpose |
|---------|---------|
| `\namesection{}{Name}{contact}` | Header |
| `\currentdate{date}` | Date field |
| `\lettercontent{text}` | Body paragraph |
| `\closing{text}` | Closing line |
| `\signature{name}` | Printed name |
