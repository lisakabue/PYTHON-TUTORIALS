# 1. Access characters in a string by index
greeting = "Hello, World!"
print("First character:", greeting[0])    # H
print("Last character:", greeting[-1])    # !

# 2. Create a multiline string
multiline_text = """This is line one.
This is line two.
This is line three."""
print("\nMultiline string:")
print(multiline_text)

# 3. Check for the presence of a substring
if "World" in greeting:
    print("\n'World' is in the greeting")
else:
    print("\n'World' is not in the greeting")

# 4. Use f-strings for string interpolation
name = "Alice"
age = 25
print(f"\n{name} is {age} years old.")

# 5. Implement built-in string methods
text = "  python programming  "
print("\nOriginal text:", text)

# Strip whitespace
print("Stripped text:", text.strip())

# Uppercase
print("Uppercase:", text.upper())

# Replace a word
print("Replace 'python' with 'Java':", text.replace("python", "Java"))

# Split into words
words = text.split()
print("Split into words:", words)
