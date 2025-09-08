import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox


class MarkdownGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Markdown Question Formatter")

        # Set fullscreen as minimum size
        self.root.state("zoomed")  # Maximized on Windows
        self.root.minsize(1920, 1080)  # Fullscreen minimum size

        # Beautiful dark theme background
        self.root.configure(bg="#0d1117")

        # Modern window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # Create style
        self.style = ttk.Style()
        self.configure_styles()

        # Variables
        self.md_file_path = tk.StringVar()
        self.question_name = tk.StringVar()
        self.markdown_content = ""

        # Main frame - Direct layout without scrolling
        main_frame = ttk.Frame(root, style="MainContainer.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Paned window for split view - Direct layout
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Left frame - Input
        left_frame = ttk.Frame(paned_window, padding="10", style="TFrame")
        paned_window.add(left_frame, weight=1)

        # Title with enhanced styling - Compact version
        title_frame = ttk.Frame(left_frame, style="TitleFrame.TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 10))

        title_label = ttk.Label(
            title_frame,
            text="🎨 Markdown Question Formatter",
            font=("Segoe UI", 18, "bold"),
            style="MainTitle.TLabel",
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            title_frame,
            text="Create beautiful markdown documentation for your coding problems",
            font=("Segoe UI", 9),
            style="Subtitle.TLabel",
        )
        subtitle_label.pack(pady=(2, 0))

        # Question Name
        self.create_label_entry(left_frame, "❓ Question Name", self.question_name)

        # Question Description
        self.description_text = self.create_scrolled_text(
            left_frame, "📜 Description", height=4
        )

        # Input List
        self.input_text = self.create_scrolled_text(left_frame, "📥 Examples", height=4)

        # Code Input
        self.code_text = self.create_scrolled_text(left_frame, "💻 C++ Code", height=5)

        # Action buttons with enhanced styling
        buttons_frame = ttk.Frame(left_frame, style="ButtonFrame.TFrame")
        buttons_frame.pack(fill=tk.X, pady=(10, 5))

        # Create button container for better spacing
        button_container = ttk.Frame(buttons_frame, style="ButtonContainer.TFrame")
        button_container.pack(expand=True)

        ttk.Button(
            button_container,
            text="✨ Preview",
            command=self.generate_preview,
            style="Primary.TButton",
        ).pack(side=tk.LEFT, padx=10, pady=5)

        ttk.Button(
            button_container,
            text="💾 Save to File",
            command=self.save_to_file,
            style="Success.TButton",
        ).pack(side=tk.LEFT, padx=10, pady=5)

        ttk.Button(
            button_container,
            text="🗑️ Clear All",
            command=self.clear_all,
            style="Danger.TButton",
        ).pack(side=tk.LEFT, padx=10, pady=5)

        # Enhanced status bar
        status_frame = ttk.Frame(left_frame, style="StatusFrame.TFrame")
        status_frame.pack(fill=tk.X, pady=(5, 0))

        self.status_var = tk.StringVar()
        status_bar = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            anchor=tk.W,
            style="Status.TLabel",
        )
        status_bar.pack(fill=tk.X, padx=10, pady=3)

        # Right frame - Enhanced Preview
        right_frame = ttk.LabelFrame(
            paned_window,
            text="📋 Live Preview",
            padding="10",
            style="Preview.TLabelframe",
        )
        paned_window.add(right_frame, weight=1)

        # Preview text with enhanced styling
        self.preview_text = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            bg="#161b22",
            fg="#e6edf3",
            insertbackground="#f0f6fc",
            font=("Cascadia Code", 11),
            selectbackground="#264f78",
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            padx=12,
            pady=12,
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        # Set initial status with beautiful message
        self.status_var.set(
            "🚀 Ready to create beautiful markdown! Enter your question details and click Preview."
        )

    def configure_styles(self):
        """Configure beautiful modern dark theme styles"""
        self.style.theme_use("clam")

        # GitHub Dark Theme Colors
        github_dark_bg = "#0d1117"
        github_card_bg = "#161b22"
        github_border = "#30363d"
        github_blue = "#58a6ff"
        github_green = "#3fb950"
        github_red = "#f85149"
        github_text = "#e6edf3"
        github_text_secondary = "#8b949e"
        github_accent = "#1f6feb"

        # Main container styles
        self.style.configure(
            "MainContainer.TFrame", background=github_dark_bg, relief="flat"
        )

        self.style.configure(
            "ScrollableFrame.TFrame", background=github_dark_bg, relief="flat"
        )

        self.style.configure(
            "TitleFrame.TFrame", background=github_dark_bg, relief="flat"
        )

        self.style.configure(
            "ButtonFrame.TFrame", background=github_dark_bg, relief="flat"
        )

        self.style.configure(
            "ButtonContainer.TFrame", background=github_dark_bg, relief="flat"
        )

        self.style.configure(
            "StatusFrame.TFrame",
            background=github_card_bg,
            relief="solid",
            borderwidth=1,
        )

        # Frame and Label styles
        self.style.configure("TFrame", background=github_dark_bg, relief="flat")

        self.style.configure(
            "TLabelframe",
            background=github_dark_bg,
            foreground=github_text,
            borderwidth=2,
            relief="solid",
            bordercolor=github_border,
        )

        self.style.configure(
            "TLabelframe.Label",
            background=github_dark_bg,
            foreground=github_blue,
            font=("Segoe UI", 10, "bold"),
        )

        # Text and Label styles
        self.style.configure(
            "TLabel",
            background=github_dark_bg,
            foreground=github_text,
            font=("Segoe UI", 9),
        )

        self.style.configure(
            "MainTitle.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground=github_blue,
            background=github_dark_bg,
        )

        self.style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 9),
            foreground=github_text_secondary,
            background=github_dark_bg,
        )

        self.style.configure(
            "Status.TLabel",
            font=("Segoe UI", 9),
            foreground=github_text,
            background=github_card_bg,
            padding=(10, 5),
        )

        # Entry styles
        self.style.configure(
            "TEntry",
            font=("Segoe UI", 10),
            foreground=github_text,
            fieldbackground=github_card_bg,
            borderwidth=2,
            relief="solid",
            bordercolor=github_border,
            insertcolor=github_text,
        )

        # Button styles
        self.style.configure(
            "Primary.TButton",
            background=github_accent,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 6),
            relief="flat",
            borderwidth=0,
        )
        self.style.map(
            "Primary.TButton",
            background=[("active", "#1158c7"), ("pressed", "#0d419d")],
        )

        self.style.configure(
            "Success.TButton",
            background=github_green,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 6),
            relief="flat",
            borderwidth=0,
        )
        self.style.map(
            "Success.TButton",
            background=[("active", "#2ea043"), ("pressed", "#238636")],
        )

        self.style.configure(
            "Danger.TButton",
            background=github_red,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(15, 6),
            relief="flat",
            borderwidth=0,
        )
        self.style.map(
            "Danger.TButton", background=[("active", "#da3633"), ("pressed", "#b91c1c")]
        )

        # Preview frame styles
        self.style.configure(
            "Preview.TLabelframe",
            background=github_dark_bg,
            foreground=github_text,
            borderwidth=2,
            relief="solid",
            bordercolor=github_border,
        )

    def create_label_entry(self, parent, label_text, var):
        """Creates a beautifully styled label and entry widget"""
        frame = ttk.LabelFrame(
            parent, text=label_text, padding="10", style="TLabelframe"
        )
        frame.pack(fill=tk.X, pady=5)
        entry = ttk.Entry(
            frame, textvariable=var, font=("Segoe UI", 10), style="TEntry"
        )
        entry.pack(fill=tk.X, expand=True, ipady=5)
        return entry

    def create_scrolled_text(self, parent, label_text, height=4):
        """Creates a beautifully styled labeled scrolled text widget"""
        frame = ttk.LabelFrame(
            parent, text=label_text, padding="10", style="TLabelframe"
        )
        frame.pack(fill=tk.BOTH, expand=True, pady=5)

        text_area = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            height=height,
            font=("Cascadia Code", 10),
            bg="#161b22",
            fg="#e6edf3",
            insertbackground="#f0f6fc",
            selectbackground="#264f78",
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10,
        )
        text_area.pack(fill=tk.BOTH, expand=True)
        return text_area

    def generate_markdown(self):
        """Generate markdown content from the form inputs"""
        question_name = self.question_name.get().strip()
        question_description = self.description_text.get(1.0, tk.END).strip()
        example_list = self.input_text.get(1.0, tk.END).strip()
        cpp_code = self.code_text.get(1.0, tk.END).strip()

        if not question_name:
            messagebox.showwarning("⚠ Warning", "Please enter a question name.")
            return None

        return f"""# 🔍 {question_name}

## 📝 Description
{question_description}

## 📥 Examples
```plaintext
{example_list}
```

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
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(self.markdown_content)

    def clear_all(self):
        """Clear all fields"""
        self.question_name.set("")
        self.description_text.delete(1.0, tk.END)
        self.input_text.delete(1.0, tk.END)
        self.code_text.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownGeneratorApp(root)
    root.mainloop()
