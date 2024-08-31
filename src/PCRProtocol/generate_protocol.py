import pandas as pd

def read_excel_file(file_path):
    # Load the Excel file
    excel_data = pd.ExcelFile(file_path)
    
    # Initialize the dictionary to hold sheet data
    sheet_data = {}
    
    # Iterate through each sheet except the last one
    for sheet_name in excel_data.sheet_names:
        if sheet_name != "mappings":
            # Read the sheet into a DataFrame
            df = pd.read_excel(file_path, sheet_name=sheet_name, index_col=0)
            df = df.fillna("")
            
            # Convert DataFrame to 2D array
            data_array = df.values
            
            # Store the 2D array in the dictionary
            sheet_data[sheet_name] = data_array.tolist()
    
    # Process the 'mappings' sheet separately
    if 'mappings' in excel_data.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(file_path, sheet_name='mappings')
        df = df.fillna("")
            
        # Convert DataFrame to 2D array
        data_array = df.values
        
        # Get row headers and id
        row_headers = df.index.tolist()
        ids = df.index.to_list()
        
        # Store the 2D array in the dictionary
        sheet_data['mappings'] = data_array.tolist()

    return sheet_data

# Example usage
file_path = 'input.xlsx'  # Replace with your actual file path
data = read_excel_file(file_path)
print(data)
