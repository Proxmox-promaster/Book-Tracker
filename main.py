import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("650x450")
        self.file_path = "books.json"
        self.books = []

        # Поля ввода
        frame_in = tk.Frame(root, pady=10)
        frame_in.pack()

        tk.Label(frame_in, text="Название:").grid(row=0, column=0)
        self.e_title = tk.Entry(frame_in)
        self.e_title.grid(row=0, column=1, padx=5)

        tk.Label(frame_in, text="Автор:").grid(row=0, column=2)
        self.e_author = tk.Entry(frame_in)
        self.e_author.grid(row=0, column=3, padx=5)

        tk.Label(frame_in, text="Жанр:").grid(row=1, column=0, pady=5)
        self.e_genre = tk.Entry(frame_in)
        self.e_genre.grid(row=1, column=1, padx=5)

        tk.Label(frame_in, text="Страниц:").grid(row=1, column=2)
        self.e_pages = tk.Entry(frame_in)
        self.e_pages.grid(row=1, column=3, padx=5)

        tk.Button(frame_in, text="Добавить", command=self.add_book).grid(row=0, column=4, rowspan=2, padx=10)

        # Фильтры
        frame_f = tk.Frame(root, pady=5)
        frame_f.pack()
        
        tk.Label(frame_f, text="Фильтр Жанр:").grid(row=0, column=0)
        self.f_genre = tk.Entry(frame_f, width=10)
        self.f_genre.grid(row=0, column=1, padx=5)

        tk.Label(frame_f, text="Мин. страниц:").grid(row=0, column=2)
        self.f_pages = tk.Entry(frame_f, width=5)
        self.f_pages.grid(row=0, column=3, padx=5)

        tk.Button(frame_f, text="Ок", command=self.apply_filter).grid(row=0, column=4, padx=2)
        tk.Button(frame_f, text="Сброс", command=self.show_all).grid(row=0, column=5, padx=2)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("t", "a", "g", "p"), show="headings", height=10)
        self.tree.heading("t", text="Название"); self.tree.heading("a", text="Автор")
        self.tree.heading("g", text="Жанр"); self.tree.heading("p", text="Стр.")
        self.tree.column("p", width=50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load()

    def add_book(self):
        t, a, g, p = self.e_title.get(), self.e_author.get(), self.e_genre.get(), self.e_pages.get()
        if not (t and a and g and p): return messagebox.showerror("!", "Заполните всё")
        if not p.isdigit(): return messagebox.showerror("!", "Страницы — число")
        
        self.books.append({"title": t, "author": a, "genre": g, "pages": int(p)})
        self.save()
        self.show_all()
        for e in [self.e_title, self.e_author, self.e_genre, self.e_pages]: e.delete(0, 'end')

    def apply_filter(self):
        gen, pag = self.f_genre.get().lower(), self.f_pages.get()
        res = [b for b in self.books if gen in b['genre'].lower()]
        if pag.isdigit(): res = [b for b in res if b['pages'] >= int(pag)]
        self.update_view(res)

    def show_all(self): self.update_view(self.books)

    def update_view(self, data):
        self.tree.delete(*self.tree.get_children())
        for b in data: self.tree.insert("", "end", values=(b['title'], b['author'], b['genre'], b['pages']))

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f: json.dump(self.books, f, ensure_ascii=False)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f: self.books = json.load(f)
            self.show_all()

if __name__ == "__main__":
    root = tk.Tk()
    BookTracker(root)
    root.mainloop()
