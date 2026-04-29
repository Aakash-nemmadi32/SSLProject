Main = report
all: $(Main).pdf
$(Main).pdf: $(Main).tex
	pdflatex $(Main)
	bibtex $(Main)
	pdflatex $(Main)
	pdflatex $(Main)
clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg