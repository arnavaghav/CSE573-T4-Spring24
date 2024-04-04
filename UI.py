'''
CSE573 Semantic Web Mining
Group #4 Project #22 Dark Web Crawling

'''

import tkinter as tk
from tkinter import messagebox
import pysolr

''' TODO:
Replace solr_url with our Solr core
'''
solr_url = "http://localhost:8983/solr/my_core"
solr = pysolr.Solr(solr_url, always_commit=True)

def index_data():
    #for user inputs to get ID, Title, Content
    data = {
        "id": entry_id.get(),
        "title": entry_title.get(),
        "content": entry_content.get("1.0", tk.END).strip()
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
            result_text.insert(tk.END, f"ID: {result['id']}\nTitle: {result['title']}\nContent: {result['content']}\n\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to search data: {e}")

# Create the main window
root = tk.Tk()
root.title("CSE573 Dark Web Crawling")

# Create input fields and buttons
tk.Label(root, text="ID:").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="Title:").pack()
entry_title = tk.Entry(root)
entry_title.pack()

tk.Label(root, text="Content:").pack()
entry_content = tk.Text(root, height=5, width=50)
entry_content.pack()

tk.Button(root, text="Index Data", command=index_data).pack()

tk.Label(root, text="Query:").pack()
entry_query = tk.Entry(root)
entry_query.pack()

tk.Button(root, text="Search Data", command=search_data).pack()

# Create a text area for displaying search results
result_text = tk.Text(root, height=20, width=70)
result_text.pack()

# Start the GUI event loop
root.mainloop()