import os

def combine_and_deduplicate_txt_files(input_files, output_file):
    unique_streets = set()

    # Read each file and add streets to the set
    for file in input_files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                street = line.strip()  # Remove extra spaces and newline characters
                if street:
                    unique_streets.add(street)

    # Write unique streets to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        for street in sorted(unique_streets):  # Sort streets alphabetically
            f.write(f"{street}\n")

# Specify the input text files and the output file
input_files = [
    "streets_0-19.txt",
    "streets_20-39.txt",
    "streets_40-99.txt",
    "streets_100-199.txt",
    "streets_200-288.txt"
]
output_file = "streets_names.txt"

# Call the function
combine_and_deduplicate_txt_files(input_files, output_file)

print(f"Combined and deduplicated street names saved to '{output_file}'.")
