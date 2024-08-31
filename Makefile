# Nome del file Python per Latex
PYSCRIPT_TEX=latex.py
# Nome del file Python per Csound
PYSCRIPT_CSOUND=csound.py
# Nome del file di input markdown
INPUT=input.md
# Nome del file di output generato dallo script Python per Latex
OUTPUT_TEX=parte.tex
# Nome del file di output generato dallo script Python per Csound
OUTPUT_SCO=eventi.sco
# Nome del file TeX da compilare con pdflatex
MAIN_TEX=armonicheRitmicheLayout.tex
# Nome del file PDF finale
OUTPUT_PDF=$(basename $(MAIN_TEX)).pdf
# Nome del file PDF finale
OUTPUT_SVG=$(basename $(MAIN_TEX)).svg

# Regola principale
all: latex csound

# Target per generare il file Latex
latex: $(OUTPUT_PDF)

$(OUTPUT_TEX): $(PYSCRIPT_TEX) $(INPUT)
	python3 $(PYSCRIPT_TEX) $(INPUT)

$(OUTPUT_PDF): $(OUTPUT_TEX) $(MAIN_TEX)
	pdflatex $(MAIN_TEX)

# Target per generare il file Csound
csound: $(OUTPUT_SCO)

$(OUTPUT_SCO): $(PYSCRIPT_CSOUND) $(INPUT)
	python3 $(PYSCRIPT_CSOUND) $(INPUT)


print: 
	pdflatex $(MAIN_TEX)
	pdf2svg $(OUTPUT_PDF) $(OUTPUT_SVG)



# Pulizia dei file generati
clean:
	rm -f $(OUTPUT_TEX) $(OUTPUT_PDF) $(OUTPUT_SCO) *.aux *.log *.out

.PHONY: all latex csound clean
