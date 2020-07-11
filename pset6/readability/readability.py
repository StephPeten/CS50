import re
from cs50 import get_string


text = get_string("Text : ")
count_letters = 0
count_words = 1
count_sentences = 0

for i in range(len(text)):
    if (text[i] >= 'a' and text[i] <= 'z') or (text[i] >= 'A' and text[i] <= 'Z'):
        count_letters += 1
    
    elif ((text[i] == ' ') and (text[i] != "." or "?" or "!")):
        count_words += 1
        
    elif (text[i] == '.' or text[i] == '?' or text[i] == '!'):
        count_sentences += 1


L = 100 * float(count_letters) / float(count_words)
S = 100 * float(count_sentences) / float(count_words)
index = round(0.0588 * L - 0.296 * S - 15.8)
    
if index < 1:
    print("Before Grade 1")
    
elif 1 <= index and index <= 16:
    print(f"Grade {index}")

elif index > 16:
    print("Grade 16+")