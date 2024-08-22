
##Program for Playfair Encryption


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

# def digraph_with_split(input_text):
#     inputText_onlyAlphabets=only_alphabets(input_text) #takes only the alphabets in the input message
#     index = 0
#     while (index <len(inputText_onlyAlphabets)):
#         compare_one = inputText_onlyAlphabets[index]
#         if index == len(inputText_onlyAlphabets)-1:  #this is to check if last character is lone
#             inputText_onlyAlphabets = inputText_onlyAlphabets + 'X'  #Using X as the filler
#             index=index+2
#             continue
#         compare_two = inputText_onlyAlphabets[index+1]
#         if compare_one == compare_two :        #to check if two consecutive characters are same
#             inputText_onlyAlphabets = inputText_onlyAlphabets[:index+1] + "X" + inputText_onlyAlphabets[index+1:]
#         index=index+2
#     index =0
#     while (index<len(inputText_onlyAlphabets)):    #to seperate the pair of letters
#         inputText_onlyAlphabets = inputText_onlyAlphabets[:index+2]+' '+ inputText_onlyAlphabets[index+2:]
#         index=index+3
#     print("The Digraph is as follows\n",inputText_onlyAlphabets)
#     return inputText_onlyAlphabets

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


# def index_get(chr,mat):
#     for num in range (5):
#         try:
#             ind = mat[num].index(chr)
#             return (num,ind)
#         except:
#             continue

def get_index(chr, mat):
    for num, row in enumerate(mat):
        if chr in row:
            ind = row.index(chr)
            return num, ind
    return None

# def playfair_encrypt():
#     key = input('Enter the key\n')
#     message = input('Enter the message\n')
#     k = key_matrix(key) #calling matrix function
#     m = digraph_with_split(message) #processing the message
#     cip_text = ''
#     for(var1, var2) in zip(m[0::3], m[1::3]):
#         r1, c1 = index_get(var1,k)  #getting the values for row & coloum form index_get
#         r2, c2 = index_get(var2,k)
#         if r1 == r2 : # when letters are in same row
#           cip_text += k[r1][(c1+1)%5] + k[r2][(c2+1)%5]
#         elif c1 == c2 : # when letters are in same col
#           cip_text += k[(r1+1)%5][c1] + k[(r2+1)%5][c2]
#         else : # when letters are in a different column and row
#           cip_text += k[r1][c2] + k[r2][c1]
#     print("\nEncrypted Message \n",cip_text)

def playfair_encrypt():
    key = input('Enter the key: ')  # Prompt user to enter the encryption key
    message = input('Enter the message: ')  # Prompt user to enter the message to encrypt

    key_matrix = generate_key_matrix(key)  # Generate the key matrix using the provided key
    digraphs = preprocess_message(message)  # Process the message into digraphs

    encrypted_text = ''

    # Iterate through pairs of characters in the digraphs
    for (char1, char2) in zip(digraphs[0::3], digraphs[1::3]):
        row1, col1 = get_index(char1, key_matrix)  # Get row and column indices for the first character
        row2, col2 = get_index(char2, key_matrix)  # Get row and column indices for the second character

        # Apply Playfair Cipher encryption rules based on the character positions
        if row1 == row2:  # When characters are in the same row
            encrypted_text += key_matrix[row1][(col1 + 1) % 5] + key_matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:  # When characters are in the same column
            encrypted_text += key_matrix[(row1 + 1) % 5][col1] + key_matrix[(row2 + 1) % 5][col2]
        else:  # When characters are in different rows and columns
            encrypted_text += key_matrix[row1][col2] + key_matrix[row2][col1]

    print("\nEncrypted Message:\n", encrypted_text)  # Print the encrypted message

# Call the playfair_encrypt function to run the encryption process
playfair_encrypt()





