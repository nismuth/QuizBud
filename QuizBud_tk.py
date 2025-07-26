import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import PhotoImage

class QuizApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.resizable(False, False)
        self.root.title("QuizBud")

        icon = PhotoImage(file="bud-moth.png")  # Window icon
        self.root.iconphoto(True, icon)

        image = Image.open("bgs/green-marble.jpg")
        image = image.resize((600, 300))
        backgroundImage = ImageTk.PhotoImage(image)
        bgLabel = tk.Label(self.root, image=backgroundImage)
        bgLabel.image = backgroundImage
        bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

        self.option = None
        self.name = ""
        self.enter_torf = ""
        self.num_questions = 0
        self.questions = []
        self.answers = []
        self.entries = []

        self.create_option_window()
        self.root.mainloop()

    def create_option_window(self):
        pFrame = tk.Frame(self.root, bd=5, relief=tk.SUNKEN, bg="#165f36")
        pFrame.pack(expand=True, padx=15, pady=15)

        label = tk.Label(pFrame, text="Choose an Activity:", font=("Georgia", 20),
                         fg="white", bg="#45b58c", padx=5, pady=6, relief=tk.RAISED)
        label.pack(pady=(15, 15))

        frame = tk.Frame(pFrame, bd=5, relief=tk.SUNKEN, bg="#45b58c")
        frame.pack(expand=True, padx=15, pady=(0, 15))

        tk.Button(frame, text="QUIZ", command=lambda: self.open_info_window("Quiz"),
                  font=("Georgia", 20), bg="red", fg="white").pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame, text="TEST", command=lambda: self.open_info_window("Test"),
                  font=("Georgia", 20), bg="blue", fg="white").pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame, text="CARDS", command=lambda: self.open_info_window("Flashcards"),
                  font=("Georgia", 20), bg="#c0c53f", fg="white").pack(side=tk.LEFT, padx=5, pady=5)

    def open_info_window(self, selected_option):
        self.option = selected_option
        self.info_win = tk.Toplevel(self.root)
        self.info_win.config(bg="#165f36")
        self.info_win.geometry("260x210")
        self.info_win.resizable(False, False)
        self.info_win.title(f"{selected_option} Setup")

        if self.option == "Flashcards":
            self.enter_torf = "Cards"
        if self.option in ["Quiz" or "Test"]:
            self.enter_torf = "Questions"

        tk.Label(self.info_win, text="Enter Study Topic:", relief=tk.RAISED,
                 padx=4, fg="white", bg="#165f36").pack(pady=(25, 0))
        self.name_entry = tk.Entry(self.info_win)
        self.name_entry.pack(pady=(10, 15))

        tk.Label(self.info_win, text=f"Enter # of {self.enter_torf}:", relief=tk.RAISED,
                 fg="white", bg="#165f36", padx=4).pack()
        self.num_entry = tk.Entry(self.info_win)
        self.num_entry.pack(pady=(10, 10))

        tk.Button(self.info_win, text="Submit", fg="white", bg="#165f36",
                  command=self.collect_info).pack(pady=6)

    def collect_info(self):
        self.name = self.name_entry.get().strip()
        try:
            self.num_questions = int(self.num_entry.get())
            if self.num_questions <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of questions.")
            return

        self.info_win.destroy()
        self.open_question_input_window()

    def open_question_input_window(self):
        self.q_win = tk.Toplevel(self.root)
        self.q_win.title(f"Create Your {self.option} Set")
        self.q_win.geometry("500x500")
        self.q_win.config(bg="#165f36")
        self.root.resizable(False, False)

        canvas = tk.Canvas(self.q_win, bg="#165f36", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.q_win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame = tk.Frame(canvas, bg="#165f36", pady=12)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        self.q_entries = []
        self.a_entries = []

        for i in range(self.num_questions):
            if self.option == "Test" or "Quiz":
                self.term = self.option
                self.defin = self.option
            if self.option == "Flashcards":
                self.term = "Term"
                self.defin = "Definition"

            tk.Label(frame, text=f"{self.term} {i + 1}:", relief=tk.RAISED,
                     padx=4, pady=8, fg="white", bg="#165f36").pack(pady=15)
            q_entry = tk.Entry(frame, width=70)
            q_entry.pack(pady=4, padx=20)
            self.q_entries.append(q_entry)

            tk.Label(frame, text=f"{self.defin} {i + 1}:", relief=tk.RAISED,
                     padx=4, pady=8, fg="white", bg="#165f36").pack(pady=15)
            a_entry = tk.Entry(frame, width=70)
            a_entry.pack(pady=4, padx=20)
            self.a_entries.append(a_entry)

        tk.Button(frame, text="Submit All", relief=tk.RAISED, padx=4, fg="white",
                  bg="#165f36", command=self.collect_questions).pack(pady=15)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)

    def collect_questions(self):
        self.questions = [q.get().strip() for q in self.q_entries]
        self.answers = [a.get().strip() for a in self.a_entries]

        if not all(self.questions) or not all(self.answers):
            messagebox.showerror("Missing Data", "Please fill out all questions and answers.")
            return

        self.q_win.destroy()
        self.display_quiz_window()

    def display_quiz_window(self):
        self.quiz_win = tk.Toplevel(self.root)
        self.quiz_win.title(f"My QuizBud {self.option}")
        self.quiz_win.geometry("500x500")
        self.quiz_win.config(bg="#165f36")
        self.root.resizable(False, False)

        canvas = tk.Canvas(self.quiz_win, bg="#165f36", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.quiz_win, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame = tk.Frame(canvas, bg="#165f36", pady=12)
        canvas.create_window((140, 0), window=frame, anchor="nw")

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        tk.Label(frame, text=f"{self.option} for {self.name}", fg="white", bg="#165f36",
                 font=("Georgia", 20, 'bold')).pack(pady=10, padx=(10, 0))

        self.entries = []
        for i, question in enumerate(self.questions):
            tk.Label(frame, text=f"{i + 1}. {question}", relief=tk.RAISED,
                     bg="#165f36", fg="white", pady=10, padx=10).pack()
            entry = tk.Entry(frame)
            entry.pack(fill='x', expand=True, pady=10)
            self.entries.append(entry)

        tk.Button(frame, text="Submit Answers", command=self.check_answers,
                  bg="#165f36", fg="white").pack(pady=10)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        frame.bind("<Configure>", on_frame_configure)

    def check_answers(self):
        user_answers = [e.get().strip() for e in self.entries]
        correct = sum(1 for ua, a in zip(user_answers, self.answers) if ua.lower() == a.lower())

        grade_response = messagebox.askquestion(
            "Results", f"You got {correct} out of {self.num_questions} correct!\nWould you like to go again?"
        )

        self.quiz_win.destroy()

        if grade_response == 'yes':
            # Reset and show main window again
            for widget in self.root.winfo_children():
                widget.destroy()

            self.option = ""
            self.name = ""
            self.num_questions = 0
            self.questions = []
            self.answers = []
            self.entries = []

            image = Image.open("bgs/green-marble.jpg")
            image = image.resize((600, 300))
            backgroundImage = ImageTk.PhotoImage(image)
            bgLabel = tk.Label(self.root, image=backgroundImage)
            bgLabel.image = backgroundImage
            bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

            self.create_option_window()
        else:
            self.root.quit()


if __name__ == "__main__":
    QuizApp()
