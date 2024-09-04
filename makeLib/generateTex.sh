#!/bin/bash

# Carica le variabili di ambiente da config.env
if [ -f makeLib/config.env ]; then
    source makeLib/config.env
else
    echo "File config.env non trovato!"
    exit 1
fi

# Variabili di input
REAL_DIR_EXPORT=$DIR_TEX/$DIR_EXPORT
TEMP_TEX_COMBINE=$DIR_TEX/$TMP_TEX

# Inizio del file LaTeX
echo "\\documentclass{article}" > $TEMP_TEX_COMBINE
echo "\\usepackage{pdfpages}" >> $TEMP_TEX_COMBINE
echo "\\usepackage[a3paper,landscape, bottom=2cm]{geometry}" >> $TEMP_TEX_COMBINE
echo "\\usepackage{fancyhdr}" >> $TEMP_TEX_COMBINE
echo "\\pagestyle{fancy}" >> $TEMP_TEX_COMBINE
echo "\\fancyhf{}" >> $TEMP_TEX_COMBINE
echo "\\fancyfoot[C]{\\thepage}" >> $TEMP_TEX_COMBINE
echo "\\renewcommand{\\headrulewidth}{0pt}" >> $TEMP_TEX_COMBINE
echo "\\renewcommand{\\footrulewidth}{0pt}" >> $TEMP_TEX_COMBINE
echo "\\begin{document}" >> $TEMP_TEX_COMBINE


# Aggiungi tutti i PDF
for pdf in $REAL_DIR_EXPORT/*.pdf; do
    echo "\\includepdf[pages=-, pagecommand={\\thispagestyle{fancy}}]{$DIR_EXPORT/$(basename "$pdf" .pdf)}" >> $TEMP_TEX_COMBINE
done

# Fine del file LaTeX
echo "\\end{document}" >> $TEMP_TEX_COMBINE
