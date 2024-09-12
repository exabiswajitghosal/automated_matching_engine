import shutil
import xml.etree.ElementTree as ET
import os
import csv
import io

def simplify_xml_attributes(filename,filetype):
    output_dir = f'data/{filetype}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Load and parse the XML file
    input_file = f'./uploads/{filetype}/{filename}'
    output_file = f'{output_dir}/{filename}'
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Iterate through each Attribute and remove unnecessary elements
    for attribute in root.findall('.//Attribute'):
        for elem in list(attribute):
            if elem.tag not in ['Name', 'DataType', 'PrimaryKey', 'ForeignKey']:
                attribute.remove(elem)

    # Write the modified XML back to a file
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)


def merge_xml_files_to_string():
    input_folder = './data/source'
    # Get a list of all XML files in the directory
    xml_files = [f for f in os.listdir(input_folder) if f.endswith('.xml')]

    if not xml_files:
        return "No XML files found in the folder."

    # Initialize an empty string to store the merged content
    merged_content = '<?xml version="1.0"?>\n'

    # Loop over the files and read their content line by line
    for xml_file in xml_files:
        file_path = os.path.join(input_folder, xml_file)
        with open(file_path, 'r', encoding='utf-8') as file:
            # Append file content to the merged_content string
            for line in file:
                merged_content += line.strip() + '\n'

    return merged_content



def save_response_to_csv(response_text,file_name):
    output_dir = 'data/output'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    filename = f'{output_dir}/{file_name}_comparison_report.csv'
    # Use io.StringIO to simulate a file object
    csv_data = io.StringIO(response_text)

    # Read the CSV data from the string
    reader = csv.reader(csv_data)

    # Open a file for writing
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write each row from the CSV data to the file
        for row in reader:
            writer.writerow(row)

def read_previous_file():
    # Directory containing the files
    directory = './data/previous_file/'

    # Initialize a variable to store the response text
    previous_data = ""

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if the file is a CSV file
        if filename.endswith('.csv'):
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)

                for row in reader:
                    previous_data += ','.join(row) + "\n"
    return previous_data

def read_target_data():
    # Directory containing the files
    directory = './data/target/'

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if the file is an XML file
        if filename.endswith('.xml'):
            with open(file_path, 'r') as file:
                target_data = file.read().strip()
    return target_data