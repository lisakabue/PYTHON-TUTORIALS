# 1. Create a list
fruits = ["apple", "banana", "cherry"]
print("Original list:", fruits)

# 2. Print an element by index
print("Element at index 1:", fruits[1])  # banana

# 3. Add an item to the end
fruits.append("orange")
print("After appending 'orange':", fruits)

# 4. Remove an item
fruits.remove("banana")
print("After removing 'banana':", fruits)

# 5. Iterate over the list
print("Iterating over the list:")
for fruit in fruits:
    print("I like", fruit)

# 6. Reverse the list
fruits.reverse()
print("Reversed list:", fruits)
