import svgwrite
from xml.dom import minidom

def combine_svg_paths(input_svg_path, output_svg_path):
    """
    Combine all path elements in an SVG file into a single path element.
    
    Args:
        input_svg_path (str): Path to the input SVG file.
        output_svg_path (str): Path to the output SVG file.
    """
    # Parse the input SVG file
    doc = minidom.parse(input_svg_path)
    path_strings = []

    # Extract all path elements
    for path in doc.getElementsByTagName('path'):
        d = path.getAttribute('d')
        path_strings.append(d)

    # Combine all path data into one string
    combined_path_data = ' '.join(path_strings)

    # Create a new SVG drawing
    dwg = svgwrite.Drawing(output_svg_path)

    # Add the combined path to the drawing
    dwg.add(dwg.path(d=combined_path_data, fill='none', stroke='black'))

    # Save the new SVG file
    dwg.save()

if __name__ == "__main__":
    # Example usage
    input_svg = 'input.svg'
    output_svg = 'output.svg'
    combine_svg_paths(input_svg, output_svg)