IMAGES=logo-cover.png 1w6-seitenleistenoberkante.png

all: ews.html ews.pdf

ews.html : ews.org ews30setup.tex ews30setup.el ${IMAGES}
	echo yes | HOME=$(realpath .) emacs -l $(realpath ews30setup.el) $(realpath $<) -e org-html-export-to-html -e kill-emacs

ews.pdf : ews.tex ews30setup.tex ewstitle.pdf
	pdflatex -shell-escape $<
	while grep "LaTeX Warning: Label(s) may have changed" ews.log; do pdflatex -shell-escape $<; done

ewstitle.pdf : ewstitle.tex  ${IMAGES}
	pdflatex -shell-escape $< 

ews.tex : ews.org ews30setup.tex ews30setup.el
	echo yes | HOME=$(realpath .) emacs -l $(realpath ews30setup.el) $(realpath $<) -e org-latex-export-to-latex -e kill-emacs

ews30.pdf : ews30.tex ews30setup.tex logo-cover.png
	pdflatex -shell-escape ews30

logo-cover.png:
	cp ../../Quelldateien/Gertrud_Wenzel/Dragons_original_EWS_Logo.png $@

1w6-seitenleistenoberkante.png:
	cp ../../Quelldateien/Bildentwuerfe/1w6-seitenleistenoberkante.png $@
