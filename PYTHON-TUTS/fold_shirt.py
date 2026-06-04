# Initialize a variable to keep track of the number of shirts folded
shirts_folded = 0

# Use a while loop to "fold" shirts until five are folded
# The loop will run as long as the counter is less than 5
while shirts_folded < 5:
    # Increment the counter by 1 each time the loop runs
    shirts_folded += 1
    
    # Print a message for each shirt folded
    # This will display "Folding shirt number 1" through "Folding shirt number 5"
    print(f"Folding shirt number {shirts_folded}...")

# Print a final message when all five shirts are folded
print("All five shirts are folded and ready to be put away!")
