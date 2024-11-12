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

    # Calculate the translation needed to center the SVGs after scaling
    translate_x = total_width / 4
    translate_y = total_height / 4

    # Apply a 180-degree rotation and scaling transformation to the entire figure, and center it
    fig.root.set("transform", "scale(0.15, -0.15)")

    # Save the merged SVG figure to the output file
    fig.save(output_file, encoding="utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge SVG files")
    parser.add_argument("svg_folder", help="Path to the folder containing SVG files")
    parser.add_argument("output_file", help="Path to the output file")
    args = parser.parse_args()

    merge_svgs(args.svg_folder, args.output_file)