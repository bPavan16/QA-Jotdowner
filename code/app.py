import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox

class MarkdownGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Question Formatter")
        self.root.geometry("1200x800")
        self.root.minsize(900, 700)
        self.root.configure(bg="#1e1e1e")

        # Create style
        self.style = ttk.Style()
        self.configure_styles()

        # Variables
        self.md_file_path = tk.StringVar()
        self.question_name = tk.StringVar()
        self.markdown_content = ""

        # Main frame with scrollbar
        container = ttk.Frame(root)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg="#1e1e1e")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, padding=20, style="TFrame")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        window_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Layout
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Paned window for split view
        paned_window = ttk.PanedWindow(scrollable_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Left frame - Input
        left_frame = ttk.Frame(paned_window, padding="10", style="TFrame")
        paned_window.add(left_frame, weight=1)

        # Title
        title_label = ttk.Label(
            left_frame,
            text="📄 Markdown Question Formatter",
            font=("Segoe UI", 18, "bold"),
            style="Title.TLabel",
        )
        title_label.pack(pady=(0, 15))

        # Question Name
        self.create_label_entry(left_frame, "❓ Question Name", self.question_name)

        # Question Description
        self.description_text = self.create_scrolled_text(left_frame, "📜 Description", height=7)

        # Input List
        self.input_text = self.create_scrolled_text(left_frame, "📥 Input List", height=7)

        # Output List
        self.output_text = self.create_scrolled_text(left_frame, "📤 Output List", height=7)

        # Code Input
        self.code_text = self.create_scrolled_text(left_frame, "💻 C++ Code", height=8)

        # Action buttons
        buttons_frame = ttk.Frame(left_frame, style="TFrame")
        buttons_frame.pack(fill=tk.X, pady=(10, 5))

        ttk.Button(buttons_frame, text="📌 Preview", command=self.generate_preview, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="💾 Save", command=self.save_to_file, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="🗑 Clear", command=self.clear_all, style="Clear.TButton").pack(side=tk.RIGHT, padx=5)

        # Status bar
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(left_frame, textvariable=self.status_var, anchor=tk.W, style="Status.TLabel")
        status_bar.pack(fill=tk.X, pady=(5, 0))

        # Right frame - Preview
        right_frame = ttk.LabelFrame(paned_window, text="📌 Preview", padding="10", style="Preview.TLabelframe")
        paned_window.add(right_frame, weight=1)

        self.preview_text = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            height=20,
            bg="#252526",
            fg="white",
            insertbackground="white",
            font=("Courier New", 12),
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        # Set initial status
        self.status_var.set("✅ Ready. Enter question details and generate preview.")

    def configure_styles(self):
        """Configure custom styles for the application"""
        self.style.theme_use("clam")

        # Main Colors
        dark_bg = "#1e1e1e"
        light_bg = "#252526"
        accent_color = "#007acc"
        text_color = "white"

        self.style.configure("TFrame", background=dark_bg)
        self.style.configure("TLabelframe", background=dark_bg, foreground=text_color)
        self.style.configure("TLabel", background=dark_bg, foreground=text_color, font=("Segoe UI", 10))

        self.style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground=accent_color, background=dark_bg)

        self.style.configure("Status.TLabel", font=("Segoe UI", 10, "italic"), foreground="lightgray", background=dark_bg)

        self.style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self.style.configure("Accent.TButton", background=accent_color, foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Accent.TButton", background=[("active", "#005f99")])

        self.style.configure("Clear.TButton", background="#ff4d4d", foreground="white", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Clear.TButton", background=[("active", "#cc0000")])

        self.style.configure("Preview.TLabelframe", background=light_bg, foreground=text_color)

    def create_label_entry(self, parent, label_text, var):
        """Creates a label and entry widget"""
        frame = ttk.LabelFrame(parent, text=label_text, padding="10", style="TLabelframe")
        frame.pack(fill=tk.X, pady=5)
        entry = ttk.Entry(frame, textvariable=var, font=("Segoe UI", 10))
        entry.pack(fill=tk.X, expand=True)

    def create_scrolled_text(self, parent, label_text, height=4):
        """Creates a labeled scrolled text widget"""
        frame = ttk.LabelFrame(parent, text=label_text, padding="10", style="TLabelframe")
        frame.pack(fill=tk.BOTH, expand=True, pady=5)
        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=height, font=("Segoe UI", 10), bg="#252526", fg="white", insertbackground="white")
        text_area.pack(fill=tk.BOTH, expand=True)
        return text_area

    def generate_markdown(self):
        """Generate markdown content from the form inputs"""
        question_name = self.question_name.get().strip()
        question_description = self.description_text.get(1.0, tk.END).strip()
        input_list = self.input_text.get(1.0, tk.END).strip()
        output_list = self.output_text.get(1.0, tk.END).strip()
        cpp_code = self.code_text.get(1.0, tk.END).strip()

        if not question_name:
            messagebox.showwarning("⚠ Warning", "Please enter a question name.")
            return None

        return f"""
# 🔍 {question_name}

## 📝 Description
{question_description}

## 📥 Inputs
{input_list}

## 📤 Outputs
{output_list}

## 💻 Solution
```cpp
{cpp_code}
```
"""
    def generate_preview(self):
        """Generate preview of the markdown content"""
        self.markdown_content = self.generate_markdown()
        if self.markdown_content:
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, self.markdown_content)

    def save_to_file(self):
        """Save the markdown content"""
        file_path = filedialog.asksaveasfilename(defaultextension=".md")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.markdown_content)

    def clear_all(self):
        """Clear all fields"""
        self.question_name.set("")
        self.description_text.delete(1.0, tk.END)
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.code_text.delete(1.0, tk.END)

if __name__ == "__main__": 
    root = tk.Tk() 
    app = MarkdownGeneratorApp(root) 
    root.mainloop()
    



