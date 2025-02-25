tex_template_content=r"""
\documentclass[]{article}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage{geometry}
\geometry{margin=1in}

% Define \namesection command for the article class
\newcommand{\namesection}[2]{%
  \begin{center}
    {\Large \textbf{#1}}\\[1ex]
    {#2}
  \end{center}
}

\pagestyle{fancy}
\fancyhf{}

\begin{document}
\sloppy  % Relax line justification (or use \raggedright for left alignment)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%     TITLE NAME
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\namesection{\VAR{name}}{%
\href{mailto:\VAR{email}}{\VAR{email}} | \href{tel:\VAR{phone}}{\VAR{phone}}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%     LINKS
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section{Links}

\noindent
LinkedIn: \href{https://linkedin.com/in/\VAR{linkedin}}{linkedin.com/in/\VAR{linkedin}} \\
Github: \href{https://github.com/\VAR{github}}{github.com/\VAR{github}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%     PROFESSIONAL SUMMARY
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section{Professional Summary}

\VAR{professional_summary}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%     SKILLS
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section{Skills}

\BLOCK{ for skill_category in skills }
\textbf{\VAR{skill_category.category}}: \VAR{skill_category.skills_list}\par
\BLOCK{ endfor }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%     WORK EXPERIENCE
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section{Work Experience}

\BLOCK{ for experience in work_experience }
\subsection*{\VAR{experience.role} at \VAR{experience.company}}
\textbf{Duration:} \VAR{experience.start_date} -- \VAR{experience.end_date}\\
\textbf{Location:} \VAR{experience.location}\\
\VAR{experience.description}\par
\BLOCK{ endfor }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%     EDUCATION
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section{Education}

\BLOCK{ for edu in education }
\subsection*{\VAR{edu.degree} at \VAR{edu.institution}}
\textbf{Duration:} \VAR{edu.start_date} -- \VAR{edu.end_date}\\
\textbf{Location:} \VAR{edu.location}\\
\VAR{edu.description}\par
\BLOCK{ endfor }

\end{document}

"""