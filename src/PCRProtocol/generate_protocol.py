import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import simpledialog
import pandas as pd
import csv


class EditMappingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Edit Mapping and Plate Manager")

        self.data = pd.DataFrame(columns=["id", "plasmid", "forward", "reverse", "notes"])
        self.plates = []
        self.selected_plate = None

        self.create_widgets()

    def create_widgets(self):
        # Mapping Table
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        self.table_buttons_frame = tk.Frame(self.root)
        self.table_buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        self.load_button = tk.Button(self.table_buttons_frame, text="Load Mapping CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.load_plate_button = tk.Button(self.table_buttons_frame, text="Load Plate CSV", command=self.load_plates_from_csv)
        self.load_plate_button.pack(side=tk.LEFT, padx=5)

        self.new_button = tk.Button(self.table_buttons_frame, text="New", command=self.new_csv)
        self.new_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.table_buttons_frame, text="Save Mapping CSV", command=self.save_csv)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.save_plate_button = tk.Button(self.table_buttons_frame, text="Save Plate CSV", command=self.save_plates_to_csv)
        self.save_plate_button.pack(side=tk.LEFT, padx=5)

        self.add_row_button = tk.Button(self.table_buttons_frame, text="Add Row", command=self.add_row)
        self.add_row_button.pack(side=tk.LEFT, padx=5)

        self.remove_row_button = tk.Button(self.table_buttons_frame, text="Remove Row", command=self.remove_row)
        self.remove_row_button.pack(side=tk.LEFT, padx=5)

        self.add_plate_button = tk.Button(self.table_buttons_frame, text="Add Plate", command=self.add_plate)
        self.add_plate_button.pack(side=tk.LEFT, padx=5)

        self.manage_plates_button = tk.Button(self.table_buttons_frame, text="Manage Plates", command=self.manage_plates)
        self.manage_plates_button.pack(side=tk.LEFT, padx=5)

        self.generate_button = tk.Button(self.table_buttons_frame, text="Generate Protocol", command=self.generate_protocol)
        self.generate_button.pack(side=tk.LEFT, padx=5)



        self.refresh_table()

    def refresh_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Add column headers
        for idx, col in enumerate(self.data.columns):
            header = tk.Label(self.table_frame, text=col, borderwidth=1, relief="solid")
            header.grid(row=0, column=idx, sticky="nsew")

        # Add rows and entry fields
        for row_idx, row_data in self.data.iterrows():
            for col_idx, col_name in enumerate(self.data.columns):
                if col_name in ["plasmid", "forward", "reverse"]:
                    entry = tk.Entry(self.table_frame, borderwidth=1, relief="solid")
                    entry.insert(0, row_data[col_name])
                    entry.grid(row=row_idx + 1, column=col_idx, sticky="nsew")
                    entry.bind("<FocusOut>", lambda e, r=row_idx, c=col_name: self.update_data(r, c, e.widget.get()))
                else:
                    entry = tk.Label(self.table_frame, text=row_data[col_name], borderwidth=1, relief="solid")
                    entry.grid(row=row_idx + 1, column=col_idx, sticky="nsew")

    def update_data(self, row, col_name, value):
        self.data.at[row, col_name] = value

    def add_row(self):
        new_row = pd.DataFrame([[""] * len(self.data.columns)], columns=self.data.columns)
        self.data = pd.concat([self.data, new_row], ignore_index=True)
        self.refresh_table()

    def remove_row(self):
        if not self.data.empty:
            self.data = self.data.iloc[:-1]
            self.refresh_table()

    def load_csv(self):
        self.file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not self.file_path:
            return

        try:
            self.data = pd.read_csv(self.file_path, dtype=str).fillna("")
            self.refresh_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def new_csv(self):
        self.data = pd.DataFrame(columns=["id", "plasmid", "forward", "reverse", "notes"])
        self.refresh_table()

    def save_csv(self):
        self.file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save CSV File"
        )
        if not self.file_path:
            return

        try:
            self.data.to_csv(self.file_path, index=False)
            messagebox.showinfo("Success", "File saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def refresh_plate(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if not self.selected_plate:
            return

        # Add plate headers
        for row in range(4):
            row_label = tk.Label(self.table_frame, text=chr(65 + row), borderwidth=1, relief="solid")
            row_label.grid(row=row + 1, column=0, sticky="nsew")

        for col in range(6):
            col_label = tk.Label(self.table_frame, text=str(col + 1), borderwidth=1, relief="solid")
            col_label.grid(row=0, column=col + 1, sticky="nsew")

        # Populate cells with entries and dropdowns
        for row in range(4):
            for col in range(6):
                if row == 3 and col == 5:  # Block D6
                    entry = tk.Label(self.table_frame, text="Common Reagents", borderwidth=1, relief="solid", bg="lightgray")
                    entry.grid(row=row + 1, column=col + 1, sticky="nsew")
                else:
                    # Create a frame to hold the entry and dropdown
                    cell_frame = tk.Frame(self.table_frame)
                    cell_frame.grid(row=row + 1, column=col + 1, sticky="nsew")

                    # Entry for content
                    entry = tk.Entry(cell_frame, borderwidth=1, relief="solid")
                    entry.insert(0, self.selected_plate.get_content(row, col))
                    entry.grid(row=0, column=0, sticky="nsew")
                    entry.bind("<FocusOut>", lambda e, r=row, c=col: self.update_plate_content(r, c, e.widget.get()))

                    # Dropdown for type
                    dropdown = ttk.Combobox(cell_frame, values=["Plasmid", "Forward Primer", "Reverse Primer"])
                    dropdown.grid(row=1, column=0, sticky="nsew")
                    dropdown.set(self.selected_plate.get_type(row, col))
                    dropdown.bind("<<ComboboxSelected>>", lambda e, r=row, c=col: self.update_plate_type(r, c, e.widget.get()))

        # Configure row and column weights
        for i in range(7):
            self.table_frame.columnconfigure(i, weight=1)
        for i in range(5):
            self.table_frame.rowconfigure(i, weight=1)


    def add_plate(self):
        name = simpledialog.askstring("Input", "Enter plate name:")
        if name:
            plate = Plate(name)
            self.plates.append(plate)

            # Automatically select the new plate
            self.selected_plate = plate
            self.refresh_plate()  # Refresh the UI to show the new plate

    def manage_plates(self):
        plate_manager = PlateManager(self.root, self.plates)
        self.root.wait_window(plate_manager.window)

        # Check if a new plate was selected
        if hasattr(plate_manager, 'selected_plate_index'):
            self.selected_plate = self.plates[plate_manager.selected_plate_index]
            self.refresh_plate()

    def refresh_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Add column headers
        for idx, col in enumerate(self.data.columns):
            header = tk.Label(self.table_frame, text=col, borderwidth=1, relief="solid")
            header.grid(row=0, column=idx, sticky="nsew")

        # Add rows and entry fields
        for row_idx, row_data in self.data.iterrows():
            for col_idx, col_name in enumerate(self.data.columns):
                if col_name in ["plasmid", "forward", "reverse", "id", "notes"]:
                    entry = tk.Entry(self.table_frame, borderwidth=1, relief="solid")
                    entry.insert(0, row_data[col_name])
                    entry.grid(row=row_idx + 1, column=col_idx, sticky="nsew")
                    entry.bind("<FocusOut>", lambda e, r=row_idx, c=col_name: self.update_data(r, c, e.widget.get()))
                else:
                    entry = tk.Label(self.table_frame, text=row_data[col_name], borderwidth=1, relief="solid")
                    entry.grid(row=row_idx + 1, column=col_idx, sticky="nsew")

        # Configure row and column weights
        for i in range(len(self.data.columns)):
            self.table_frame.columnconfigure(i, weight=1)
        for i in range(len(self.data.index) + 1):
            self.table_frame.rowconfigure(i, weight=1)

    def save_plates_to_csv(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not filepath:
            return

        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Plate Number", "Well", "Content", "Type"])  # Header

            for plate_index, plate in enumerate(self.plates):
                for row in range(4):
                    for col in range(6):
                        well = chr(65 + row) + str(col + 1)  # e.g., A1, B2
                        content = plate.get_content(row, col)
                        content_type = plate.get_type(row, col)
                        writer.writerow([plate_index + 1, well, content, content_type])

            # Write plate order metadata
            writer.writerow(["Order", ",".join(str(i+1) for i in range(len(self.plates)))])

    def load_plates_from_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not filepath:
            return

        with open(filepath, mode='r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip header

            # Initialize empty plates
            self.plates = []
            plate_order = []

            for row in reader:
                if row[0] == "Order":
                    plate_order = list(map(int, row[1].split(',')))
                    break

                plate_index = int(row[0]) - 1
                well = row[1]
                content = row[2]
                content_type = row[3]

                # Ensure the plate exists
                while len(self.plates) <= plate_index:
                    self.plates.append(Plate())  # Assuming Plate is your class for handling plate data

                # Convert well position back to row and col
                row_index = ord(well[0]) - 65
                col_index = int(well[1]) - 1

                self.plates[plate_index].set_content(row_index, col_index, content)
                self.plates[plate_index].set_type(row_index, col_index, content_type)

            # Reorder plates according to saved order
            self.plates = [self.plates[i-1] for i in plate_order]

            # Set the first plate as the selected plate and refresh the UI
            self.selected_plate = self.plates[0] if self.plates else None

        self.refresh_plate()  # Refresh the UI to display loaded plates


        
    def update_plate_content(self, row, col, value):
        self.selected_plate.set_content(row, col, value)

    def update_plate_type(self, row, col, value):
            self.selected_plate.set_type(row, col, value)
        
    def generate_protocol(self):

        def get_file_path(prompt):
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            file_path = filedialog.askopenfilename(title=prompt, filetypes=[("CSV files", "*.csv")])
            return file_path

        def get_protocol_name():
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            protocol_name = simpledialog.askstring("Protocol Name", "Enter the name of the protocol:")
            return protocol_name

        # Get the file paths
        mappings_file_path = get_file_path("Select the mappings CSV file")
        plates_file_path = get_file_path("Select the plates CSV file")

        # Load the CSV files
        mappings_df = pd.read_csv(mappings_file_path)
        plates_df = pd.read_csv(plates_file_path)

        # Get protocol name
        protocol_name = get_protocol_name()

        # Initialize the output dictionary
        encoded_input = {
            'plasmids': [['' for _ in range(6)] for _ in range(4)],
            'forward_primers': [['' for _ in range(6)] for _ in range(4)],
            'reverse_primers': [['' for _ in range(6)] for _ in range(4)],
            'mappings': mappings_df.values.tolist()
        }

        # Process the plates DataFrame to fill the encoded_input dictionary
        for _, row in plates_df.iterrows():
            well = row['Well']
            content = row['Content']
            content_type = row['Type']
            
            # Validate well format
            if pd.notna(well) and len(well) >= 2 and well[0] in 'ABCD' and well[1:].isdigit():
                # Convert well to row and column indices
                row_index = ord(well[0]) - ord('A')
                col_index = int(well[1:]) - 1
                
                if content_type == 'Plasmid':
                    encoded_input['plasmids'][row_index][col_index] = content
                elif content_type == 'Forward Primer':
                    encoded_input['forward_primers'][row_index][col_index] = content
                elif content_type == 'Reverse Primer':
                    encoded_input['reverse_primers'][row_index][col_index] = content
            else:
                print(f"Warning: Skipping invalid well format or empty well: {well}")

        # Convert encoded_input to a string representation
        encoded_input_str = repr(encoded_input)

        # File path for _pcr.py in the current directory
        script_directory = os.path.dirname(os.path.abspath(__file__))
        pcr_file_path = os.path.join(script_directory, '_pcr.py')

        # Read the _pcr.py file
        with open(pcr_file_path, 'r') as file:
            pcr_content = file.readlines()

        # Replace the line starting with encoded_input=
        new_pcr_content = []
        for line in pcr_content:
            if line.strip().startswith('encoded_input = '):
                new_pcr_content.append(f'encoded_input = {encoded_input_str}\n')
            else:
                new_pcr_content.append(line)

        # Write to the new file
        new_file_path = f'{protocol_name}.py'
        with open(new_file_path, 'w') as file:
            file.writelines(new_pcr_content)

        print(f"Updated file saved as {new_file_path}")





class Plate:
    def __init__(self, name=""):
        self.name = name
        self.grid = pd.DataFrame("", index=range(4), columns=range(6))
        self.type_grid = pd.DataFrame("", index=range(4), columns=range(6))

    def get_content(self, row, col):
        return self.grid.iat[row, col]

    def set_content(self, row, col, value):
        self.grid.iat[row, col] = value

    def get_type(self, row, col):
        return self.type_grid.iat[row, col]

    def set_type(self, row, col, value):
        self.type_grid.iat[row, col] = value


class PlateManager:
    def __init__(self, parent, plates):
        self.window = tk.Toplevel(parent)
        self.window.title("Manage Plates")
        self.plates = plates
        self.create_widgets()

    def create_widgets(self):
        self.listbox = tk.Listbox(self.window, selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        for i, plate in enumerate(self.plates):
            self.listbox.insert(tk.END, plate.name)

        self.up_button = tk.Button(self.window, text="Move Up", command=self.move_up)
        self.up_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.down_button = tk.Button(self.window, text="Move Down", command=self.move_down)
        self.down_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.rename_button = tk.Button(self.window, text="Rename", command=self.rename_plate)
        self.rename_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(self.window, text="Delete", command=self.delete_plate)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.select_button = tk.Button(self.window, text="Select", command=self.select_plate)
        self.select_button.pack(side=tk.LEFT, padx=5, pady=5)

    def rename_plate(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            new_name = simpledialog.askstring("Input", "Enter new plate name:")
            if new_name:
                self.plates[index].name = new_name
                self.listbox.delete(index)
                self.listbox.insert(index, new_name)

    def move_up(self):
        selection = self.listbox.curselection()
        if not selection:
            return

        index = selection[0]
        if index > 0:
            self.plates[index], self.plates[index - 1] = self.plates[index - 1], self.plates[index]
            self.listbox.delete(0, tk.END)
            for plate in self.plates:
                self.listbox.insert(tk.END, plate.name)
            self.listbox.select_set(index - 1)

    def move_down(self):
        selection = self.listbox.curselection()
        if not selection:
            return

        index = selection[0]
        if index < len(self.plates) - 1:
            self.plates[index], self.plates[index + 1] = self.plates[index + 1], self.plates[index]
            self.listbox.delete(0, tk.END)
            for plate in self.plates:
                self.listbox.insert(tk.END, plate.name)
            self.listbox.select_set(index + 1)

    def delete_plate(self):
        selection = self.listbox.curselection()
        if not selection:
            return

        index = selection[0]
        del self.plates[index]
        self.listbox.delete(index)

    def select_plate(self):
        selection = self.listbox.curselection()
        if selection:
            # Update the selected plate index
            self.selected_plate_index = selection[0]
            self.window.destroy()

    

if __name__ == "__main__":
    root = tk.Tk()
    app = EditMappingApp(root)
    root.mainloop()
