ews.html : ews.org ews30setup.tex ews30setup.el
	echo yes | HOME=$(realpath .) emacs -l $(realpath ews30setup.el) $(realpath $<) -e org-html-export-to-html -e kill-emacs

ews.pdf : ews.tex ews30setup.tex
	pdflatex -shell-escape $<
	while grep "LaTeX Warning: Label(s) may have changed" ews.log; do pdflatex -shell-escape $<; done

ews.tex : ews.org ews30setup.tex ews30setup.el
	echo yes | HOME=$(realpath .) emacs -l $(realpath ews30setup.el) $(realpath $<) -e org-latex-export-to-latex -e kill-emacs

ews30.pdf : ews30.tex ews30setup.tex logo-cover.png
	pdflatex -shell-escape ews30

logo-cover.png:
	cp ../Quelldateien/Gertrud_Wenzel/Dragons_original_EWS_Logo.png $@
