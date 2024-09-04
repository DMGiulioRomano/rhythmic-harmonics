include makeLib/Makefile.lib

# Default rule to build everything
all: config_env csound latex

# Rule to create necessary directories
create_dirs:
	@mkdir -p $(DIR_TEX)/$(DIR_EXPORT) $(DIR_TEX)/$(DIR_INPUT_TEX) $(DIR_CS)/$(DIR_WAV)


ifeq ($(FRAGS), True)
latex: texTrueFrags
else
latex: texFalseFrags
endif

#-----------------------------------
ifeq ($(POLY), False)
texTrueFrags: create_dirs latexpyTrue compile_fragments combine_pdfs
else 
texTrueFrags: create_dirs #has yet to be implemented
endif
# Rule to run the LaTeX Python script

sortInputFile:
	cd $(DIR_PY_MANIP) && python3 sortingPoints.py

latexpyTrue:
	cd $(DIR_TEX) && python3 $(PYSCRIPT_TEX) --fragments

compile_fragments: create_dirs
	rm -rf $(DIR_TEX)/$(DIR_EXPORT)/*.pdf
	@NUMBER=$(shell awk 'NR==1 {print $$0}' $(DIR_TEX)/$(TEMP_FILE)) && \
	python3 $(DIR_PY_MANIP)/replaceLine.py $(DIR_TEX)/$(MAIN_TEX) 11 "\\def\\makeval{$$NUMBER}"
	for file in $(DIR_TEX)/$(DIR_INPUT_TEX)/*.tex; do \
		touch $(DIR_TEX)/$(FRAGMENT); \
		filename=$$(basename $$file .tex); \
		echo "\input{$(DIR_INPUT_TEX)/$$filename}" > $(DIR_TEX)/$(FRAGMENT); \
		cd $(DIR_TEX) && pdflatex -output-directory=$(DIR_EXPORT) -jobname=$$filename $(MAIN_TEX); \
		cd ..; \
	done
	rm $(DIR_TEX)/$(TEMP_FILE) $(DIR_TEX)/$(FRAGMENT)
	rm $(DIR_TEX)/$(DIR_EXPORT)/*.log $(DIR_TEX)/$(DIR_EXPORT)/*.aux

combine_pdfs: config_env
	chmod +x makeLib/generateTex.sh
	makeLib/generateTex.sh
	cd $(DIR_TEX) && pdflatex $(TMP_TEX) -output-directory=$(DIR_TEX)/$(DIR_EXPORT)
	rm -f $(DIR_TEX)/*.aux	$(DIR_TEX)/*log
	rm -f $(DIR_TEX)/$(TMP_TEX)
#-----------------------------------

#-----------------------------------

texFalseFrags: create_dirs latexpyFalse compile_part

latexpyFalse:
	cd $(DIR_TEX) && python3 $(PYSCRIPT_TEX) --no-fragments --output "$(UNIQUE)"

compile_part: 
	@NUMBER=$(shell awk 'NR==1 {print $$0}' $(DIR_TEX)/$(TEMP_FILE)) && \
	python3 $(DIR_PY_MANIP)/replaceLine.py latex/main.tex 11 "\\def\\makeval{$$NUMBER}"
	rm -f latex/temp_max_color.md
	touch $(DIR_TEX)/$(FRAGMENT)
	echo "\input{$$(basename $(UNIQUE) .tex)}" > $(DIR_TEX)/$(FRAGMENT)
	cd $(DIR_TEX) && pdflatex -output-directory=$(DIR_EXPORT) -jobname=$$(basename $(UNIQUE) .tex) $(MAIN_TEX)
	rm $(DIR_TEX)/$(TEMP_FILE) $(DIR_TEX)/$(FRAGMENT)
	rm $(DIR_TEX)/$(DIR_EXPORT)/*.log $(DIR_TEX)/$(DIR_EXPORT)/*.aux

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
	rm -rf $(DIR_TEX)/main.tex.bak $(DIR_TEX)/$(UNIQUE) $(DIR_TEX)/$(DIR_INPUT_TEX) $(DIR_TEX)/$(DIR_EXPORT) $(DIR_TEX)/$(FRAGMENT) $(DIR_TEX)/$(TEMP_FILE) $(DIR_CS)/$(OUTPUT_SCO) $(DIR_CS)/$(DIR_WAV) rm -rf *.bak

.PHONY: all pdf csound print clean
