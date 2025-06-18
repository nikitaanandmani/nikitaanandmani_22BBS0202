import tkinter as tk
from tkinter import messagebox
from . import auth, book_crud
from PIL import Image, ImageTk
import os

class App:
    def set_background(self):
        try:
            bg_path = os.path.join(os.path.dirname(__file__), "..", "assets", "bg.jpg")
            bg_image = Image.open(bg_path)
            bg_image = bg_image.resize((1200, 700))
            self.bg_img = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.root, image=self.bg_img)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_layer = bg_label
        except Exception as e:
            print("Background image error:", e)

    def __init__(self, root):
        self.root = root
        self.root.title("Books Management System")
        self.current_user = None
        self.build_login_ui()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.set_background()

    def build_login_ui(self):
        self.clear_window()

        form_frame = tk.Frame(self.root, bg="white", bd=4, relief="groove")
        form_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)

        heading = tk.Label(form_frame, text="Library System Login", font=("Helvetica", 18, "bold"), bg="white")
        heading.pack(pady=(20, 10))

        tk.Label(form_frame, text="Username", bg="white", anchor="w").pack(fill="x", padx=40)
        email_entry = tk.Entry(form_frame, width=30, font=("Helvetica", 12))
        email_entry.pack(pady=5)

        tk.Label(form_frame, text="Password", bg="white", anchor="w").pack(fill="x", padx=40)
        password_entry = tk.Entry(form_frame, show="*", width=30, font=("Helvetica", 12))
        password_entry.pack(pady=5)

        def login():
            email = email_entry.get()
            password = password_entry.get()
            if auth.login_user(email, password):
                messagebox.showinfo("Success", "Logged in successfully")
                self.build_crud_ui()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(form_frame, text="Login", command=login, font=("Helvetica", 12), width=20).pack(pady=10)
        tk.Button(form_frame, text="Register", command=self.build_register_ui, font=("Helvetica", 10)).pack()

    def build_register_ui(self):
        self.clear_window()
        form_frame = tk.Frame(self.root, bg="white", bd=4, relief="groove")
        form_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=250)

        tk.Label(form_frame, text="Register", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        tk.Label(form_frame, text="Username", bg="white").pack()
        email_entry = tk.Entry(form_frame)
        email_entry.pack()

        tk.Label(form_frame, text="Password", bg="white").pack()
        password_entry = tk.Entry(form_frame, show="*")
        password_entry.pack()

        def register():
            email = email_entry.get()
            password = password_entry.get()
            if auth.register_user(email, password):
                messagebox.showinfo("Success", "Registered successfully")
                self.build_login_ui()
            else:
                messagebox.showerror("Error", "User already exists")

        tk.Button(form_frame, text="Register", command=register).pack(pady=5)
        tk.Button(form_frame, text="Back", command=self.build_login_ui).pack()

    def build_crud_ui(self):
        self.clear_window()

        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(btn_frame, text="Books Management", font=("Helvetica", 18, "bold"), bg="white").pack(pady=(0, 20))

        def styled_button(text, cmd, bg_color="#FF7AF2", active_bg="#FF7AF2"):
            return tk.Button(
                btn_frame,
                text=text,
                command=cmd,
                bg=bg_color,
                fg="white",
                font=("Helvetica", 12, "bold"),
                activebackground=active_bg,
                relief="raised",
                bd=3,
                width=20
            )

        styled_button("Add Book", self.add_book_form).pack(pady=5)
        styled_button("Show All Books", self.show_books_table).pack(pady=5)
        styled_button("Update Book", self.update_book).pack(pady=5)
        styled_button("Delete Book", self.delete_book).pack(pady=5)
        styled_button("Search Books", self.search_books_ui).pack(pady=5)
        styled_button("Logout", self.build_login_ui, bg_color="#421005", active_bg="#421005").pack(pady=15)

    def add_book_form(self):
        self.clear_window()
        form_frame = tk.Frame(self.root, bg="white")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        fields = [
            "title", "author", "isbn", "publisher", "year",
            "location_row", "location_column", "section"
        ]
        entries = {}

        for field in fields:
            tk.Label(form_frame, text=field.replace('_', ' ').capitalize(), bg="white").pack()
            entry = tk.Entry(form_frame)
            entry.pack()
            entries[field] = entry

        def submit():
            data = {key: entry.get() for key, entry in entries.items()}
            book_crud.add_book(data)
            messagebox.showinfo("Success", "Book added successfully!")
            self.build_crud_ui()

        tk.Button(form_frame, text="Submit", command=submit).pack(pady=5)
        tk.Button(form_frame, text="Back", command=self.build_crud_ui).pack()

    def show_books_table(self):
        self.clear_window()

        outer_frame = tk.Frame(self.root)
        outer_frame.place(relx=0.5, rely=0.5, anchor="center")

        books = book_crud.get_all_books()
        columns = ["_id", "title", "author", "isbn", "publisher", "year", "location_row", "location_column", "section"]

        for col_num, col in enumerate(columns):
            tk.Label(outer_frame, text=col.upper(), borderwidth=1, relief="solid", width=15).grid(row=0, column=col_num)

        for row_num, book in enumerate(books, start=1):
            for col_num, col in enumerate(columns):
                value = str(book.get(col, ""))
                tk.Label(outer_frame, text=value, borderwidth=1, relief="solid", width=15).grid(row=row_num, column=col_num)

        tk.Button(self.root, text="Back", command=self.build_crud_ui).place(relx=0.5, rely=0.80, anchor="center")

    def update_book(self):
        self.clear_window()
        form_frame = tk.Frame(self.root, bg="white")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        books = book_crud.get_all_books()
        options = [f"{book['_id']} - {book['title']}" for book in books]

        tk.Label(form_frame, text="Select Book to Update", bg="white").pack()
        selected = tk.StringVar()
        dropdown = tk.OptionMenu(form_frame, selected, *options)
        dropdown.pack()

        entries = {}
        fields = [
            "title", "author", "isbn", "publisher", "year",
            "location_row", "location_column", "section"
        ]

        for field in fields:
            tk.Label(form_frame, text=f"New {field.replace('_', ' ').capitalize()}", bg="white").pack()
            entry = tk.Entry(form_frame)
            entry.pack()
            entries[field] = entry

        def submit():
            if not selected.get():
                messagebox.showerror("Error", "No book selected")
                return
            book_id = selected.get().split(" - ")[0]
            updated_data = {k: v.get() for k, v in entries.items() if v.get()}
            book_crud.update_book(book_id, updated_data)
            messagebox.showinfo("Success", "Book updated successfully")
            self.build_crud_ui()

        tk.Button(form_frame, text="Update", command=submit).pack(pady=5)
        tk.Button(form_frame, text="Back", command=self.build_crud_ui).pack()

    def delete_book(self):
        self.clear_window()
        form_frame = tk.Frame(self.root, bg="white")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        books = book_crud.get_all_books()
        options = [f"{book['_id']} - {book['title']}" for book in books]

        tk.Label(form_frame, text="Select Book to Delete", bg="white").pack()
        selected = tk.StringVar()
        dropdown = tk.OptionMenu(form_frame, selected, *options)
        dropdown.pack()

        def submit():
            if not selected.get():
                messagebox.showerror("Error", "No book selected")
                return
            book_id = selected.get().split(" - ")[0]
            book_crud.delete_book(book_id)
            messagebox.showinfo("Success", "Book deleted successfully")
            self.build_crud_ui()

        tk.Button(form_frame, text="Delete", command=submit).pack(pady=5)
        tk.Button(form_frame, text="Back", command=self.build_crud_ui).pack()

    def search_books_ui(self):
        self.clear_window()

        form_frame = tk.Frame(self.root, bg="white")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(form_frame, text="Search Books", font=("Arial", 16), bg="white").pack(pady=10)

        tk.Label(form_frame, text="Select Field", bg="white").pack()
        field_var = tk.StringVar(value="title")
        field_options = ["title", "author", "isbn", "publisher", "year", "location_row", "location_column", "section"]
        field_dropdown = tk.OptionMenu(form_frame, field_var, *field_options)
        field_dropdown.pack()

        tk.Label(form_frame, text="Enter Keyword", bg="white").pack()
        keyword_entry = tk.Entry(form_frame)
        keyword_entry.pack(pady=5)

        def search():
            field = field_var.get()
            keyword = keyword_entry.get()
            results = book_crud.search_books(field, keyword)

            if not results:
                messagebox.showinfo("No Results", "No books found for your query.")
                return

            self.clear_window()
            result_frame = tk.Frame(self.root)
            result_frame.place(relx=0.5, rely=0.5, anchor="center")

            columns = ["_id", "title", "author", "isbn", "publisher", "year", "location_row", "location_column", "section"]
            for col_num, col in enumerate(columns):
                tk.Label(result_frame, text=col.upper(), borderwidth=1, relief="solid", width=15).grid(row=0, column=col_num)

            for row_num, book in enumerate(results, start=1):
                for col_num, col in enumerate(columns):
                    value = str(book.get(col, ""))
                    tk.Label(result_frame, text=value, borderwidth=1, relief="solid", width=15).grid(row=row_num, column=col_num)

            tk.Button(self.root, text="Back", command=self.build_crud_ui).place(relx=0.5, rely=0.95, anchor="center")

        tk.Button(form_frame, text="Search", command=search).pack(pady=5)
        tk.Button(form_frame, text="Back", command=self.build_crud_ui).pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Books Management System")
    root.geometry("1200x700")
    root.minsize(1000, 600)
    app = App(root)
    root.mainloop()
