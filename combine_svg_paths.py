import svgwrite
from xml.dom import minidom
import sys
import os

def combine_svg_paths(input_svg_path, output_svg_path):
    print(f"Combining paths in {input_svg_path} into {output_svg_path}")
    # Parse the input SVG file
    doc = minidom.parse(input_svg_path)
    path_strings = []

    # Extract all path elements
    for path in doc.getElementsByTagName('path'):
        d = path.getAttribute('d')
        if d:  # Only include non-empty 'd' attributes
            path_strings.append(d)

    # Combine all path data into one string
    combined_path_data = ' '.join(path_strings)

    # Get the width and height attributes from the input SVG
    svg_element = doc.getElementsByTagName('svg')[0]
    width = svg_element.getAttribute('width')
    height = svg_element.getAttribute('height')

    # Create a new SVG drawing with the same width and height
    dwg = svgwrite.Drawing(output_svg_path, size=(width, height))

    # Add the combined path to the drawing if it's not empty
    if combined_path_data.strip():
        dwg.add(dwg.path(d=combined_path_data, fill='none', stroke='black'))

    # Save the new SVG file
    dwg.save()
    print(f"Saved combined SVG to {output_svg_path}")

def process_folder(input_folder, output_folder):
    print(f"Processing folder: {input_folder}")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    for filename in os.listdir(input_folder):
        if filename.endswith('.svg'):
            input_svg_path = os.path.join(input_folder, filename)
            output_svg_path = os.path.join(output_folder, filename)
            print(f"Processing file: {filename}")
            combine_svg_paths(input_svg_path, output_svg_path)

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) != 3:
        print("Usage: python combine_svg_paths.py <input_folder> <output_folder>")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    print(f"Input folder: {input_folder}, Output folder: {output_folder}")
    process_folder(input_folder, output_folder)
    print("Processing complete.")