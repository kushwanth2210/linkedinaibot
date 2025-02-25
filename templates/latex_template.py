tex_template_content = r"""
\documentclass[10pt]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[margin=0.7in]{geometry}
\usepackage{microtype}
\usepackage[usenames,dvipsnames]{color}
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=Blue,
    urlcolor=Blue
}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.2em} % reduced spacing between paragraphs

% Header command for name & contact info
\newcommand{\namesection}[1]{%
  \begin{center}
    {\LARGE \textbf{#1}}
  \end{center}
}

\begin{document}
\sloppy

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% TITLE & CONTACT INFORMATION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\namesection{\VAR{name}}
\begin{center}
{\small \href{mailto:\VAR{email}}{\VAR{email}} \textbullet\ \VAR{phone} \textbullet\ \href{https://linkedin.com/in/\VAR{linkedin}}{linkedin.com/in/\VAR{linkedin}} \textbullet\ \href{https://github.com/\VAR{github}}{github.com/\VAR{github}}}
\end{center}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% PROFESSIONAL SUMMARY
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section*{Professional Summary}
\VAR{professional_summary}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SKILLS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section*{Skills}
\BLOCK{ for skill_category in skills }
\textbf{\VAR{skill_category.category}}: \VAR{skill_category.skills_list}\par
\BLOCK{ endfor }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WORK EXPERIENCE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section*{Work Experience}
\BLOCK{ for experience in work_experience }
\subsection*{\VAR{experience.role} at \VAR{experience.company}}
\textbf{Duration:} \VAR{experience.start_date} -- \VAR{experience.end_date}\quad
\textbf{Location:} \VAR{experience.location}\\
\VAR{experience.description}\par
\BLOCK{ endfor }

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EDUCATION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section*{Education}
\BLOCK{ for edu in education }
\subsection*{\VAR{edu.degree} at \VAR{edu.institution}}
\textbf{Duration:} \VAR{edu.start_date} -- \VAR{edu.end_date}\quad
\textbf{Location:} \VAR{edu.location}\\
\VAR{edu.description}\par
\BLOCK{ endfor }

\end{document}
"""
