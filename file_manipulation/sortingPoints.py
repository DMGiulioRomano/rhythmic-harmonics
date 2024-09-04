import sys
import os
import shutil

def sort_points(input_file):
    points = []
    
    # Read the points from the input file
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                coords, color = line.split()
                x, y, z = map(int, coords.split('-'))
                points.append((x, y, z, color))

    # Sort the points based on x, then y, then z
    points.sort(key=lambda p: (p[0], p[1], p[2]))

    # Create a backup of the original file
    backup_file = input_file + '.bak'
    shutil.copy(input_file, backup_file)
    
    # Write the sorted points back to the original file
    with open(input_file, 'w') as file:
        for x, y, z, color in points:
            file.write(f"{x}-{y}-{z} {color}\n")

if __name__ == "__main__":
    input_file = "../input.md"
    sort_points(input_file)
