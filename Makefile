# Directory variables
DIR_CS=csound
DIR_TEX=latex
DIR_WAV=outputWav
DIR_INPUT_TEX=fragments
DIR_EXPORT=export

# Python script names for LaTeX and Csound
PYSCRIPT_TEX=latex.py
PYSCRIPT_CSOUND=csound.py

# Input and output file names
INPUT=input.md
MAIN_TEX=main.tex
FRAGMENT=which_fragment.tex
UNIQUE=unique.tex
TEMP_FILE := latex/temp_max_first.md

#------
OUTPUT_SCO=eventi.sco
OUTPUT_PDF=partitura.pdf
#------ for layout
LAYOUT_TEX=layout.tex
OUTPUT_LAYOUT=layout.pdf
OUTPUT_SVG=layout.svg

# Default rule to build everything
all: csound latex


# Rule to create necessary directories
create_dirs:
	@mkdir -p $(DIR_TEX)/$(DIR_EXPORT) $(DIR_TEX)/$(DIR_INPUT_TEX) $(DIR_CS)/$(DIR_WAV)



#-----------------------------------

texTrueFrags: create_dirs latexpyTrue compile_fragments combine_pdfs
# Rule to run the LaTeX Python script
latexpyTrue:
	cd $(DIR_TEX) && python3 $(PYSCRIPT_TEX) --fragments

compile_fragments: create_dirs
	@NUMBER=$(shell awk 'NR==1 {print $$0}' $(TEMP_FILE)) && \
	python3 file_manipulation/replaceLine.py $(DIR_TEX)/$(MAIN_TEX) 11 "\\def\\makeval{$$NUMBER}"
	for file in $(DIR_TEX)/$(DIR_INPUT_TEX)/*.tex; do \
		touch $(DIR_TEX)/$(FRAGMENT); \
		filename=$$(basename $$file .tex); \
		echo "\input{$(DIR_INPUT_TEX)/$$filename}" > $(DIR_TEX)/$(FRAGMENT); \
		cd $(DIR_TEX) && pdflatex -output-directory=$(DIR_EXPORT) -jobname=$$filename $(MAIN_TEX); \
		cd ..; \
	done
	rm $(DIR_TEX)/$(DIR_EXPORT)/*.log $(DIR_TEX)/$(DIR_EXPORT)/*.aux

# Rule to combine all PDFs
combine_pdfs: 
	for file in $(DIR_TEX)/$(DIR_EXPORT)/*.pdf; do \
		pdfs+=$$file" "; \
	done; \
	pdfunite $$pdfs $(DIR_TEX)/$(DIR_EXPORT)/combined.pdf
#-----------------------------------


#-----------------------------------

texFalseFrags: create_dirs latexpyFalse compile_part

latexpyFalse:
	cd $(DIR_TEX) && python3 $(PYSCRIPT_TEX) --no-fragments --output "$(UNIQUE)"

compile_part: 
	@NUMBER=$(shell awk 'NR==1 {print $$0}' $(TEMP_FILE)) && \
	python3 file_manipulation/replaceLine.py latex/main.tex 11 "\\def\\makeval{$$NUMBER}"
	rm -f latex/temp_max_color.md
	touch $(DIR_TEX)/$(FRAGMENT)
	echo "\input{$$(basename $(UNIQUE) .tex)}" > $(DIR_TEX)/$(FRAGMENT)
	cd $(DIR_TEX) && pdflatex -output-directory=$(DIR_EXPORT) -jobname=$$(basename $(UNIQUE) .tex) $(MAIN_TEX)

#-----------------------------------



#-----------------------------------

csound: create_dirs csoundpy outputWav

# Rule to generate the Csound file
csoundpy:
	cd $(DIR_CS) && python3 $(PYSCRIPT_CSOUND)

outputWav: 
	cd $(DIR_CS) && csound -o $(DIR_WAV)/output.wav orc.orc $(OUTPUT_SCO)
#-----------------------------------











#-----------------------------------
# Rule to convert the PDF to SVG
print: create_dirs
	cd $(DIR_TEX) && pdflatex -output-directory=$(DIR_EXPORT) $(LAYOUT_TEX)
	pdf2svg $(DIR_TEX)/$(DIR_EXPORT)/$(OUTPUT_LAYOUT) $(DIR_TEX)/$(DIR_EXPORT)/$(OUTPUT_SVG)
#-----------------------------------







# Clean up generated files
clean:
	rm -rf $(DIR_TEX)/$(UNIQUE) $(DIR_TEX)/$(DIR_INPUT_TEX) $(DIR_TEX)/$(DIR_EXPORT) $(DIR_TEX)/$(FRAGMENT) $(TEMP_FILE) $(DIR_CS)/$(OUTPUT_SCO) $(DIR_CS)/$(DIR_WAV) 

.PHONY: all pdf csound print clean
