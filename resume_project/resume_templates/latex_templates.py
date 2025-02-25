tex_template_content = r"""
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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%     TITLE NAME
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\namesection{\VAR{name}}{%
\href{mailto:\VAR{email}}{\VAR{email}} | \href{tel:\VAR{phone}}{\VAR{phone}}%
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

\end{document}
"""