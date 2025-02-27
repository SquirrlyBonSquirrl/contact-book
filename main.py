import tkinter as tk
from tkinter import simpledialog, messagebox
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

        for contact in contacts:
            contact_str = ", ".join(contact)
            label = tk.Label(root, text=contact_str)
            label.pack()

            delete_button = tk.Button(root, text="Delete", command=lambda c=contact: confirm_delete(c, root))
            delete_button.pack()

        root.mainloop()
    except Exception as e:
        print(f"Failed to read contacts: {e}")

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

    add_button = tk.Button(root, text="Add Contact", command=add_contact)
    add_button.pack(pady=10)

    view_button = tk.Button(root, text="View Contacts", command=view_contacts)
    view_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
