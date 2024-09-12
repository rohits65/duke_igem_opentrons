import pandas as pd
from collections import defaultdict

# Load the Excel file (adjust file path and sheet name as needed)
file_path = 'plate_layout.xlsx'  # Replace with your file name
sheet_name = 'Sheet1'  # Replace with your sheet name

# Read the Excel file into a DataFrame
df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

# Initialize an empty list to store the well identifiers in the desired order
well_list = []

# Loop through each column, then each row to append to the list
for col in df.columns:
    well_list.extend(df[col].tolist())

# Print the final list to verify
#print(well_list)


# Dictionaries to store indices for templates and primers
template_indices = defaultdict(list)
primer_indices = defaultdict(list)

# Parsing the well identifiers
for index, identifier in enumerate(well_list):
    if '_' in identifier and identifier != '_':
        # Split the identifier to get template name and primer combination
        template, primer = identifier.split('_')
        
        # Store the index in the corresponding template and primer lists
        template_indices[template].append(index)
        primer_indices[primer].append(index)

# Convert disctionaries into lists of lists
template_wells = list(template_indices.values())
MM_wells = list(primer_indices.values())

print('Template Wells List:', template_wells)
print('Master Mix Wells:', MM_wells)