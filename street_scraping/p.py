import re
# def clean_file(input_file_path, output_file_path):
#     # Open the input file for reading
#     with open(input_file_path, 'r') as infile:
#         # Read all lines from the file
#         lines = infile.readlines()

#     # Remove unwanted characters from each line
#     cleaned_lines = [line.strip().replace('"', '').replace(',', '') for line in lines]

#     # Open the output file for writing
#     with open(output_file_path, 'w') as outfile:
#         # Write the cleaned lines to the output file
#         for line in cleaned_lines:
#             outfile.write(line + '\n')

#     print(f"Cleaned data saved to {output_file_path}")

# # Example usage
# input_file_path = 'street_data.txt'  # Replace with your input file path
# output_file_path = 'output.txt'  # Replace with your desired output file path

# clean_file(input_file_path, output_file_path)


def combine_and_sort_files(file1, file2, output_file):
    # Read contents from both files with the specified encoding
    try:
        with open(file1, 'r', encoding='utf-8-sig') as f1, open(file2, 'r', encoding='utf-8-sig') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
    except UnicodeDecodeError:
        print("There was an issue with the encoding of the files.")
        return
    
    lines1 = [line.replace("'", "") for line in lines1]
    lines2 = [line.replace("'", "") for line in lines2]
    lines1 = [re.sub(r"[^a-zA-Z\s]", "", line.replace("'", "")) for line in lines1]
    lines2 = [re.sub(r"[^a-zA-Z\s]", "", line.replace("'", "")) for line in lines2]

    # Combine both lists and remove duplicates using a set
    combined_lines = list(set(lines1 + lines2))

    # Sort the combined lines
    combined_lines.sort()

    # Write the sorted and unique lines to the output file
    with open(output_file, 'w', encoding='utf-8-sig') as output:
        for line in combined_lines:
            output.write(line)

    print(f"Combined and sorted content saved to {output_file}")

# Example usage
file1 = 'final_streets.txt'  # Replace with your first file path
file2 = 'final_streets.txt'  # Replace with your second file path
output_file = 'final_streets2.txt'  # Replace with your desired output file path

combine_and_sort_files(file1, file2, output_file)
