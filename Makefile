# Directory variables
DIR_CS=csound
DIR_TEX=latex
DIR_WAV=outputWav
DIR_EXPORT=export

# Python script names for LaTeX and Csound
PYSCRIPT_TEX=latex.py
PYSCRIPT_CSOUND=csound.py

# Input and output file names
INPUT=input.md
OUTPUT_TEX=parte.tex
OUTPUT_SCO=eventi.sco
MAIN_TEX=armonicheRitmicheLayout.tex
OUTPUT_PDF=armonicheRitmicheLayout.pdf
OUTPUT_SVG=armonicheRitmicheLayout.svg

# Default rule to build everything
all: csound latex


# Rule to create necessary directories
create_dirs:
	@mkdir -p $(DIR_TEX)/$(DIR_EXPORT) $(DIR_CS)/$(DIR_WAV)



#-----------------------------------

latex: create_dirs latexpy pdf

# Rule to run the LaTeX Python script
latexpy:  
	cd $(DIR_TEX) && python3 $(PYSCRIPT_TEX)

# Rule to generate the PDF
pdf: 
	cd $(DIR_TEX) && pdflatex -output-directory=$(DIR_EXPORT) $(MAIN_TEX)

#-----------------------------------




#-----------------------------------

csound: create_dirs csoundpy outputWav

# Rule to generate the Csound file
csoundpy:
	cd $(DIR_CS) && python3 $(PYSCRIPT_CSOUND)

outputWav: 
	cd $(DIR_CS) && csound -o $(DIR_WAV)/output.wav orc.orc $(OUTPUT_SCO)
#-----------------------------------





# Rule to convert the PDF to SVG
print: pdf
	pdflatex -output-directory=$(DIR_EXPORT) $(MAIN_TEX)
	pdf2svg $(DIR_EXPORT)/$(OUTPUT_PDF) $(DIR_EXPORT)/$(OUTPUT_SVG)







# Clean up generated files
clean:
	rm -rf $(DIR_TEX)/$(OUTPUT_TEX) $(DIR_TEX)/$(DIR_EXPORT) $(DIR_TEX)/$(DIR_EXPORT)/$(OUTPUT_SVG) $(DIR_CS)/$(OUTPUT_SCO) *.aux *.log *.out

.PHONY: all pdf csound print clean
