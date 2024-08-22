#Program to decrypt a message using playfair cipher

def only_alphabets(string):
    # Convert the input string to uppercase and filter out non-alphabetic characters
    # using a list comprehension.
    only_alpha = ''.join([letter.upper() for letter in string if letter.isalpha()])
    return only_alpha


def duplicate_checking(string):
    # Check whether there are any duplicates present in the given string or not?
    seen = set()  # Create an empty set to track seen characters
    newstr = []    # Create an empty list to store unique characters in order
    
    for char in string:
        if char not in seen:
            newstr.append(char)
            seen.add(char)  # Add the character to the set of seen characters
            
    return newstr

def convert_j_to_i(string):
    # Create a list of modified characters using a list comprehension
    modified_chars = ['I' if char.lower() == 'j' else char for char in string]
    
    # Join the list of modified characters to create the final modified string
    modified_string = ''.join(modified_chars)
    
    return modified_string  # Return the modified string

def generate_key_matrix(key):
    # Process the input key to remove non-alphabetic characters
    key1 = only_alphabets(key)
    
    # Initialize an empty 5x5 matrix filled with zeroes
    matrix = [[0 for i in range(5)] for j in range(5)]
    
    # Create a list to store unique letters from the key
    add_letters = []
    
    # Iterate through the processed key to populate the list of unique letters
    for letter in key1:
        if letter not in add_letters:
            add_letters.append(letter)
        else:
            continue
    
    # Fill the remaining positions in the list with uppercase letters from 'A' to 'Z'
    for letter in range(65, 91):  # ASCII values for 'A' to 'Z'
        if chr(letter) not in add_letters:
            add_letters.append(chr(letter))
    
    # Convert 'j' and 'J' to 'I', and remove duplicates while preserving order
    new_add_letters = convert_j_to_i(add_letters)
    new_add_letters_wodup = duplicate_checking(new_add_letters)
    
    index = 0
    
    # Populate the key matrix with characters from the processed list
    for i in range(5):
        for j in range(5):
            matrix[i][j] = new_add_letters_wodup[index]
            index += 1
    
    # Print the generated key matrix
    print("The Key Matrix is:")
    for row in matrix:
        print(row)
    
    return matrix  # Return the key matrix

def preprocess_message(input_text):
    inputText_onlyAlphabets = only_alphabets(input_text)  # Takes only the alphabets in the input message
    input_text_length = len(inputText_onlyAlphabets)
    
    # Create a list to hold digraphs
    digraphs = []
    
    index = 0
    while index < input_text_length:
        if index == input_text_length - 1:
            # If the last character is alone, add 'X' to make it a digraph
            digraphs.append(inputText_onlyAlphabets[index] + 'X')
            index += 1
        elif inputText_onlyAlphabets[index] == inputText_onlyAlphabets[index + 1]:
            # If two consecutive characters are the same, add 'X' between them
            digraphs.append(inputText_onlyAlphabets[index] + 'X')
            index += 1
        else:
            # Otherwise, create a regular digraph
            digraphs.append(inputText_onlyAlphabets[index] + inputText_onlyAlphabets[index + 1])
            index += 2
    
    formatted_digraphs = ' '.join(digraphs)
    
    print("The Digraph is as follows:\n", formatted_digraphs)
    
    return formatted_digraphs


def get_index(chr, mat):
    for num, row in enumerate(mat):  # Iterate through each row and its corresponding index
        if chr in row:  # If the character is present in the current row
            ind = row.index(chr)  # Get the column index of the character in the row
            return num, ind  # Return the row and column indices as a tuple
    return None  # If the character is not found in any row, return None
    
def playfair_decrypt():
    key = input('Enter the key: ')  # Prompt user to enter the decryption key
    encrypted_message = input('Enter the encrypted message: ')  # Prompt user to enter the encrypted message

    key_matrix = generate_key_matrix(key)  # Generate the key matrix using the provided key
    digraphs = preprocess_message(encrypted_message)  # Process the encrypted message into digraphs

    decrypted_text = ''

    # Iterate through pairs of characters in the digraphs
    for (char1, char2) in zip(digraphs[0::3], digraphs[1::3]):
        row1, col1 = get_index(char1, key_matrix)  # Get row and column indices for the first character
        row2, col2 = get_index(char2, key_matrix)  # Get row and column indices for the second character

        # Apply Playfair Cipher decryption rules based on the character positions
        if row1 == row2:  # When characters are in the same row
            decrypted_text += key_matrix[row1][(col1 - 1) % 5] + key_matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:  # When characters are in the same column
            decrypted_text += key_matrix[(row1 - 1) % 5][col1] + key_matrix[(row2 - 1) % 5][col2]
        else:  # When characters are in different rows and columns
            decrypted_text += key_matrix[row1][col2] + key_matrix[row2][col1]

    print("\nDecrypted Message:\n", decrypted_text)  # Print the decrypted message

# Call the playfair_decrypt function to run the decryption process
playfair_decrypt()



