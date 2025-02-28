import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import os
import csv

def add_contact():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    add_contact = simpledialog.askstring("Input", "Enter the name of the contact you want to add:")
    phone_number = simpledialog.askstring("Input", f"Enter the phone number of {add_contact}:")

    if add_contact and phone_number:
        file_path = r"C:\Users\nathan.adams_searcys\Documents\contact book\contacts.csv"
        try:
            with open(file_path, "a") as file:
                file.write(f"{add_contact}, {phone_number}, home\n")
            print("Added Contact!")
        except Exception as e:
            print(f"Failed to add contact: {e}")
    else:
        print("Contact not added. Missing information.")

def view_contacts():
    file_path = r"C:\Users\nathan.adams_searcys\Documents\contact book\contacts.csv"
    contacts = []

    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                contacts.append(row)
        contacts.sort(key=lambda x: x[0])  # Sort by name

        root = tk.Tk()
        root.title("Contacts A-Z")
        root.geometry("400x300")

        frame = ttk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        search_frame = ttk.Frame(frame)
        search_frame.pack(fill=tk.X, pady=5)

        search_label = ttk.Label(search_frame, text="Search:", font=("Century", 12))
        search_label.pack(side=tk.LEFT, padx=10)

        search_entry = ttk.Entry(search_frame, font=("Century", 12))
        search_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        search_button = ttk.Button(search_frame, text="Search", command=lambda: search_contacts(search_entry.get(), scrollable_frame))
        search_button.pack(side=tk.RIGHT, padx=10)

        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        display_contacts(contacts, scrollable_frame)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        root.mainloop()
    except Exception as e:
        print(f"Failed to read contacts: {e}")

def display_contacts(contacts, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    for contact in contacts:
        contact_str = ", ".join(contact)
        contact_frame = ttk.Frame(frame)
        contact_frame.pack(fill=tk.X, pady=5)

        label = ttk.Label(contact_frame, text=contact_str, font=("Century", 12))
        label.pack(side=tk.LEFT, padx=10)

        delete_button = ttk.Button(contact_frame, text="Delete", command=lambda c=contact: confirm_delete(c, frame))
        delete_button.pack(side=tk.RIGHT, padx=10)

def search_contacts(query, frame):
    file_path = r"C:\Users\nathan.adams_searcys\Documents\contact book\contacts.csv"
    contacts = []

    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if query.lower() in row[0].lower():
                    contacts.append(row)
        contacts.sort(key=lambda x: x[0])  # Sort by name

        display_contacts(contacts, frame)
    except Exception as e:
        print(f"Failed to search contacts: {e}")

def confirm_delete(contact, root):
    result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {contact[0]}?")
    if result:
        delete_contact(contact)
        root.destroy()
        view_contacts()

def delete_contact(contact):
    file_path = r"C:\Users\nathan.adams_searcys\Documents\contact book\contacts.csv"
    contacts = []

    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row != contact:
                    contacts.append(row)

        with open(file_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Email"])
            writer.writerows(contacts)

        print("Deleted Contact!")
    except Exception as e:
        print(f"Failed to delete contact: {e}")

def main_menu():
    root = tk.Tk()
    root.title("Contact Book")
    root.geometry("300x200")

    add_button = ttk.Button(root, text="Add Contact", command=add_contact)
    add_button.pack(pady=10)

    view_button = ttk.Button(root, text="View Contacts", command=view_contacts)
    view_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
