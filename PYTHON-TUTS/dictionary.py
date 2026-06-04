# 1. Create a dictionary
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}
print("Original dictionary:", person)

# 2. Look up a value using a key
print("Name:", person["name"])
print("Age:", person["age"])

# 3. Add a new key-value pair
person["profession"] = "Engineer"
print("After adding profession:", person)

# 4. Remove a key-value pair
del person["city"]
print("After removing city:", person)

# 5. Iterate over the dictionary
print("Iterating over dictionary:")
for key, value in person.items():
    print(f"{key}: {value}")
