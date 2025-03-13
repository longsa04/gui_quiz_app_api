from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        # Window setup
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Score label
        self.score_label = Label(
            text="Score: 0/0", fg="white", bg=THEME_COLOR, font=("Arial", 12, "bold")
        )
        self.score_label.grid(row=0, column=1, sticky="e")

        # Question canvas
        self.canvas = Canvas(width=300, height=250, bg="white", highlightthickness=0)
        self.question_text = self.canvas.create_text(
            150, 125, width=280, text="Welcome to Quizzler!",
            fill=THEME_COLOR, font=("Arial", 20, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # True button
        self.true_image = PhotoImage(file="images/true.png")  # Keep reference
        self.true_button = Button(
            image=self.true_image, highlightthickness=0, command=self.true_pressed
        )
        self.true_button.grid(row=2, column=0)

        # False button
        self.false_image = PhotoImage(file="images/false.png")  # Keep reference
        self.false_button = Button(
            image=self.false_image, highlightthickness=0, command=self.false_pressed
        )
        self.false_button.grid(row=2, column=1)

        # Restart button (initially disabled)
        self.restart_button = Button(
            text="Restart", bg="white", fg=THEME_COLOR, font=("Arial", 10, "bold"),
            command=self.restart_quiz, state="disabled"
        )
        self.restart_button.grid(row=0, column=0, sticky="w")

        # Start the quiz
        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        """Display the next question or end the quiz."""
        self.canvas.config(bg="white")
        self.true_button.config(state="normal")
        self.false_button.config(state="normal")
        self.restart_button.config(state="disabled")

        if self.quiz.still_has_questions():
            self.score_label.config(
                text=f"Score: {self.quiz.score}/{self.quiz.question_number}"
            )
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            final_message = (
                f"Quiz Ended!\n"
                f"Final Score: {self.quiz.score}/{self.quiz.question_number}"
            )
            self.canvas.itemconfig(self.question_text, text=final_message)
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
            self.restart_button.config(state="normal")

    def true_pressed(self):
        """Handle True button press."""
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        """Handle False button press."""
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right):
        """Provide feedback and proceed to the next question."""
        self.canvas.config(bg="green" if is_right else "red")
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")
        self.window.after(1000, self.get_next_question)

    def restart_quiz(self):
        """Restart the quiz from the beginning."""
        self.quiz.reset()
        self.get_next_question()