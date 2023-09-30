# Import modules
import tkinter as tk
import random
import csv
import time

# Define global variables
digits = list(range(10)) # List of digits from 0 to 9
span = 2 # Initial span length
sequence = [] # List to store the current sequence of digits
forward = True # Boolean to indicate forward or backward span
score = 0 # Variable to store the final score
number = "" # Variable to store the user's number

# Define functions
def generate_sequence():
    """Generate a random sequence of digits with the current span length"""
    global sequence
    sequence = random.choices(digits, k=span) # Choose span number of digits randomly

def display_sequence():
    """Display the sequence of digits on the GUI with 1 second interval"""
    global sequence, forward, span_label, direction_label, digit_label, entry, button
    span_label.config(text=f"Sequence length: {span}") # Update the span label
    if forward: # If forward span
        direction_label.config(text="Forward") # Set direction label to forward
    else: # If backward span
        direction_label.config(text="Backward") # Set direction label to backward
        sequence.reverse() # Reverse the sequence
    for digit in sequence: # For each digit in the sequence
        digit_label.config(text=digit) # Display the digit on the GUI
        root.update() # Update the GUI
        time.sleep(1) # Wait for 1 second
    digit_label.config(text="") # Clear the digit label
    entry.delete(0, tk.END) # Clear the entry box
    entry.config(state=tk.NORMAL) # Enable the entry box
    button.config(text="Submit", command=check_answer) # Change the button text and command to submit and check answer

def check_answer():
    """Check the user's answer and update the score and span accordingly"""
    global sequence, span, forward, score, entry, button, result_label
    answer = entry.get() # Get the user's answer from the entry box
    if answer.isdigit(): # If the answer is a valid number
        answer = [int(digit) for digit in answer] # Convert the answer to a list of digits
        if answer == sequence: # If the answer matches the sequence
            result_label.config(text="Correct!", fg="green") # Display correct on the GUI with green color
            score += 1 # Increment the score by 1 
            span += 1 # Increment the span by 1 
        else: # If the answer does not match the sequence 
            result_label.config(text="Incorrect!", fg="red") # Display incorrect on the GUI with red color 
            if not forward: # If backward span 
                end_test() # End the test 
                return # Return from the function 
            else: # If forward span 
                forward = not forward # Toggle the forward boolean 
                span = 2 # Reset the span to 2 
    else: # If the answer is not a valid number 
        result_label.config(text="Invalid input!", fg="red") # Display invalid input on the GUI with red color 
    entry.delete(0, tk.END) # Clear the entry box 
    entry.config(state=tk.DISABLED) # Disable the entry box 
    button.config(text="Next", command=start_trial) # Change the button text and command to next and start trial 

def start_trial():
    """Start a new trial by generating and displaying a new sequence"""
    global result_label 
    result_label.config(text="") # Clear the result label 
    generate_sequence() # Generate a new sequence 
    display_sequence() # Display the new sequence 

def end_test():
    """End the test by showing the final score and saving the data"""
    global number, score, span_label, direction_label, digit_label, entry, button, result_label 
    span_label.config(text=f"Test ended") # Update the span label 
    direction_label.config(text="") # Clear the direction label 
    digit_label.config(text=f"Your final score is {score}") # Display the final score on the GUI 
    entry.config(state=tk.DISABLED) # Disable the entry box 
    button.config(state=tk.DISABLED) # Disable the button 
    result_label.config(text=f"Thank you for participating!") # Display a thank you message on the GUI 
    save_data() # Save the data to a CSV file 

def save_data():
    """Save the data to a CSV file named 'digit_span_data_[number].csv'"""
    global number, score 
    data = [number, score] # Create a list of data 
    with open(f"digit_span_data_{number}.csv", "a", newline="") as file: # Open the CSV file in append mode 
        writer = csv.writer(file) # Create a CSV writer object 
        writer.writerow(data) # Write the data as a row 

def start_test():
    """Start the test by getting the user's number and starting the first trial"""
    global number, number_entry, start_button, span_label, direction_label, digit_label, entry, button 
    number = number_entry.get() # Get the user's number from the entry box 
    if number.isdigit(): # If the number is a valid number 
        number_entry.destroy() # Destroy the number entry box 
        start_button.destroy() # Destroy the start button 
        span_label = tk.Label(root, text=f"Sequence length: {span}") # Create a span label 
        span_label.pack() # Pack the span label 
        direction_label = tk.Label(root, text="Forward") # Create a direction label with forward text 
        direction_label.pack() # Pack the direction label 
        digit_label = tk.Label(root, font=("Arial", 32)) # Create a digit label with large font 
        digit_label.pack() # Pack the digit label 
        entry = tk.Entry(root, state=tk.DISABLED) # Create an entry box and disable it initially 
        entry.pack() # Pack the entry box 
        button = tk.Button(root, text="Next", command=start_trial) # Create a button with next text and start trial command 
        button.pack() # Pack the button 
        start_trial() # Start the first trial 
    else: # If the number is not a valid number 
        tk.messagebox.showerror("Error", "Please enter a valid number") # Show an error message 

# Create the root window
root = tk.Tk()
root.title("Digit Span Test")

# Create a welcome label
welcome_label = tk.Label(root, text="Welcome to the Digit Span Test!")
welcome_label.pack()

# Create a number label
number_label = tk.Label(root, text="Please enter your number:")
number_label.pack()

# Create a number entry box
number_entry = tk.Entry(root)
number_entry.pack()

# Create a start button
start_button = tk.Button(root, text="Start", command=start_test)
start_button.pack()

# Create a result label
result_label = tk.Label(root)
result_label.pack()

# Start the main loop
root.mainloop()
