
.PHONY: clean draft preview 

VERSION = 1.0-1

BIBSRC = references.bib
PKGSRC = packages.tex
TEXSRC = cloudstack.tex \
  abstract.tex \
  cpt-hardware.tex \
  cpt-install.tex \
  cpt-config.tex \
  cpt-issues.tex
GLOSRC = glossary.tex
FIGSRC = figures/cernlogo.tex \
  figures/passwd.png \
  figures/cernvm.pdf 
TIKZSRC = gnuplot-lua-tikz.tex gnuplot-lua-tikz.sty gnuplot-lua-tikz-common.tex 
TABSRC = 
SOURCES = $(TEXSRC) $(GLOSRC) $(PKGSRC) $(BIBSRC) $(TIKZSRC) $(FIGSRC) $(TABSRC)
MAINFILE = cloudstack

all: $(MAINFILE)-$(VERSION).pdf

$(MAINFILE)-$(VERSION).pdf: $(SOURCES)
	sed 's/---VERSION---/$(VERSION)/' $(MAINFILE).tex > $(MAINFILE)-tmp.tex
	pdflatex -interaction=batchmode $(MAINFILE)-tmp > /dev/null
	bibtex $(MAINFILE)-tmp | grep -i warning || true
	makeindex $(MAINFILE)-tmp.idx
	makeglossaries $(MAINFILE)-tmp
	pdflatex -interaction=batchmode $(MAINFILE)-tmp > /dev/null
	pdflatex -interaction=batchmode $(MAINFILE)-tmp | grep -i 'overful|underful' || true
	thumbpdf $(MAINFILE)-tmp
	pdflatex -interaction=batchmode $(MAINFILE)-tmp > /dev/null
	mv $(MAINFILE)-tmp.pdf $(MAINFILE)-$(VERSION).pdf

clean:
	rm -f *.aux *.log figures/*.log
	rm -f $(MAINFILE)-tmp* $(MAINFILE)*.pdf \
  $(MAINFILE)*.synctex.gz \
  $(MAINFILE)*.rai \
  $(MAINFILE)*.tpt \
  $(MAINFILE)*.aux \
  $(MAINFILE)*.bbl \
  $(MAINFILE)*.blg \
  $(MAINFILE)*.log \
  $(MAINFILE)*.out \
  $(MAINFILE)*.toc \
  $(MAINFILE)*.idx \
  $(MAINFILE)*.ind \
  $(MAINFILE)*.ilg \
  $(MAINFILE)*.glo \
  $(MAINFILE)*.ist \
  $(MAINFILE)*.glg \
  $(MAINFILE)*.gls
	
