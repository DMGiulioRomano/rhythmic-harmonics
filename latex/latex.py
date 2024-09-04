import os
import argparse
import sys
import configparser
# Add the path to the pyLib directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pyLib')))
from markdown_utils import read_markdown_file, filter_comments, parse_line, Voce

# ---------------------------------------------------------------
# Define default values
layoutTempColor = {0: 'black', 1: 'red', 2: 'green', 3: 'violet'}
input_markdown = "../input.md"
# ---------------------------------------------------------------



def load_config(config_file):
    global layoutTempColor, input_markdown

    config = configparser.ConfigParser()
    config.read(config_file)

    # Load layout colors
    layout_color_str = config.get('Latex', 'layoutTempColor', fallback='')
    layoutTempColor = {int(k): v for k, v in (item.split(':') for item in layout_color_str.split(', '))} if layout_color_str else layoutTempColor
    
    # Load input markdown file
    input_markdown = config.get('Latex', 'input_markdown', fallback='../input.md')



class Block:
    def __init__(self):
        self.colors = []  # List of Voce objects, each representing a color
    
    def add_voce(self, voce):
        self.colors.append(voce)  # Add a Voce to the list

    def get_voce_by_color(self, color):
        # Find and return the Voce object that matches the color
        for voce in self.colors:
            if voce.color == color:
                return voce
        return None
    
    def merge(self, other_block):
        # Create a new block to hold the merged results
        merged_block = Block()
        # Copy all the Voce instances from the current block
        for voce in self.colors:
            merged_block.add_voce(voce)
        # Merge all Voce instances from the other block
        for voce in other_block.colors:
            existing_voce = merged_block.get_voce_by_color(voce.color)
            if existing_voce:
                existing_voce.punti.extend(voce.punti)
            else:
                merged_block.add_voce(voce)
        return merged_block
    

class Point:
    def __init__(self, first, second, third, color):
        self.first = first
        self.second = second
        self.third = third
        self.color = color

def write_max_first_to_md(max_first_value, filename="temp_max_first.md"):
    """Write the maximum 'first' value to a temporary Markdown file."""
    with open(filename, 'w') as file:
        file.write(f"{max_first_value + 1}\n")
    print(f"Temporary Markdown file '{filename}' created with max_first_value: {max_first_value}")

def create_point(first, second, third, additional_value):
    """Create a Point instance and return it."""
    color = layoutTempColor.get(additional_value, 'red')
    return Point(first, second, third, color)


def process_markdown_block(input_file, output_dir):

    blocks = []  # List of Block objects
    max_first_value = 1  # To track the maximum 'first' value
    # Read the file and process points
    
    lines = read_markdown_file(input_file)
    lines = filter_comments(lines)

    for line in lines:
        result = parse_line(line)
        if result:
            first, second, third, additional_value = result
            point = create_point(first, second, third, additional_value)

            # Find or create the corresponding block
            while len(blocks) <= first:
                blocks.append(Block())
            current_block = blocks[first]
            
            # Find or create the Voce for the color
            voce = current_block.get_voce_by_color(point.color)
            if not voce:
                voce = Voce(point.color)
                current_block.add_voce(voce)
            
            voce.add_point(point)

        # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)


    # Write each pair of blocks to a separate file
    num_blocks = len(blocks)
    for i in range(0, num_blocks,2):
        output_file = os.path.join(output_dir, f'fragment_{i // 2}.tex')
        with open(output_file, 'w') as tex_file:
            # Process the first block in the pair
                # Merge the first and second block in the pair
            if i < num_blocks:
                block1 = blocks[i]
                block2 = blocks[i + 1] if i + 1 < num_blocks else Block()
                merged_block = block1.merge(block2)
                for voce in merged_block.colors:
                    for point in voce.punti:
                        tex_file.write(f"\\fill[{point.color}] (point-{point.first % 2}-{point.second}-{point.third}) circle (2pt);\n")
                        tex_file.write(f"\\draw[thick] (point-{point.first % 2}-{point.second}-{point.third}) circle [radius=0.3cm]; % Circle around node point-{point.first}-{point.second}-{point.third}\n")
                    # Draw arrows between consecutive points of the same color
                    for j in range(len(voce.punti) - 1):
                        p1, p2 = voce.punti[j], voce.punti[j + 1]
                        tex_file.write(f"\\draw[->, thick, color={p1.color}, line width=1px] (point-{p1.first % 2}-{p1.second}-{p1.third}) -- (point-{p2.first % 2}-{p2.second}-{p2.third});\n")
                tex_file.write(f"\n")

    # Write the Markdown file with the actual max_first_value found
    write_max_first_to_md(max_first_value)





def process_markdown_color(input_file, output_file):
    color_lists = []  # List of lists to hold points by color
    max_color_value = 0  # To track the maximum value of additional_value
    max_first_value = 0  # To track the maximum 'first' value

    # Read and filter comments from the file
    lines = read_markdown_file(input_file)
    lines = filter_comments(lines)
    
    # First pass: Determine max values and prepare color lists
    for line in lines:
        result = parse_line(line)
        if result:
            first, second, third, additional_value = result
            max_first_value = max(max_first_value, first)
            max_color_value = max(max_color_value, additional_value)
            
            # Ensure color_lists has enough space for the new color
            while len(color_lists) <= additional_value:
                color_lists.append([])
            
            # Create a Point instance and store it in the appropriate color list
            point = create_point(first, second, third, additional_value)
            color_lists[additional_value].append(point)
    
    # Write the points to the LaTeX file
    try:
        with open(output_file, 'w') as tex_file:
            # Process each color index
            for color_index, points in enumerate(color_lists):
                for point in points:
                    tex_file.write(f"\\fill[{point.color}] (point-{point.first}-{point.second}-{point.third}) circle (2pt);\n")
                    tex_file.write(f"\\draw[thick] (point-{point.first}-{point.second}-{point.third}) circle [radius=0.3cm]; % Circle around node point-{point.first}-{point.second}-{point.third}\n")
                
                # Draw arrows between consecutive points of the same color
                for i in range(len(points) - 1):
                    p1, p2 = points[i], points[i + 1]
                    tex_file.write(f"\\draw[->, thick, color={p1.color}, line width=1px] (point-{p1.first}-{p1.second}-{p1.third}) -- (point-{p2.first}-{p2.second}-{p2.third});\n")
                tex_file.write(f"\n")
    except Exception as e:
        print(f"Error while writing file {output_file}: {e}")

    # Write the Markdown file with the actual max_first_value found
    write_max_first_to_md(max_first_value)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process markdown to LaTeX")
    parser.add_argument('--fragments', action='store_true', help="Process fragments")
    parser.add_argument('--no-fragments', action='store_false', dest='fragments', help="Process color only")
    parser.add_argument('--output', type=str, default="unique.tex", help="Boolean to decide file name")
    args = parser.parse_args()

    config_file = '../config.ini'  # Name of the config file
    # Load the configuration
    load_config(config_file)
    output_dir = "fragments"        # Directory per l'output nel caso del blocco
      # Nome del file di output nel caso del colore

    if args.fragments:
        process_markdown_block(input_markdown, output_dir)
    else:
        process_markdown_color(input_markdown, args.output)


