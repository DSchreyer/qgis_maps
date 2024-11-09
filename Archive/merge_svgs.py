#!/usr/bin/env python3

import argparse
import glob
from svgutils.compose import Figure, SVG
from svgutils.transform import SVGFigure

def merge_svgs(svg_folder, output_file):
    # Get a list of all SVG files in the folder
    svg_files = glob.glob(f"{svg_folder}/*.svg")

    # Load all SVG files into SVG objects
    svgs = [SVG(svg_file) for svg_file in svg_files]

    # Calculate the total width and height of the merged SVG
    total_width = sum(svg.width for svg in svgs)
    total_height = max(svg.height for svg in svgs)

    # Create a new SVG figure with the calculated width and height
    fig = SVGFigure(total_width, total_height)

    # Merge the SVG objects into the new figure
    for svg in svgs:
        fig.append(svg)

    # Save the merged SVG figure to the output file
    fig.save(args.output_file, encoding="utf-8")  # Set encoding to "utf-8"

    # Clear the list of SVG objects
    svgs = []
    for svg_file in svg_files:
        if svg_file.endswith('.svg'):
            svgs.append(SVG(svg_file))

    # Calculate the total width and height of the merged SVG

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge SVG files")
    parser.add_argument("svg_folder", help="Path to the folder containing SVG files")
    parser.add_argument("output_file", help="Path to the output file")
    args = parser.parse_args()

    merge_svgs(args.svg_folder, args.output_file)