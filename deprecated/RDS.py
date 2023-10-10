import tkinter as tk
import random

class DigitSpanTest:
    def __init__(self, master):
        """
        Initialize the DigitSpanTest application.

        Args:
            master (tk.Tk): The master Tkinter window.
        """
        self.master = master
        self.master.title("Digit Span Test for Working Memory Evaluation")

        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry(f"{self.width}x{self.height}")

        self.canvas = tk.Canvas(self.master, bg='#FDF5E6')
        self.canvas.pack(fill='both', expand=True)

        self.ask_for_id()

    def ask_for_id(self):
        """
        Create a screen to ask for the user's ID.
        """
        self.canvas.delete('all')
        label = self.canvas.create_text(self.width/2, self.height/2.3, fill='darkblue', font='Arial 26', text="Please enter your ID:", justify='c')
        self.id_entry = tk.Entry(self.master, font=('Arial', 32))
        e = self.canvas.create_window(self.width/2, self.height/2, window=self.id_entry)
        self.id_entry.bind('<Return>', self.start_intro)

    def start_intro(self, event=None):
        """
        Start the introduction phase of the test.

        Args:
            event: Event object (default is None).
        """
        self.user_id = self.id_entry.get().strip()
        if not self.user_id:
            return  # Don't proceed without ID

        self.canvas.delete('all')
        title_text = "Digit Span Test for Working Memory Evaluation"
        self.canvas.create_text(self.width/2, self.height/4.5, fill='darkblue', font='Arial 52', text=title_text, justify='c')

        docs = ("This is a Digit Span Test that evaluates working memory performance.\n"
                "Try to remember the digits in the order that they are presented and \n"
                "repeat them once the sequence has stopped. \n"
                "If successful, the length of the sequence will increase by 1. \n\n"
                "We will start out with 2 digits. \n"
                "Click 'Start' or press 'Enter' if you are ready to start the test.")
        self.canvas.create_text(self.width/2, self.height/2.2, fill='darkblue', font='Arial 36', text=docs, justify='c')

        self.start_btn = tk.Button(self.master, text="Start", font='Arial 24', fg='black', bg='#4682B4', activebackground='#36648B', activeforeground='white', command=self.start_test)
        self.canvas.create_window(self.width/2, self.height/1.4, window=self.start_btn)

        self.forward = True
        self.sequence_length = 2
        self.sequence_attempts = 0
        self.correct_attempts = 0
        self.score = 0

    def start_test(self):
        """
        Start the Digit Span Test.
        """
        self.start_btn.destroy()
        self.run_test()

    def run_test(self):
        """
        Run the test, showing sequences and collecting user input.
        """
        if self.sequence_attempts < 2:
            # Generate a random sequence of digits with the specified length.
            while True:
                self.sequence = [str(random.randint(0, 9)) for _ in range(self.sequence_length)]
                if self.consecutive(self.sequence):
                    break
            # After a delay, show the sequence to the user.
            self.master.after(500, self.show_sequence)
        else:
            if self.correct_attempts >= 1:
                # If the user got the sequence correct, increase length and restart.
                self.correct_attempts = 0
                self.sequence_attempts = 0
                self.sequence_length += 1
                self.run_test()
            else:
                if self.forward:
                    # If the user fails to repeat forwards, switch to backwards.
                    self.forward = False
                    self.sequence_length = 2
                    self.sequence_attempts = 0
                    self.correct_attempts = 0
                    self.show_backwards_notice()
                else:
                    # If the user fails both forwards and backwards, end the test.
                    self.end_test()

    def show_sequence(self):
        """
        Display the sequence of digits to the user.
        """
        if not hasattr(self, "sequence_index"):
            self.sequence_index = 0

        self.canvas.delete('all')

        if self.sequence_index < len(self.sequence):
            num = self.sequence[self.sequence_index]
            self.canvas.create_text(self.width/2, self.height/2, fill='darkblue', font='Times 160', text=num, justify='c')
            self.sequence_index += 1
            # After a delay, show the next digit in the sequence.
            self.master.after(1000, self.show_sequence)
        else:
            self.sequence_index = 0
            self.get_input()

    def get_input(self):
        """
        Display an input field for the user to enter the sequence they saw.
        """
        prompt = "Input the numbers forwards:" if self.forward else "Input the numbers backwards:"
        self.canvas.create_text(self.width/2, self.height/2.3, fill='darkblue', font='Arial 26', text=prompt, justify='c')
        
        self.input_entry = tk.Entry(self.master, font=('Arial', 32))
        e = self.canvas.create_window(self.width/2, self.height/2, window=self.input_entry)
        self.input_entry.bind('<Return>', self.validate_input)

    def validate_input(self, event):
        """
        Validate the user's input and continue the test.

        Args:
            event: Event object.
        """
        user_input = self.input_entry.get()
        self.input_entry.destroy()

        correct_sequence = ''.join(self.sequence)
        if not self.forward:
            correct_sequence = correct_sequence[::-1]

        if user_input == correct_sequence:
            self.correct_attempts += 1
            self.score += 1

        self.sequence_attempts += 1
        self.run_test()

    def end_test(self):
        """
        End the test and display the user's score.
        """
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2.3, fill='darkblue', font='Arial 26', text="Thank you for your participation!", justify='c')
        self.canvas.create_text(self.width/2, self.height/2, fill='darkblue', font='Arial 36', text=f"Your score: {self.score}", justify='c')

        # Save results to a file.
        with open(f"data/{self.user_id}_results.txt", 'w') as f:
            f.write(f"User ID: {self.user_id}\n")
            f.write(f"Score: {self.score}\n")

    def consecutive(self, sequence):
        """
        Check if a sequence of digits is consecutive.

        Args:
            sequence (list): List of digits.

        Returns:
            bool: True if the sequence is consecutive, False otherwise.
        """
        l = len(sequence)
        for x in range(l-1):
            if sequence[x] == sequence[x+1] or abs(int(sequence[x]) - int(sequence[x+1])) == 1:
                return False
        return True

    def show_backwards_notice(self):
        """
        Show a notice for the user to input numbers backwards.
        """
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2.3, fill='darkblue', font='Arial 26', text="Now, input the numbers backwards.", justify='c')
        self.master.after(3000, self.run_test)

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitSpanTest(root)
    root.mainloop()
