import pandas as pd
import numpy as np

def encode_input(file_path):
    # Load the Excel workbook 
    plate_df = pd.read_excel(file_path, sheet_name='plate', dtype='str')
    mappings_df = pd.read_excel(file_path, sheet_name='mappings', dtype='str')

    # Get plasmids
    plasmids = mappings_df['plasmid'].to_list()
    plasmids_map = [['' for j in range(0,6)] for i in range(0,4)]

    plate = plate_df.to_numpy()[:, 1:]

    for i in range(0, 4):
        for j in range(0, 6):
            if plate[i][j] in plasmids:
                plasmids_map[i][j] = plate[i][j]

    print(plasmids_map)

    # Get primers
    primers = mappings_df['primer 1'].to_list()
    primers.extend(mappings_df['primer 2'].to_list())
    primers_map = [['' for j in range(0,6)] for i in range(0,4)]

    for i in range(0, 4):
        for j in range(0, 6):
            if plate[i][j] in primers:
                primers_map[i][j] = plate[i][j]

    print(primers_map)

    return {'plasmids': plasmids_map, 'primers': primers_map, 'mappings': mappings_df.fillna('').to_numpy().tolist()}

print(encode_input('input.xlsx'))