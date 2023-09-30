import tkinter as tk
import random

class DigitSpanTest:
    def __init__(self, master):
        self.master = master
        self.master.title("Reliable Digit Span Test")

        self.entry_label = tk.Label(self.master, text="Enter data file number:")
        self.entry_label.grid(row=0, column=0)

        self.data_file_entry = tk.Entry(self.master)
        self.data_file_entry.grid(row=0, column=1)

        self.start_btn = tk.Button(self.master, text="Start", command=self.start_test)
        self.start_btn.grid(row=1, columnspan=2)

        self.test_label = tk.Label(self.master, font=("Arial", 14))
        self.test_label.grid(row=2, columnspan=2, pady=20)

        self.input_entry = tk.Entry(self.master)
        self.input_entry.grid(row=3, columnspan=2)

        self.forward = True
        self.sequence_length = 2
        self.sequence_attempts = 0
        self.correct_attempts = 0
        self.score = 0

    def start_test(self):
        self.data_file_num = self.data_file_entry.get()
        self.data_file_entry.config(state='disabled')
        self.start_btn.config(state='disabled')
        self.run_test()

    def run_test(self):
        if self.sequence_attempts < 2:
            self.sequence = [str(random.randint(0, 9)) for _ in range(self.sequence_length)]
            self.show_sequence()
        else:
            if self.correct_attempts >= 1:
                self.correct_attempts = 0
                self.sequence_attempts = 0
                self.sequence_length += 1
                self.run_test()
            else:
                if self.forward:
                    self.forward = False
                    self.sequence_length = 2
                    self.sequence_attempts = 0
                    self.correct_attempts = 0
                    self.test_label.config(text="Now, input the numbers backwards.")
                    self.run_test()
                else:
                    self.end_test()

    def show_sequence(self):
        self.test_label.config(text="Watch the numbers...")
        for digit in self.sequence:
            self.test_label.config(text=digit)
            self.master.after(1000, self.master.update_idletasks())

        self.get_input()

    def get_input(self):
        prompt = "Input the numbers forwards:" if self.forward else "Input the numbers backwards:"
        self.test_label.config(text=prompt)
        self.input_entry.bind('<Return>', self.validate_input)

    def validate_input(self, event):
        user_input = self.input_entry.get()
        self.input_entry.delete(0, 'end')

        correct_sequence = ''.join(self.sequence)
        if not self.forward:
            correct_sequence = correct_sequence[::-1]

        if user_input == correct_sequence:
            self.correct_attempts += 1
            self.score += self.sequence_length

        self.sequence_attempts += 1
        self.run_test()

    def end_test(self):
        self.test_label.config(text=f"Your score is {self.score}.")
        with open(f"data_{self.data_file_num}.txt", "w") as f:
            f.write(f"Score: {self.score}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitSpanTest(root)
    root.mainloop()
