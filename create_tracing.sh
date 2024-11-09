#!/bin/bash

# Check if input folder was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <input_folder_path>"
    exit 1
fi

# Input folder path
INPUT_FOLDER="$1"

# Output folders within the input folder
BMP_OUTPUT_FOLDER="${INPUT_FOLDER}/bmp_output"
SVG_OUTPUT_FOLDER="${INPUT_FOLDER}/svg_output"

rm "${INPUT_FOLDER}/OSM Standard.png"
rm -rf "${INPUT_FOLDER}/svg_output"
rm -rf "${INPUT_FOLDER}/bmp_output"
rm ${SVG_OUTPUT_FOLDER}/stack/layer_stack.svg

# Create output directories if they don't exist
mkdir -p "${BMP_OUTPUT_FOLDER}"
mkdir -p "${SVG_OUTPUT_FOLDER}"


# Convert all PNG files in the input directory
for png_file in ${INPUT_FOLDER}/*.png; do
    if [ -f "$png_file" ]; then
        # Extract filename without extension
        filename=$(basename -- "$png_file")
        filename="${filename%.*}"

        # Define output file paths
        bmp_file="${BMP_OUTPUT_FOLDER}/${filename}.bmp"
        svg_file="${SVG_OUTPUT_FOLDER}/${filename}.svg"

        # Convert PNG to BMP
        convert "$png_file" "$bmp_file"

        # Trace BMP to SVG with Potrace
        potrace -b svg -a 0 -t 0 "$bmp_file" -o "$svg_file"

        echo "Processed: $png_file"
    fi
done

# Generate svg stack
mkdir -p "${SVG_OUTPUT_FOLDER}/stack"
python3 /Users/daniel/Documents/Maps/Automation/merge_svgs.py ${SVG_OUTPUT_FOLDER} ${SVG_OUTPUT_FOLDER}/stack/layer_stack.svg

echo "Merged svg files."
