import tkinter as tk
import random

class DigitSpanTest:
    """
    A class that implements a Digit Span Test for evaluating working memory performance.

    Attributes:
    - master: the tkinter master window
    - width: the width of the screen
    - height: the height of the screen
    - canvas: the tkinter canvas used for displaying UI elements
    - id_entry: the tkinter entry widget for entering user ID
    - user_id: the ID entered by the user
    - practice_btn: the tkinter button widget for starting practice mode
    - pre_test_btn: the tkinter button widget for starting pre-test mode
    - post_test_btn: the tkinter button widget for starting post-test mode
    - forward: a boolean indicating whether the current test is forward or backward
    - sequence_length: the length of the current sequence
    - sequence_attempts: the number of attempts made to repeat the current sequence
    - correct_attempts: the number of correct attempts made to repeat the current sequence
    - max_forward_length: the maximum length of a forward sequence achieved in the current test
    - max_backward_length: the maximum length of a backward sequence achieved in the current test
    - last_sequence: the last sequence generated in the current test
    - sequence: the current sequence to be repeated by the user
    - practice_mode: a boolean indicating whether the current test is in practice mode
    - test_type: a string indicating the type of the current test (pre or post)
    """
    def __init__(self, master):
        """
        Initializes the DigitSpanTest object.

        Args:
        - master: the tkinter master window
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
        Displays a UI element for entering user ID.
        """
        self.canvas.delete('all')
        label = self.canvas.create_text(self.width/2, self.height/2.3, fill='darkblue', font='Arial 26', text="Please enter your ID:", justify='c')
        self.id_entry = tk.Entry(self.master, font=('Arial', 32))
        self.canvas.create_window(self.width/2, self.height/2, window=self.id_entry)
        self.id_entry.bind('<Return>', self.start_intro)
        self.id_entry.focus_set()

    def start_intro(self, event=None):
        """
        Displays the introduction UI elements and buttons for starting the test.

        Args:
        - event: the tkinter event that triggered the function (default None)
        """
        self.user_id = self.id_entry.get().strip()
        if not self.user_id:
            return

        self.canvas.delete('all')
        title_text = "Digit Span Test for Working Memory Evaluation"
        self.canvas.create_text(self.width/2, self.height/4.5, fill='darkblue', font='Arial 52', text=title_text, justify='c')

        docs = ("This is a Digit Span Test that evaluates working memory performance.\n"
                "Try to remember the digits in the order they are presented and\n"
                "repeat them once the sequence has stopped.\n"
                "If successful, the length of the sequence will increase by 1.\n"
                "We will start out with 2 digits.\n"
                "Choose if you'd like to start the test or practice first.")
        self.canvas.create_text(self.width/2, self.height/2.2, fill='darkblue', font='Arial 26', text=docs, justify='c')

        self.practice_btn = tk.Button(self.master, text="Practice", font='Arial 24', fg='black', bg='#4682B4', command=self.start_practice)
        self.canvas.create_window(self.width/2.6, self.height/1.4, window=self.practice_btn)
        
        self.pre_test_btn = tk.Button(self.master, text="Start Pre-test", font='Arial 24', fg='black', bg='#4682B4', command=lambda: self.start_test('pre'))
        self.canvas.create_window(self.width/1.9, self.height/1.4, window=self.pre_test_btn)

        self.post_test_btn = tk.Button(self.master, text="Start Post-test", font='Arial 24', fg='black', bg='#4682B4', command=lambda: self.start_test('post'))
        self.canvas.create_window(self.width/1.4, self.height/1.4, window=self.post_test_btn)

    def initialize_test_values(self):
        """
        Initializes the test values for a new test.
        """
        self.forward = True
        self.sequence_length = 2
        self.sequence_attempts = 0
        self.correct_attempts = 0
        self.max_forward_length = 0
        self.max_backward_length = 0

    def start_practice(self):
        """
        Starts the practice mode.
        """
        self.practice_mode = True
        self.initialize_test_values()
        self.run_test()

    def start_test(self, test_type):
        """
        Starts the pre-test or post-test mode.

        Args:
        - test_type: a string indicating the type of the test (pre or post)
        """
        self.test_type = test_type
        self.practice_mode = False
        self.initialize_test_values()
        self.run_test()

    def run_test(self):
        """
        Runs the current test.
        """
        if self.sequence_attempts < 2:
            while True:
                new_sequence = [str(random.randint(0, 9))]
                for _ in range(1, self.sequence_length):
                    while True:
                        next_digit = str(random.randint(0, 9))
                        if next_digit != new_sequence[-1]:
                            new_sequence.append(next_digit)
                            break
                if new_sequence != getattr(self, 'last_sequence', []):
                    break

            self.sequence = new_sequence
            self.last_sequence = new_sequence
            self.show_sequence()
        else:
            if self.correct_attempts >= 1:
                if self.forward:
                    self.max_forward_length = max(self.max_forward_length, self.sequence_length)
                else:
                    self.max_backward_length = max(self.max_backward_length, self.sequence_length)
                self.correct_attempts = 0
                self.sequence_attempts = 0
                self.sequence_length += 1

                if self.practice_mode:
                    if self.sequence_length > 3:
                        if self.forward:
                            self.forward = False
                            self.sequence_length = 2
                            self.sequence_attempts = 0
                            self.correct_attempts = 0
                            self.show_backwards_notice()
                            return
                        else:
                            self.end_test()
                            return
                self.run_test()
            else:
                if self.forward:
                    self.forward = False
                    self.sequence_length = 2
                    self.sequence_attempts = 0
                    self.correct_attempts = 0
                    self.show_backwards_notice()
                else:
                    if self.practice_mode:
                        self.end_test()
                    else:
                        self.end_test()

    def show_sequence(self):
        """
        Displays the current sequence to be repeated by the user.
        """
        self.canvas.delete('all')
        for idx, num in enumerate(self.sequence):
            self.master.after(idx * 1000, self.display_number, num)
        self.master.after(len(self.sequence) * 1000, self.get_input)

    def display_number(self, num):
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, fill='darkblue', font='Times 160', text=num)

    def get_input(self):
        self.canvas.delete('all')  
        prompt = "Input the numbers forwards:" if self.forward else "Input the numbers backwards:"
        self.canvas.create_text(self.width/2, self.height/2.3, fill='darkblue', font='Arial 26', text=prompt)
        self.input_entry = tk.Entry(self.master, font=('Arial', 32))
        self.canvas.create_window(self.width/2, self.height/2, window=self.input_entry)
        self.input_entry.bind('<Return>', self.validate_input)
        self.input_entry.focus_set()

    def validate_input(self, event):
        user_input = self.input_entry.get()
        correct_sequence = ''.join(self.sequence)
        if not self.forward:
            correct_sequence = correct_sequence[::-1]
        if user_input == correct_sequence:
            self.correct_attempts += 1
        self.sequence_attempts += 1
        self.run_test()

    def show_backwards_notice(self):
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2.3, fill='darkblue', font='Arial 26', text="Now, input the numbers backwards.")
        self.master.after(3000, self.run_test)

    def end_test(self):
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2.5, fill='darkblue', font='Arial 26', text=f"Test complete, {self.user_id}!")
        
        combined_score = self.max_forward_length + self.max_backward_length
        combined_results = f"Combined Test Score: {combined_score}"
        forward_results = f"Max Forward Length: {self.max_forward_length}"
        backward_results = f"Max Backward Length: {self.max_backward_length}"
        
        self.canvas.create_text(self.width/2, self.height/2, fill='darkblue', font='Arial 22', text=forward_results)
        self.canvas.create_text(self.width/2, self.height/1.8, fill='darkblue', font='Arial 22', text=backward_results)
        self.canvas.create_text(self.width/2, self.height/1.6, fill='darkblue', font='Arial 22', text=combined_results)
        
        if self.practice_mode:
            self.canvas.create_text(self.width/2, self.height/1.3, fill='darkblue', font='Arial 26', text="Practice Complete!")
            self.master.after(4000, self.start_intro)
        else:
            with open(f"data/{self.user_id}_{self.test_type}_test.txt", "w") as f:
                f.write(f"{self.max_forward_length},{self.max_backward_length},{combined_score}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitSpanTest(master=root)
    root.mainloop()