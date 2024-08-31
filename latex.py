def process_markdown(input_file, output_file):
    with open(input_file, 'r') as md_file:
        lines = [line.strip() for line in md_file.readlines() if line.strip()]
    
    with open(output_file, 'w') as tex_file:
        for i, line in enumerate(lines, start=1):
            try:
                values = line.split('-')
                
                if len(values) != 3:
                    raise ValueError(f"Linea {i}: Formato non valido, aspettati tre valori separati da trattini.")
                
                first, second, third = int(values[0]), int(values[1]), int(values[2])
                
                if third >= second:
                    raise ValueError(f"Linea {i}: Il terzo numero ({third}) deve essere minore del secondo ({second}).")
                
                tex_file.write(f"\\fill[red] (point-{line}) circle (2pt);\n")
                tex_file.write(f"\\draw[thick] (point-{line}) circle [radius=0.3cm]; % Cerchio attorno al nodo point-{line}\n")
                
                if i < len(lines):
                    next_value = lines[i]
                    tex_file.write(f"\\draw[->, thick, line width=1px] (point-{line}) -- (point-{next_value});\n\n")
            
            except ValueError as e:
                print(f"Errore: {e}")

if __name__ == "__main__":
    input_markdown = "input.md"  # Nome del file markdown di input
    output_tex = "parte.tex"     # Nome del file di output
    process_markdown(input_markdown, output_tex)
