import re


class Voce:
    def __init__(self, color):
        self.color = color  # The color associated with this Voce
        self.punti = []     # List of points associated with this color

    def add_point(self, point):
        self.punti.append(point)  # Add a point to the list



def read_markdown_file(input_file):
    """Read the markdown file and return non-empty lines."""
    with open(input_file, 'r') as md_file:
        return [line.strip() for line in md_file.readlines() if line.strip()]


def filter_comments(lines):
    """Filter out lines that are comments (starting with '#')."""
    return [line for line in lines if not line.startswith('#')]


def parse_line(line):
    """Parse a line of the markdown file and return its components."""
    try:
        parts = re.split(r'\s+', line, maxsplit=1)
        if len(parts) < 2:
            raise ValueError("Invalid format, expected two parts separated by spaces/tabs.")
        
        number_part = parts[0].strip()
        additional_value = int(parts[1].strip())
        
        values = number_part.split('-')
        if len(values) != 3:
            raise ValueError("Invalid format in the number part, expected three values separated by hyphens.")
        
        first, second, third = map(int, values)
        return first, second, third, additional_value
    except ValueError as e:
        print(f"Error: {e}")
        return None
    