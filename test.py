# Import random module
import random

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

# Run the digits span test
run_digits_span_test()
