'''
CSE573 Semantic Web Mining
Group #4 Project #22 Dark Web Crawling

Group Members:
Arnav Aghav
Rachel Guzman
Yang Husurianto
Yumi Lamansky
Saidubabu Mallela
Wangyang Ying
'''

import tkinter as tk
from tkinter import messagebox, ttk
import pysolr

#TODO: Replace link with our Solr core
solr_url = "http://localhost:8983/solr/my_core"
solr = pysolr.Solr(solr_url, always_commit=True)

def index_data():
    data = {
        "id": entry_id.get(),
        "title": entry_title.get(),
        #"content": entry_content.get("1.0", tk.END).strip()
    }
    try:
        solr.add([data])
        messagebox.showinfo("Success", "Data indexed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to index data: {e}")

def search_data():
    query = entry_query.get()
    try:
        results = solr.search(query)
        result_text.delete("1.0", tk.END)
        for result in results:
            result_text.insert(tk.END, f"ID: {result['id']}\nTitle: {result['title']}\n\n") #Content: {result['content']}\n\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to search data: {e}")

# Create the main window
root = tk.Tk()
root.title("CSE573 Dark Web Crawling")

# Create a styled frame for the input fields
input_frame = ttk.Frame(root, padding="10")
input_frame.pack()

# ID input field
ttk.Label(input_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
entry_id = ttk.Entry(input_frame, width=30)
entry_id.grid(row=0, column=1, padx=5, pady=5)

# Title input field
ttk.Label(input_frame, text="Title:").grid(row=1, column=0, padx=5, pady=5)
entry_title = ttk.Entry(input_frame, width=30)
entry_title.grid(row=1, column=1, padx=5, pady=5)

# Content input field
ttk.Label(input_frame, text="Content:").grid(row=2, column=0, padx=5, pady=5)
entry_content = tk.Text(input_frame, height=5, width=40)
entry_content.grid(row=2, column=1, padx=5, pady=5)

# Index button
index_button = ttk.Button(input_frame, text="Index Data", command=index_data)
index_button.grid(row=3, column=0, columnspan=2, pady=10)

# Create a styled frame for the search section
search_frame = ttk.Frame(root, padding="10")
search_frame.pack()

# Query input field
ttk.Label(search_frame, text="Query:").grid(row=0, column=0, padx=5, pady=5)
entry_query = ttk.Entry(search_frame, width=30)
entry_query.grid(row=0, column=1, padx=5, pady=5)

# Search button
search_button = ttk.Button(search_frame, text="Search Data", command=search_data)
search_button.grid(row=0, column=2, padx=5, pady=5)

# Create a text area for displaying search results
result_text = tk.Text(root, height=10, width=50)
result_text.pack(pady=10)

# Start the GUI event loop
root.mainloop()
