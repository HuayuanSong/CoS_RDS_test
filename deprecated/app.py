# Import Streamlit and random modules
import streamlit as st
import random

# Forward then backward
# 2 x Sequence of 2, 2 x sequence of 3 until they fail both
#


# Define a function to generate a sequence of digits of a given length
def generate_digits(length):
  # Initialize an empty string
  digits = ""
  # Loop for the given length
  for i in range(length):
    # Append a random digit from 0 to 9 to the string
    digits += str(random.randint(0, 9))
  # Return the string
  return digits

# Define a function to run the digits span test
def run_digits_span_test():
  # Initialize the level, score, and flag variables
  level = 1
  score = 0
  flag = True
  # Open a file to save the test results
  file = open("digits_span_test_results.txt", "w")
  # Print a welcome message and instructions
  print("Welcome to the digits span test!")
  print("You will be presented with a sequence of digits and you have to repeat them in the same or reverse order as instructed.")
  print("The test will start with one digit and increase by one after every two correct responses.")
  print("The test will end when you make a mistake or enter 'q' to quit.")
  print("Press any key to start the test.")
  # Wait for user input
  input()
  # Loop until the flag is False
  while flag:
    # Generate a sequence of digits of the current level
    digits = generate_digits(level)
    # Choose a random direction (same or reverse)
    direction = random.choice(["same", "reverse"])
    # Print the sequence and the direction
    print("Digits:", digits)
    print("Direction:", direction)
    # Wait for user input
    answer = input("Your answer: ")
    # Check if the user wants to quit
    if answer == "q":
      print("You have quit the test.")
      flag = False
    else:
      # Check if the user's answer is correct
      if direction == "same" and answer == digits or direction == "reverse" and answer == digits[::-1]:
        print("Correct!")
        score += 1
        # Increase the level by one after every two correct responses
        if score % 2 == 0:
          level += 1
      else:
        print("Incorrect!")
        print("The correct answer was:", digits if direction == "same" else digits[::-1])
        flag = False
      # Write the test result to the file
      file.write(f"Level: {level}, Digits: {digits}, Direction: {direction}, Answer: {answer}, Score: {score}\n")
  # Close the file
  file.close()
  # Print the final score and message
  print(f"Your final score is {score}.")
  print("Thank you for taking the digits span test!")

# Add a title to the app
st.title("Digits Span Test")

# Add some text explaining what the test is and how it works
st.write("""
This is a simple app that lets you take a digits span test.
The test is a measure of working memory and attention, where you have to repeat a sequence of digits in the same or reverse order as they are presented.
The test will start with one digit and increase by one after every two correct responses.
The test will end when you make a mistake or enter 'q' to quit.
The app will save your test results in a file named "digits_span_test_results.txt".
""")

# Create a button that starts the test when clicked
if st.button("Start the test"):
  # Initialize the session state variables
  st.session_state.level = 1
  st.session_state.score = 0
  st.session_state.flag = True
  # Generate the first sequence of digits
  st.session_state.digits = generate_digits(st.session_state.level)
  # Choose a random direction
  st.session_state.direction = random.choice(["same", "reverse"])
  # Display the sequence and the direction
  st.write(f"Digits: {st.session_state.digits}")
  st.write(f"Direction: {st.session_state.direction}")

# Check if the session state variables are defined
if "level" in st.session_state and "score" in st.session_state and "flag" in st.session_state and "digits" in st.session_state and "direction" in st.session_state:
  # Create a text input for the user's answer
  answer = st.text_input("Your answer:")
  # Check if the user has entered something
  if answer:
    # Check if the user wants to quit
    if answer == "q":
      st.write("You have quit the test.")
      st.session_state.flag = False
    else:
      # Check if the user's answer is correct
      if st.session_state.direction == "same" and answer == st.session_state.digits or st.session_state.direction == "reverse" and answer == st.session_state.digits[::-1]:
        st.write("Correct!")
        st.session_state.score += 1
        # Increase the level by one after every two correct responses
        if st.session_state.score % 2 == 0:
          st.session_state.level += 1
      else:
        st.write("Incorrect!")
        st.write(f"The correct answer was: {st.session_state.digits if st.session_state.direction == 'same' else st.session_state.digits[::-1]}")
        st.session_state.flag = False
      # Write the test result to the file
      with open("digits_span_test_results.txt", "a") as file:
        file.write(f"Level: {st.session_state.level}, Digits: {st.session_state.digits}, Direction: {st.session_state.direction}, Answer: {answer}, Score: {st.session_state.score}\n")
    # Check if the flag is still True
    if st.session_state.flag:
      # Generate a new sequence of digits
      st.session_state.digits = generate_digits(st.session_state.level)
      # Choose a new direction
      st.session_state.direction = random.choice(["same", "reverse"])
      # Display the new sequence and direction
      st.write(f"Digits: {st.session_state.digits}")
      st.write(f"Direction: {st.session_state.direction}")
    else:
      # Display the final score and message
      st.write(f"Your final score is {st.session_state.score}.")
      st.write("Thank you for taking the digits span test!")
      # Stop the app from rerunning
      st.stop()
