; ews30setup.el
(add-to-list 'org-latex-classes
          '("memoir"
             "\\documentclass{memoir}
             [NO-DEFAULT-PACKAGES]
             [PACKAGES]
             [EXTRA]"
             ("\\chapter{%s}" . "\\chapter*{%s}")
             ("\\section{%s}" . "\\section*{%s}")
             ("\\subsection{%s}" . "\\subsection*{%s}")
             ("\\subsubsection{%s}" . "\\subsubsection*{%s}")
             ("\\paragraph{%s}" . "\\paragraph*{%s}")
             ("\\subparagraph{%s}" . "\\subparagraph*{%s}")))

(provide 'ews30setup)
