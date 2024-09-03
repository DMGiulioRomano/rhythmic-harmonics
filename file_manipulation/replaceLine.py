import fileinput

def replace_line_in_file(filename, line_number, new_line_content):
    # Open the file in inplace mode to allow modification
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
        for current_line_number, line in enumerate(file, start=1):
            # If the current line number matches the target line number, replace the line
            if current_line_number == line_number:
                print(new_line_content)
            else:
                # Print the original line (unchanged) to the file
                print(line, end='')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Replace a specific line in a LaTeX file")
    parser.add_argument('filename', type=str, help="The LaTeX file to modify")
    parser.add_argument('line_number', type=int, help="The line number to replace")
    parser.add_argument('new_line_content', type=str, help="The new line content")

    args = parser.parse_args()

    replace_line_in_file(args.filename, args.line_number, args.new_line_content)
