import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to sort and clean registry file content
def sort_and_clean_registry_file(file_path):
    try:
        # Open the registry file and read its contents
        with open(file_path, 'r', encoding='utf-16') as file:
            lines = file.readlines()

        # Remove empty lines and leading/trailing whitespaces
        lines = [line.strip() for line in lines if line.strip()]

        # Initialize data structures
        sorted_lines = []
        section_data = {}
        current_section = None

        # Process each line
        for line in lines:
            if line.startswith('[') and line.endswith(']'):
                # Store any previous section data before starting a new section
                if current_section is not None:
                    if current_section in section_data:
                        # Sort and add section data to sorted_lines
                        sorted_lines.append(f"[{current_section}]")
                        for key in sorted(section_data[current_section].keys()):
                            sorted_lines.append(f"{key}={section_data[current_section][key]}")
                # Start a new section
                current_section = line[1:-1]  # Remove the brackets
                section_data[current_section] = {}
            else:
                if current_section is not None:
                    key, value = line.split('=', 1)
                    section_data[current_section][key] = value

        # Add the last section data
        if current_section is not None:
            if current_section in section_data:
                sorted_lines.append(f"[{current_section}]")
                for key in sorted(section_data[current_section].keys()):
                    sorted_lines.append(f"{key}={section_data[current_section][key]}")

        # Generate sorted file name
        sorted_file_path = os.path.splitext(file_path)[0] + '_sorted.reg'

        # Write the sorted lines back to a new file
        with open(sorted_file_path, 'w', encoding='utf-16') as sorted_file:
            for line in sorted_lines:
                sorted_file.write(line + '\n')

        return sorted_file_path

    except Exception as e:
        return str(e)

# Function to open a file dialog and select the registry file
def select_registry_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select a registry file",
        filetypes=[("Registry files", "*.reg")]
    )
    if file_path:
        sorted_file = sort_and_clean_registry_file(file_path)
        if os.path.exists(sorted_file):
            messagebox.showinfo("Success", f"Sorted file created:\n{sorted_file}")
        else:
            messagebox.showerror("Error", f"An error occurred:\n{sorted_file}")
    else:
        messagebox.showinfo("Cancelled", "No file selected.")

if __name__ == "__main__":
    select_registry_file()
