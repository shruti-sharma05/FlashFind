import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog


def execute_fd_command():
    """
    Run the fd command with the user's input and display results in the listbox.
    """
    query = search_entry.get().strip()
    use_regex = regex_var.get()

    if not query:
        messagebox.showwarning("Input Error", "Please enter a search query!")
        return

    # Clear previous results
    results_listbox.delete(0, tk.END)
    result_count_label.config(text="")  # Clear result count

    # Build the fd command
    command = ["fd", query, "--absolute-path"]
    if use_regex:
        command.append("--regex")

    # Execute fd command
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        output = result.stdout.strip()
        if output:
            results = output.split("\n")
            for line in results:
                results_listbox.insert(tk.END, line)
            result_count_label.config(text=f"Results Found: {len(results)}")
        else:
            messagebox.showinfo("No Results", "No files or directories found.")
    except FileNotFoundError:
        messagebox.showerror("Error", "The 'fd' command is not installed or not found in PATH.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def open_selected_item():
    """
    Open the selected file or directory from the results list.
    """
    selected_item = results_listbox.curselection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to open.")
        return

    path = results_listbox.get(selected_item[0])
    if os.path.exists(path):
        os.startfile(path)  # Open file/directory with the default application
    else:
        messagebox.showerror("Error", "The selected file or directory no longer exists.")


def clear_results():
    """Clear the search results from the Listbox."""
    results_listbox.delete(0, tk.END)
    result_count_label.config(text="")


def save_results():
    """Save search results to a text file."""
    results = results_listbox.get(0, tk.END)
    if not results:
        messagebox.showwarning("No Results", "No search results to save!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", ".txt"), ("All Files", ".*")]
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write("\n".join(results))
        messagebox.showinfo("Saved", f"Results saved to {file_path}")


def copy_path():
    """Copy the selected file or directory path to the clipboard."""
    selected_item = results_listbox.curselection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to copy its path.")
        return

    path = results_listbox.get(selected_item[0])
    root.clipboard_clear()
    root.clipboard_append(path)
    root.update()
    messagebox.showinfo("Copied", "Path copied to clipboard!")


def open_containing_folder():
    """Open the folder containing the selected file or directory."""
    selected_item = results_listbox.curselection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item to open its containing folder.")
        return

    path = results_listbox.get(selected_item[0])
    if os.path.exists(path):
        folder_path = os.path.dirname(path)
        os.startfile(folder_path)
    else:
        messagebox.showerror("Error", "The selected file or directory no longer exists.")


# GUI Setup
root = tk.Tk()
root.title("FlashFind GUI Application")
root.geometry("800x600")
root.configure(bg="#B9E5E8")  # Dark background

# Title Label
title_label = tk.Label(
    root,
    text="FlashFind File Search",
    font=("Helvetica", 20, "bold"),
    fg="#DFF2EB",
    bg="#7AB2D3"
)
title_label.pack(pady=10)

# Search Query Frame
search_frame = tk.Frame(root, bg="#7AB2D3")
search_frame.pack(pady=10)

search_label = tk.Label(
    search_frame,
    text="Search Query:",
    font=("Helvetica", 12),
    fg="#4A628A",
    bg="#B9E5E8"
)
search_label.grid(row=0, column=0, padx=10)

search_entry = tk.Entry(search_frame, width=40, font=("Helvetica", 12))
search_entry.grid(row=0, column=1, padx=10)

search_button = tk.Button(
    search_frame,
    text="Search",
    font=("Helvetica", 12),
    bg="#4caf50",
    fg="#ffffff",
    activebackground="#388e3c",
    activeforeground="#ffffff",
    command=execute_fd_command
)
search_button.grid(row=0, column=2, padx=10)

# Regex Checkbox
regex_var = tk.BooleanVar()
regex_checkbox = tk.Checkbutton(
    search_frame,
    text="Use Regex",
    variable=regex_var,
    font=("Helvetica", 10),
    fg="#4A628A",
    bg="#B9E5E8",
    activebackground="#4A628A",
    activeforeground="#B9E5E8",
    selectcolor="#4A628A"
)
regex_checkbox.grid(row=1, column=1, pady=5)

# Results Frame
results_frame = tk.Frame(root, bg="#7AB2D3")
results_frame.pack(pady=10)

results_label = tk.Label(
    results_frame,
    text="Search Results:",
    font=("Helvetica", 12),
    fg="#4A628A",
    bg="#B9E5E8"
)
results_label.pack(anchor="w", padx=10)

results_listbox = tk.Listbox(
    results_frame,
    width=80,
    height=15,
    font=("Helvetica", 10),
    bg="#4A628A",
    fg="#B9E5E8",
    selectbackground="#4caf50",
    selectforeground="#ffffff",
    highlightbackground="#1f1f1f"
)
results_listbox.pack(pady=5, padx=10)

# Result Count
result_count_label = tk.Label(
    results_frame,
    text="",
    font=("Helvetica", 10),
    fg="#4A628A",
    bg="#B9E5E8"
)
result_count_label.pack(anchor="w", padx=10)

# Action Buttons
action_frame = tk.Frame(root, bg="#7AB2D3")
action_frame.pack(pady=10)

open_button = tk.Button(
    action_frame,
    text="Open Selected",
    font=("Helvetica", 12),
    bg="#B9E5E8",
    fg="#4A628A",
    activebackground="#4A628A",
    activeforeground="#B9E5E8",
    command=open_selected_item
)
open_button.grid(row=0, column=0, padx=10)

copy_button = tk.Button(
    action_frame,
    text="Copy Path",
    font=("Helvetica", 12),
    bg="#B9E5E8",
    fg="#4A628A",
    activebackground="#4A628A",
    activeforeground="#B9E5E8",
    command=copy_path
)
copy_button.grid(row=0, column=1, padx=10)

folder_button = tk.Button(
    action_frame,
    text="Open Containing Folder",
    font=("Helvetica", 12),
    bg="#B9E5E8",
    fg="#4A628A",
    activebackground="#4A628A",
    activeforeground="#B9E5E8",
    command=open_containing_folder
)
folder_button.grid(row=0, column=2, padx=10)

clear_button = tk.Button(
    action_frame,
    text="Clear Results",
    font=("Helvetica", 12),
    bg="#B9E5E8",
    fg="#4A628A",
    activebackground="#4A628A",
    activeforeground="#B9E5E8",
    command=clear_results
)
clear_button.grid(row=0, column=3, padx=10)

save_button = tk.Button(
    action_frame,
    text="Save Results",
    font=("Helvetica", 12),
    bg="#B9E5E8",
    fg="#4A628A",
    activebackground="#4A628A",
    activeforeground="#B9E5E8",
    command=save_results
)
save_button.grid(row=0, column=4, padx=10)

# Footer Label
footer_label = tk.Label(
    root,
    text="FlashFind by Shruti",
    font=("Helvetica", 10, "italic"),
    fg="#DFF2EB",
    bg="#7AB2D3"
)
footer_label.pack(side="bottom", pady=20)

# Run the application
root.mainloop()