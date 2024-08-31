import re

# Function to create a list of empty lists based on the maximum number of colors
def create_color_lists(num_colors):
    return [[] for _ in range(num_colors)]

# Dictionary for color mapping
layoutTempColor = {0: 'black', 1: 'red', 2: 'green', 3: 'violet'}

class Point:
    def __init__(self, first, second, third, color):
        self.first = first
        self.second = second
        self.third = third
        self.color = color

def process_markdown(input_file, output_file):
    color_lists = []
    max_color_value = 0  # To track the maximum value of additional_value
    
    # First pass: Read the file and determine the maximum color value
    with open(input_file, 'r') as md_file:
        lines = [line.strip() for line in md_file.readlines() if line.strip()]
    
    for line in lines:
        try:
            parts = re.split(r'\s+', line, maxsplit=1)
            if len(parts) < 2:
                raise ValueError(f"Invalid format, expected two parts separated by spaces/tabs.")
            
            number_part = parts[0].strip()
            additional_value = int(parts[1].strip())
            
            # Update the maximum color value
            if additional_value > max_color_value:
                max_color_value = additional_value
                
        except ValueError as e:
            print(f"Error: {e}")
    
    # Create the appropriate number of color lists
    color_lists = create_color_lists(max_color_value + 1)
    
    # Second pass: Process the file and store points in the appropriate color list
    with open(input_file, 'r') as md_file:
        lines = [line.strip() for line in md_file.readlines() if line.strip()]
    
    for line in lines:
        try:
            parts = re.split(r'\s+', line, maxsplit=1)
            if len(parts) < 2:
                raise ValueError(f"Invalid format, expected two parts separated by spaces/tabs.")
            
            number_part = parts[0].strip()
            additional_value = int(parts[1].strip())
            
            values = number_part.split('-')
            if len(values) != 3:
                raise ValueError(f"Invalid format in the number part, expected three values separated by hyphens.")
            
            first, second, third = map(int, values)
            
            color = layoutTempColor.get(additional_value, 'red')  # Default to 'red' if not found
            
            # Create a Point instance and store it in the appropriate list
            color_lists[additional_value].append(Point(first, second, third, color))
        
        except ValueError as e:
            print(f"Error: {e}")
    
    with open(output_file, 'w') as tex_file:
        # Write the TeX commands for each point in all color lists
        for color_index, points in enumerate(color_lists):
            color = layoutTempColor.get(color_index, 'red')  # Default to 'red' if not found
            for point in points:
                tex_file.write(f"\\fill[{point.color}] (point-{point.first}-{point.second}-{point.third}) circle (2pt);\n")
                tex_file.write(f"\\draw[thick] (point-{point.first}-{point.second}-{point.third}) circle [radius=0.3cm]; % Circle around node point-{point.first}-{point.second}-{point.third}\n")
            
            # Draw arrows between consecutive points of the same color
            for i in range(len(points) - 1):
                p1, p2 = points[i], points[i + 1]
                tex_file.write(f"\\draw[->, thick, color={p1.color}, line width=1px] (point-{p1.first}-{p1.second}-{p1.third}) -- (point-{p2.first}-{p2.second}-{p2.third});\n")
            tex_file.write(f"\n")

if __name__ == "__main__":
    input_markdown = "../input.md"  # Name of the input markdown file
    output_tex = "parte.tex"     # Name of the output file
    process_markdown(input_markdown, output_tex)
