import tkinter as tk
import random

class DigitSpanTest:
    def __init__(self, master):
        self.master = master
        self.master.title("Digit Span Test for Working Memory Evaluation")

        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry(f"{self.width}x{self.height}")

        self.canvas = tk.Canvas(self.master, bg='#FDF5E6')
        self.canvas.pack(fill='both', expand=True)

        self.ask_for_id()

    def ask_for_id(self):
        self.canvas.delete('all')
        label = self.canvas.create_text(self.width/2, self.height/2.3, fill='darkblue', font='Arial 26', text="Please enter your ID:", justify='c')
        self.id_entry = tk.Entry(self.master, font=('Arial', 32))
        self.canvas.create_window(self.width/2, self.height/2, window=self.id_entry)
        self.id_entry.bind('<Return>', self.start_intro)
        self.id_entry.focus_set()

    def start_intro(self, event=None):
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
        self.canvas.create_window(self.width/2.3, self.height/1.4, window=self.practice_btn)
        
        self.start_btn = tk.Button(self.master, text="Start", font='Arial 24', fg='black', bg='#4682B4', command=self.start_test)
        self.canvas.create_window(self.width/1.7, self.height/1.4, window=self.start_btn)

    def initialize_test_values(self):
        self.forward = True
        self.sequence_length = 2
        self.sequence_attempts = 0
        self.correct_attempts = 0
        self.max_forward_length = 0
        self.max_backward_length = 0

    def start_practice(self):
        self.practice_mode = True
        self.initialize_test_values()
        self.run_test()

    def start_test(self):
        self.practice_mode = False
        self.initialize_test_values()
        self.run_test()

    def run_test(self):
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
                            self.end_practice()
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
                        self.end_practice()
                    else:
                        self.end_test()

    def show_sequence(self):
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
        self.canvas.create_text(self.width/2, self.height/2.3, fill='darkblue', font='Arial 26', text=f"Test complete, {self.user_id}!")
        results = (f"Max Forward Length: {self.max_forward_length}\n"
                   f"Max Backward Length: {self.max_backward_length}")
        self.canvas.create_text(self.width/2, self.height/2, fill='darkblue', font='Arial 26', text=results)

    def end_practice(self):
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2.3, fill='darkblue', font='Arial 26', text="Practice complete!")
        self.master.after(3000, self.start_intro)

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitSpanTest(master=root)
    root.mainloop()
