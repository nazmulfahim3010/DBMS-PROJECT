# blog_gui.py
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional

from functions import Blog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MiniBlogApp(ctk.CTk):
    """Modern CustomTkinter client for the MiniBlog backend."""

    def __init__(self):
        super().__init__()
        self.title("Blog Asist")
        # full size window
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        self.geometry(f"{screen_w}x{screen_h}+0+0")
        self.minsize(980, 620)
        #------------------full size window done 
        try:
            self.state("zoomed")
        except Exception:
            pass

        self.blog = Blog()
        self.current_view: Optional[str] = None
        self.nav_buttons: dict[str, ctk.CTkButton] = {}
        self.dashboard_search_var = ctk.StringVar()
        self.community_search_var = ctk.StringVar()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_rowconfigure(6, weight=1)

        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nswe")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)
        self.content.grid_rowconfigure(2, weight=1)

        self._build_sidebar()
        self.show_login()

    # ------ UI helpers
    def _build_sidebar(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.sidebar, text="MiniBlog", font=("Montserrat", 26, "bold")
        ).grid(row=0, column=0, padx=25, pady=(30, 8), sticky="w")

        subtitle = (
            f"Welcome\n{self.blog.user_name}"
            if self.blog.user_id
            else "Create,Explore and share."
        )
        ctk.CTkLabel(
            self.sidebar, text=subtitle, font=("Montserrat", 14), text_color="#b7bec8"
        ).grid(row=1, column=0, padx=25, pady=(0, 25), sticky="w")

        self.nav_buttons = {}

        start_row = 2
        if self.blog.user_id:
            buttons = [
                ("Dashboard", self.show_dashboard, "dashboard"),
                ("Add Blog", self.show_add_blog, "add_blog"),
                ("All Blogs", self.show_blog_feed, "blog_feed"),
                ("Recycle Bin", self.show_recycle_bin, "recycle_bin"),
                ("Account", self.show_account_view, "account"),
            ]

            # Add admin button if user is admin
            try:
                if self.blog.is_admin():
                    # insert admin before "Account"
                    buttons.insert(-1, ("Admin Panel", self.show_admin_panel, "admin"))
            except Exception:
                # don't break the sidebar if role check fails
                pass
        else:
            buttons = [
                ("Login", self.show_login, "login"),
                ("Register", self.show_register, "register"),
            ]

        for idx, (text, command, key) in enumerate(buttons, start=start_row):
            is_active = self.current_view == key
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                width=180,
                height=42,
                corner_radius=12,
                fg_color="#2563eb" if is_active else "#1f2937",
                hover_color="#1d4ed8",
                border_width=1,
                border_color="#0f172a",
                state="disabled" if is_active else "normal",
            )
            btn.grid(row=idx, column=0, padx=25, pady=(0, 12), sticky="we")
            self.nav_buttons[key] = btn

        if self.blog.user_id:
            ctk.CTkButton(
                self.sidebar,
                text="Logout",
                fg_color="#ef4444",
                hover_color="#b91c1c",
                command=self.logout_action,
            ).grid(row=7, column=0, padx=25, pady=25, sticky="we")
        else:
            ctk.CTkLabel(
                self.sidebar,
                text="Need an account?\nTap Register to start.",
                font=("Montserrat", 12),
                text_color="#94a3b8",
            ).grid(row=7, column=0, padx=25, pady=25, sticky="w")

    def _select_view(self, view_name: str):
        self.current_view = view_name
        self._build_sidebar()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    

    def _format_timestamp(self, value) -> str:
        if not value:
            return ""
        try:
            return value.strftime("%b %d, %Y %I:%M %p")
        except AttributeError:
            return str(value)

    def clear_dashboard_search(self):
        self.dashboard_search_var.set("")
        self.show_dashboard()

    def clear_community_search(self):
        self.community_search_var.set("")
        self.show_blog_feed()

    def _ensure_logged_in(self) -> bool:
        if not self.blog.user_id:
            messagebox.showinfo("Login required", "Please log in to continue.")
            self.show_login()
            return False
        return True

    # ---- Auth pages
    def show_login(self):
        self._select_view("login")
        self.clear_content()

        card = ctk.CTkFrame(self.content, corner_radius=16, border_width=1, width=420)
        card.grid(row=0, column=0, padx=40, pady=40, sticky="n")

        ctk.CTkLabel(card, text="Welcome back", font=("Montserrat", 26, "bold")).pack(
            pady=(30, 5)
        )
        ctk.CTkLabel(
            card, text="Enter your credentials to continue.", font=("Montserrat", 14)
        ).pack(pady=(0, 25))

        self.login_user = ctk.CTkEntry(
            card, width=320, placeholder_text="Username", font=("Montserrat", 14)
        )
        self.login_user.pack(pady=12)

        self.login_pass = ctk.CTkEntry(
            card,
            width=320,
            placeholder_text="Password",
            show="*",
            font=("Montserrat", 14),
        )
        self.login_pass.pack(pady=12)

        ctk.CTkButton(
            card, text="Log in", width=200, height=42, command=self.login_action
        ).pack(pady=(20, 8))

        ctk.CTkButton(
            card,
            text="Create an account",
            fg_color="transparent",
            border_width=1,
            text_color="#2563eb",
            command=self.show_register,
        ).pack(pady=(0, 25))

    def show_register(self):
        self._select_view("register")
        self.clear_content()

        card = ctk.CTkFrame(self.content, corner_radius=16, border_width=1)
        card.grid(row=0, column=0, padx=40, pady=30, sticky="n")

        ctk.CTkLabel(
            card, text="Create your profile", font=("Montserrat", 24, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(25, 5))

        ctk.CTkLabel(
            card, text="We just need a few details.", font=("Montserrat", 14)
        ).grid(row=1, column=0, columnspan=2, pady=(0, 20))

        entries = [
            ("First Name", "fn"),
            ("Last Name", "ln"),
            ("Email", "email"),
            ("Contact Number", "contact"),
            ("Short Bio", "bio"),
            ("Username", "un"),
            ("Password", "pw"),
        ]

        self.fn = self.ln = self.email = self.contact = self.bio = self.un = self.pw = None

        entry_widgets = {}
        for idx, (placeholder, attr) in enumerate(entries, start=2):
            show = "*" if placeholder == "Password" else None
            entry = ctk.CTkEntry(
                card,
                width=320,
                placeholder_text=placeholder,
                show=show,
                font=("Montserrat", 13),
            )
            entry.grid(row=idx, column=0, columnspan=2, pady=6, padx=30)
            entry_widgets[attr] = entry

        self.fn = entry_widgets["fn"]
        self.ln = entry_widgets["ln"]
        self.email = entry_widgets["email"]
        self.contact = entry_widgets["contact"]
        self.bio = entry_widgets["bio"]
        self.un = entry_widgets["un"]
        self.pw = entry_widgets["pw"]

        ctk.CTkButton(
            card, text="Register", width=220, height=44, command=self.register_action
        ).grid(row=idx + 1, column=0, columnspan=2, pady=(20, 10))

        ctk.CTkButton(
            card,
            text="Back to login",
            fg_color="transparent",
            border_width=1,
            text_color="#94a3b8",
            command=self.show_login,
        ).grid(row=idx + 2, column=0, columnspan=2, pady=(0, 25))

    # --------------- Dashboard
    def show_dashboard(self):
        if not self._ensure_logged_in():
            return

        self._select_view("dashboard")
        self.clear_content()
        self._build_sidebar()

        # ---------- HEADER ----------
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="we", padx=25, pady=(25, 10))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text=f"Your blogs, {self.blog.user_name}",
            font=("Montserrat", 24, "bold"),
        ).grid(row=0, column=0, sticky="w")

        def force_refresh():
            self.dashboard_search_var.set("")
            self.show_dashboard()

        actions = ctk.CTkFrame(header, fg_color="transparent")
        actions.grid(row=0, column=1, sticky="e")
        ctk.CTkButton(actions, text="New Blog", width=140,
                    command=self.show_add_blog).pack(side="left", padx=(0, 10))
        ctk.CTkButton(actions, text="Refresh", width=120,
                    command=force_refresh).pack(side="left")

        # ---------- SEARCH BAR ----------
        search_row = ctk.CTkFrame(header, fg_color="transparent")
        search_row.grid(row=1, column=0, columnspan=2, sticky="we", pady=(12, 0))
        search_row.grid_columnconfigure(0, weight=1)

        entry = ctk.CTkEntry(
            search_row,
            textvariable=self.dashboard_search_var,
            placeholder_text="Search your blogs by title...",
            font=("Montserrat", 13),
        )
        entry.grid(row=0, column=0, sticky="we", padx=(0, 10))
        entry.bind("<Return>", lambda _e: self.show_dashboard())

        ctk.CTkButton(search_row, text="Search", width=100,
                    command=self.show_dashboard).grid(row=0, column=1, padx=(0, 8))
        ctk.CTkButton(search_row, text="Clear", width=90,
                    fg_color="#374151", hover_color="#1f2937",
                    command=self.clear_dashboard_search).grid(row=0, column=2)

        # ---------- ALWAYS UPDATE DASHBOARD STATISTICS ----------
        stats = self.blog.get_user_statistics()

        stats_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        stats_frame.grid(row=1, column=0, sticky="we", padx=25, pady=(5, 20))
        for col in range(3):
            stats_frame.grid_columnconfigure(col, weight=1, uniform="stats")

        stat_cards = [
            ("Your Posts", stats["user_posts"], "#1d4ed8"),
            ("Recycle Bin", stats["trash_posts"], "#f97316"),
            ("Community Posts", stats["community_posts"], "#22c55e"),
            ("Your Comments", stats["user_comments"], "#06b6d4"),
            ("Likes Received", stats["likes_received"], "#16a34a"),
            ("Dislikes Received", stats["dislikes_received"], "#dc2626"),
        ]

        row = 0
        col = 0
        for label, value, color in stat_cards:
            card = ctk.CTkFrame(stats_frame, corner_radius=14, border_width=1)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="we")

            ctk.CTkLabel(
                card, text=label, font=("Montserrat", 13),
                text_color="#94a3b8"
            ).pack(anchor="w", padx=18, pady=(10, 2))

            ctk.CTkLabel(
                card, text=str(value),
                font=("Montserrat", 26, "bold"),
                text_color=color
            ).pack(anchor="w", padx=18, pady=(0, 12))

            col += 1
            if col == 3:
                col = 0
                row += 1

        # ---------- ALWAYS REFRESH BLOG LIST ----------
        blogs = self.blog.view_user_blogs() or []
        blogs = blogs.copy()

        search = (self.dashboard_search_var.get() or "").strip().lower()
        if search:
            blogs = [b for b in blogs if search in (b.get("title") or "").lower()]

        list_frame = ctk.CTkScrollableFrame(self.content)
        list_frame.grid(row=2, column=0, sticky="nsew", padx=25, pady=(0, 25))

        if not blogs:
            ctk.CTkLabel(
                list_frame,
                text="No blogs found." if search else "No posts yet.\nTap “New Blog” to publish your first story.",
                font=("Montserrat", 16),
                text_color="#94a3b8"
            ).pack(pady=120)
            return

        for blog in blogs:
            card = ctk.CTkFrame(list_frame, corner_radius=16)
            card.pack(fill="x", pady=12, padx=12)

            ctk.CTkLabel(card, text=blog["title"],
                        font=("Montserrat", 18, "bold")).pack(anchor="w", padx=18, pady=(12, 4))

            preview = (blog["main_blog"] or "").strip()
            preview = preview[:320] + "..." if len(preview) > 320 else preview

            ctk.CTkLabel(
                card, text=preview, font=("Montserrat", 13),
                wraplength=860, text_color="#e2e8f0", justify="left"
            ).pack(anchor="w", padx=18, pady=(0, 12))

            btn_row = ctk.CTkFrame(card, fg_color="transparent")
            btn_row.pack(fill="x", padx=18, pady=(0, 14))

            ctk.CTkButton(
                btn_row, text="View", width=130,
                command=lambda b=blog: self.show_blog_detail(b, source="dashboard")
            ).pack(side="left", padx=(0, 8))

            ctk.CTkButton(
                btn_row, text="Edit", width=90,
                command=lambda b=blog: self.show_edit_blog(b)
            ).pack(side="left", padx=(0, 8))

            ctk.CTkButton(
                btn_row, text="Delete", width=90,
                fg_color="#ef4444", hover_color="#b91c1c",
                command=lambda bid=blog["id"]: self.delete_blog(bid)
            ).pack(side="left")




    # ------- Blog forms
    def show_add_blog(self):
        if not self._ensure_logged_in():
            return
        self._select_view("add_blog")
        self.clear_content()

        frame = ctk.CTkFrame(self.content, corner_radius=16, border_width=1)
        frame.grid(row=0, column=0, padx=40, pady=30, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="New blog post", font=("Montserrat", 24, "bold")).grid(
            row=0, column=0, sticky="w", padx=20, pady=(25, 5)
        )
        ctk.CTkLabel(
            frame, text="Share something new with the world.", font=("Montserrat", 13)
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 20))

        self.blog_title = ctk.CTkEntry(
            frame,
            width=640,
            placeholder_text="Use catchy blog title",
            font=("Montserrat", 14),
        )
        self.blog_title.grid(row=2, column=0, padx=20, pady=10, sticky="we")

        self.blog_text = ctk.CTkTextbox(frame, width=640, height=320, font=("Consolas", 13))
        self.blog_text.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.grid(row=4, column=0, sticky="e", padx=20, pady=(10, 25))

        ctk.CTkButton(
            btn_row, text="Cancel", fg_color="gray", hover_color="#4b5563", command=self.show_dashboard
        ).pack(side="right", padx=6)
        ctk.CTkButton(btn_row, text="Publish", command=self.add_blog_action).pack(
            side="right", padx=6
        )

    def show_edit_blog(self, blog):
        if not self._ensure_logged_in():
            return
        self.clear_content()
        self._select_view("add_blog")

        frame = ctk.CTkFrame(self.content, corner_radius=16, border_width=1)
        frame.grid(row=0, column=0, padx=40, pady=30, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="Edit blog", font=("Montserrat", 24, "bold")).grid(
            row=0, column=0, sticky="w", padx=20, pady=(25, 5)
        )

        self.edit_title = ctk.CTkEntry(frame, width=640, font=("Montserrat", 14))
        self.edit_title.insert(0, blog["title"])
        self.edit_title.grid(row=1, column=0, padx=20, pady=10, sticky="we")

        self.edit_text = ctk.CTkTextbox(frame, width=640, height=320, font=("Consolas", 13))
        self.edit_text.insert("1.0", blog["main_blog"])
        self.edit_text.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.grid(row=3, column=0, sticky="e", padx=20, pady=(10, 25))

        ctk.CTkButton(
            btn_row, text="Back", fg_color="gray", hover_color="#4b5563", command=self.show_dashboard
        ).pack(side="right", padx=6)
        ctk.CTkButton(
            btn_row,
            text="Update",
            command=lambda bid=blog["id"]: self.update_blog_action(bid),
        ).pack(side="right", padx=6)

    def show_blog_detail(self, blog, source="dashboard"):
        if not self._ensure_logged_in():
            return

        back_action = self.show_dashboard if source == "dashboard" else self.show_blog_feed
        self._select_view(source)
        self.clear_content()

        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(wrapper, fg_color="transparent")
        header.grid(row=0, column=0, sticky="we")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            header,
            text="← Back",
            width=160,
            command=back_action,
        ).grid(row=0, column=0, sticky="w")

        is_owner = blog.get("created_by") == self.blog.user_id
        if is_owner:
            action_row = ctk.CTkFrame(header, fg_color="transparent")
            action_row.grid(row=0, column=1, sticky="e")
            ctk.CTkButton(
                action_row,
                text="Edit",
                width=100,
                command=lambda b=blog: self.show_edit_blog(b),
            ).pack(side="left", padx=(0, 8))
            ctk.CTkButton(
                action_row,
                text="Delete",
                width=110,
                fg_color="#ef4444",
                hover_color="#b91c1c",
                command=lambda bid=blog["id"]: self.delete_blog(bid),
            ).pack(side="left")

        detail_frame = ctk.CTkFrame(wrapper, corner_radius=18, border_width=1)
        detail_frame.grid(row=1, column=0, sticky="nsew")
        detail_frame.grid_columnconfigure(0, weight=1)
        detail_frame.grid_rowconfigure(4, weight=1)

        author = blog.get("first_name") or blog.get("user_name") or self.blog.user_name or "You"
        if blog.get("last_name"):
            author = f'{blog["first_name"]} {blog["last_name"]}'

        ctk.CTkLabel(
            detail_frame,
            text=blog["title"],
            font=("Montserrat", 28, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=28, pady=(28, 8))

        meta = f'By {author} • {self._format_timestamp(blog.get("created_at"))}'
        ctk.CTkLabel(
            detail_frame,
            text=meta,
            font=("Montserrat", 13),
            text_color="#94a3b8",
        ).grid(row=1, column=0, sticky="w", padx=28)

        reaction_frame = ctk.CTkFrame(detail_frame, fg_color="transparent")
        reaction_frame.grid(row=2, column=0, sticky="we", padx=28, pady=(12, 0))
        reaction_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="react")

        stats_label = ctk.CTkLabel(reaction_frame, text="", font=("Montserrat", 12))
        stats_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 6))

        like_btn = ctk.CTkButton(
            reaction_frame,
            text="👍 Like",
            width=160,
            command=lambda: react("like"),
        )
        like_btn.grid(row=1, column=0, sticky="w")

        dislike_btn = ctk.CTkButton(
            reaction_frame,
            text="👎 Dislike",
            width=160,
            fg_color="#1f2937",
            command=lambda: react("dislike"),
        )
        dislike_btn.grid(row=1, column=1, sticky="w", padx=(12, 0))

        def refresh_reactions():
            #-- like / dislike calculation 
            summary = self.blog.get_reaction_summary(blog["id"]) or {}
            likes = summary.get("likes", 0)
            dislikes = summary.get("dislikes", 0)
            total = likes + dislikes
            like_percent = round((likes / total) * 100, 1) if total else 0
            dislike_percent = round((dislikes / total) * 100, 1) if total else 0
            stats_label.configure(
                text=f"Reactions • Likes: {likes} ({like_percent}%)   |   Dislikes: {dislikes} ({dislike_percent}%)"
            )
            user_reaction = summary.get("user_reaction")
            like_btn.configure(
                fg_color="#22c55e" if user_reaction == "like" else "#1f2937",
                text=f"👍 Like ({likes})",
            )
            dislike_btn.configure(
                fg_color="#ef4444" if user_reaction == "dislike" else "#1f2937",
                text=f"👎 Dislike ({dislikes})",
            )

        def react(value):
            if self.handle_reaction(blog["id"], value):
                refresh_reactions()

        refresh_reactions()

        text_box = ctk.CTkTextbox(detail_frame, font=("Consolas", 13), wrap="word", height=260)
        text_box.insert("1.0", blog.get("main_blog") or "")
        text_box.configure(state="disabled")
        text_box.grid(row=3, column=0, padx=28, pady=(12, 4), sticky="we")

        comments_frame = ctk.CTkScrollableFrame(detail_frame)
        comments_frame.grid(row=4, column=0, padx=28, pady=(4, 12), sticky="nsew")

        input_row = ctk.CTkFrame(detail_frame, fg_color="transparent")
        input_row.grid(row=5, column=0, padx=28, pady=(0, 28), sticky="we")
        input_row.grid_columnconfigure(0, weight=1)

        comment_entry = ctk.CTkEntry(
            input_row,
            placeholder_text="Share your thoughts...",
            font=("Montserrat", 13),
        )
        comment_entry.grid(row=0, column=0, sticky="we", padx=(0, 12))

        ctk.CTkButton(
            input_row,
            text="Post comment",
            width=150,
            command=lambda: self.submit_comment(blog["id"], comment_entry, comments_frame),
        ).grid(row=0, column=1)

        self.populate_comments(blog["id"], comments_frame)

    # ------------------------------------------------------------------ Actions
    def register_action(self):
        values = [
            self.fn.get().strip(),
            self.ln.get().strip(),
            self.contact.get().strip(),
            self.email.get().strip(),
            self.bio.get().strip(),
            self.un.get().strip(),
            self.pw.get().strip(),
        ]
        if not all(values):
            messagebox.showwarning("Missing info", "All fields are required.")
            return

        ok, err = self.blog.create_account(*values)
        if ok:
            messagebox.showinfo("Success", "Account created! You are now logged in.")
            # profile set in create_account: show dashboard
            self.show_dashboard()
        else:
            messagebox.showerror("Error", err or "Username already exists or database error.")

    def login_action(self):
        username = self.login_user.get().strip()
        password = self.login_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("Missing info", "Enter both username and password.")
            return
        if self.blog.log_in(username, password):
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def add_blog_action(self):
        title = self.blog_title.get().strip()
        main_blog = self.blog_text.get("1.0", "end").strip()
        if not title or not main_blog:
            messagebox.showwarning("Missing info", "Title and content cannot be empty.")
            return
        if self.blog.add_blog(title, main_blog):
            messagebox.showinfo("Published", "Your blog has been posted.")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Failed to save blog.")

    def update_blog_action(self, blog_id):
        title = self.edit_title.get().strip()
        main_blog = self.edit_text.get("1.0", "end").strip()
        if not title or not main_blog:
            messagebox.showwarning("Missing info", "Title and content cannot be empty.")
            return
        if self.blog.update_blog(blog_id, title, main_blog):
            messagebox.showinfo("Updated", "Blog updated successfully.")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Could not update this blog.")

    def delete_blog(self, blog_id):
        if not messagebox.askyesno("Confirm delete", "Delete this blog?"):
            return
        if self.blog.soft_delete_blog(blog_id):
            messagebox.showinfo("Deleted", "Blog moved to trash.")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Failed to delete blog.")

    # ------- Recycle bin
    def show_recycle_bin(self):
        if not self._ensure_logged_in():
            return
        self._select_view("recycle_bin")
        self.clear_content()

        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="we", padx=25, pady=(25, 10))
        ctk.CTkLabel(
            header, text="Recycle Bin", font=("Montserrat", 24, "bold")
        ).grid(row=0, column=0, sticky="w")

        trashed = self.blog.view_deleted_blogs() or []
        list_frame = ctk.CTkScrollableFrame(self.content)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 25))

        if not trashed:
            ctk.CTkLabel(
                list_frame,
                text="Recycle bin is empty.",
                font=("Montserrat", 16),
                text_color="#94a3b8",
            ).pack(pady=80)
            return

        for blog in trashed:
            card = ctk.CTkFrame(list_frame, corner_radius=16)
            card.pack(fill="x", expand=True, pady=12, padx=12)

            ctk.CTkLabel(
                card, text=blog["title"], font=("Montserrat", 18, "bold")
            ).pack(anchor="w", padx=18, pady=(14, 4))

            ctk.CTkLabel(
                card,
                text="Created on: " + self._format_timestamp(blog.get("created_at")),
                font=("Montserrat", 12),
                text_color="#94a3b8",
            ).pack(anchor="w", padx=18)

            btn_row = ctk.CTkFrame(card, fg_color="transparent")
            btn_row.pack(fill="x", padx=18, pady=(8, 14))

            ctk.CTkButton(
                btn_row,
                text="Restore",
                width=120,
                command=lambda bid=blog["id"]: self.restore_blog_action(bid),
            ).pack(side="left", padx=(0, 12))

            ctk.CTkButton(
                btn_row,
                text="Delete forever",
                width=140,
                fg_color="#ef4444",
                hover_color="#b91c1c",
                command=lambda bid=blog["id"]: self.permanent_delete_action(bid),
            ).pack(side="left")

    def restore_blog_action(self, blog_id):
        if self.blog.restore_blog(blog_id):
            messagebox.showinfo("Restored", "Blog restored to dashboard.")
            self.show_recycle_bin()
        else:
            messagebox.showerror("Error", "Unable to restore blog.")

    def permanent_delete_action(self, blog_id):
        if not messagebox.askyesno("Permanent delete", "Delete this blog permanently?"):
            return
        if self.blog.permanent_delete_blog(blog_id):
            messagebox.showinfo("Deleted", "Blog removed permanently.")
            self.show_recycle_bin()
        else:
            messagebox.showerror("Error", "Unable to delete blog.")

    # ------------------------------------------------------------------ Blog feed
    def show_blog_feed(self):
        if not self._ensure_logged_in():
            return
        self._select_view("blog_feed")
        self.clear_content()

        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="we", padx=25, pady=(25, 10))
        header.grid_columnconfigure(0, weight=1)
        header.grid_rowconfigure(1, weight=0)
        ctk.CTkLabel(
            header,
            text="Community blogs",
            font=("Montserrat", 24, "bold"),
        ).grid(row=0, column=0, sticky="w")

        search_row = ctk.CTkFrame(header, fg_color="transparent")
        search_row.grid(row=1, column=0, columnspan=2, sticky="we", pady=(12, 0))
        search_row.grid_columnconfigure(0, weight=1)

        community_entry = ctk.CTkEntry(
            search_row,
            textvariable=self.community_search_var,
            placeholder_text="Search community posts by title...",
            font=("Montserrat", 13),
        )
        community_entry.grid(row=0, column=0, sticky="we", padx=(0, 10))
        community_entry.bind("<Return>", lambda _event: self.show_blog_feed())

        ctk.CTkButton(
            search_row,
            text="Search",
            width=100,
            command=self.show_blog_feed,
        ).grid(row=0, column=1, padx=(0, 8))

        ctk.CTkButton(
            search_row,
            text="Clear",
            width=90,
            fg_color="#374151",
            hover_color="#1f2937",
            command=self.clear_community_search,
        ).grid(row=0, column=2)

        blogs = self.blog.get_all_blogs() or []
        community_term = (self.community_search_var.get() or "").strip().lower()
        if community_term:
            blogs = [
                blog
                for blog in blogs
                if community_term in (blog.get("title") or "").lower()
            ]

        list_frame = ctk.CTkScrollableFrame(self.content)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 25))

        if not blogs:
            empty = (
                "No blogs match your search."
                if community_term
                else "No blogs yet. Check back soon!"
            )
            ctk.CTkLabel(
                list_frame,
                text=empty,
                font=("Montserrat", 16),
                text_color="#94a3b8",
            ).pack(pady=120)
            return

        for blog in blogs:
            card = ctk.CTkFrame(list_frame, corner_radius=16)
            card.pack(fill="x", expand=True, pady=12, padx=12)

            author = blog.get("first_name") or blog.get("user_name") or "Unknown"
            if blog.get("last_name"):
                author = f'{blog["first_name"]} {blog["last_name"]}'
            subtitle = f'By {author} • {self._format_timestamp(blog.get("created_at"))}'

            ctk.CTkLabel(
                card, text=blog["title"], font=("Montserrat", 19, "bold")
            ).pack(anchor="w", padx=18, pady=(16, 4))
            ctk.CTkLabel(
                card,
                text=subtitle,
                font=("Montserrat", 12),
                text_color="#94a3b8",
            ).pack(anchor="w", padx=18)

            preview = (blog["main_blog"] or "").strip()
            if len(preview) > 320:
                preview = preview[:320].rstrip() + "..."
            ctk.CTkLabel(
                card,
                text=preview,
                font=("Montserrat", 13),
                wraplength=860,
                justify="left",
            ).pack(anchor="w", padx=18, pady=(8, 12))

            ctk.CTkButton(
                card,
                text="View & interact",
                width=160,
                command=lambda b=blog: self.show_blog_detail(b, source="blog_feed"),
            ).pack(anchor="e", padx=18, pady=(0, 16))

    def populate_comments(self, blog_id, container):
        for widget in container.winfo_children():
            widget.destroy()
        comments = self.blog.get_comments(blog_id) or []
        if not comments:
            ctk.CTkLabel(
                container,
                text="No comments yet. Be the first!",
                font=("Montserrat", 12),
                text_color="#94a3b8",
            ).pack(pady=10, padx=10)
            return
        for comment in comments:
            block = ctk.CTkFrame(container, corner_radius=10)
            block.pack(fill="x", padx=10, pady=6)
            author = comment.get("first_name") or comment.get("user_name") or "User"
            if comment.get("last_name"):
                author = f'{comment["first_name"]} {comment["last_name"]}'
            ctk.CTkLabel(
                block,
                text=f'{author} • {self._format_timestamp(comment.get("created_at"))}',
                font=("Montserrat", 11, "bold"),
            ).pack(anchor="w", padx=12, pady=(10, 4))
            ctk.CTkLabel(
                block,
                text=comment["comment_text"],
                font=("Montserrat", 12),
                wraplength=560,
                justify="left",
            ).pack(anchor="w", padx=12, pady=(0, 10))

    def submit_comment(self, blog_id, entry_widget, comments_frame):
        if not self._ensure_logged_in():
            return
        text = entry_widget.get().strip()
        if not text:
            messagebox.showwarning("Empty comment", "Please write a comment first.")
            return
        if self.blog.add_comment(blog_id, text):
            entry_widget.delete(0, "end")
            self.populate_comments(blog_id, comments_frame)
        else:
            messagebox.showerror("Error", "Failed to post comment.")

    def handle_reaction(self, blog_id, reaction: str) -> bool:
        if not self._ensure_logged_in():
            return False
        if self.blog.set_reaction(blog_id, reaction):
            return True
        messagebox.showerror("Error", "Unable to update reaction.")
        return False

    def logout_action(self):
        self.blog.clear_session()
        self.show_login()

    # ------------------------------------------------------------------ Account
    def show_account_view(self):
        if not self._ensure_logged_in():
            return
        profile = self.blog.get_user_profile()
        if not profile:
            messagebox.showerror("Error", "Unable to load profile.")
            return
        self._select_view("account")
        self.clear_content()

        container = ctk.CTkFrame(self.content, corner_radius=16, border_width=1)
        container.grid(row=0, column=0, padx=40, pady=30, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            container,
            text="Account overview",
            font=("Montserrat", 26, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(25, 6))
        ctk.CTkLabel(
            container,
            text="Manage your profile details.",
            font=("Montserrat", 13),
            text_color="#94a3b8",
        ).grid(row=1, column=0, sticky="w", padx=25, pady=(0, 20))

        info_items = [
            ("Username", profile.get("user_name", "")),
            ("Name", f'{profile.get("first_name", "")} {profile.get("last_name", "")}'.strip()),
            ("Email", profile.get("email", "")),
            ("Contact", profile.get("contact", "")),
            ("Bio", profile.get("bio", "")),
            ("Joined", self._format_timestamp(profile.get("created_at"))),
        ]

        info_scroll = ctk.CTkScrollableFrame(container, width=720)
        info_scroll.grid(row=2, column=0, padx=25, pady=(0, 25), sticky="nsew")
        info_scroll.grid_columnconfigure(0, weight=1)

        for idx, (label, value) in enumerate(info_items, start=0):
            frame = ctk.CTkFrame(info_scroll, corner_radius=12)
            frame.grid(row=idx, column=0, padx=0, pady=6, sticky="we")
            ctk.CTkLabel(frame, text=label, font=("Montserrat", 12, "bold")).pack(
                anchor="w", padx=18, pady=(12, 2)
            )
            ctk.CTkLabel(
                frame,
                text=value or "—",
                font=("Montserrat", 12),
                text_color="#e2e8f0",
                wraplength=520,
                justify="left",
            ).pack(anchor="w", padx=18, pady=(0, 12))

    # ------------------------------------------------------------------ Admin Panel
    def show_admin_panel(self):
        if not self._ensure_logged_in():
            return
        # only allow admins
        try:
            if not self.blog.is_admin():
                messagebox.showerror("Access denied", "You are not an admin.")
                return
        except Exception:
            messagebox.showerror("Error", "Unable to verify admin status.")
            return

        self._select_view("admin")
        self.clear_content()

        container = ctk.CTkFrame(self.content, corner_radius=16, border_width=1)
        container.grid(row=0, column=0, padx=40, pady=30, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(container, text="Admin Panel", font=("Montserrat", 26, "bold")).grid(
            row=0, column=0, sticky="w", padx=25, pady=(25, 6)
        )

        # Users list frame
        users_frame = ctk.CTkScrollableFrame(container)
        users_frame.grid(row=1, column=0, padx=25, pady=(10, 25), sticky="nsew")
        users_frame.grid_columnconfigure(0, weight=1)

        users = self.blog.list_users() or []
        if not users:
            ctk.CTkLabel(users_frame, text="No users found.", font=("Montserrat", 12), text_color="#94a3b8").pack(pady=12)
            return

        for u in users:
            row = ctk.CTkFrame(users_frame, corner_radius=10)
            row.pack(fill="x", padx=12, pady=8)
            name = f'{u.get("first_name") or ""} {u.get("last_name") or ""}'.strip()
            name = name or u.get("user_name") or "User"
            ctk.CTkLabel(row, text=f'{u.get("id")} • {name} • {u.get("user_name")} • {u.get("role")}', font=("Montserrat", 12, "bold")).pack(anchor="w", padx=12, pady=8)

            btn_row = ctk.CTkFrame(row, fg_color="transparent")
            btn_row.pack(anchor="e", padx=12, pady=(6, 10))
            # Promote / Demote
            if u.get("role") != "admin":
                ctk.CTkButton(btn_row, text="Make Admin", width=120, command=lambda uid=u["id"]: self._admin_set_role(uid, "admin")).pack(side="left", padx=(0,8))
            else:
                ctk.CTkButton(btn_row, text="Revoke Admin", width=120, fg_color="#ef4444", hover_color="#b91c1c", command=lambda uid=u["id"]: self._admin_set_role(uid, "user")).pack(side="left", padx=(0,8))

    def _admin_set_role(self, user_id, role):
        if not messagebox.askyesno("Confirm", f"Set user {user_id} role to {role}?"):
            return
        if self.blog.set_user_role(user_id, role):
            messagebox.showinfo("Success", "Role updated.")
            self.show_admin_panel()
        else:
            messagebox.showerror("Error", "Unable to update role.")

if __name__ == "__main__":
    app = MiniBlogApp()
    app.mainloop()
