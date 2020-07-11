#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>


int main(void)
{
    string text = get_string("Text : ");
    int count_letters = 0;
    int count_words = 1;
    int count_sentences = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            count_letters++;
        }
        
        else if (text[i] == ' ' && (text[i] != '.' || text[i] != '?' || text[i] != '!'))
        {
            count_words++;
        }
        
        else if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            count_sentences++;
        }
    }
    
    float L = 100 * (float)count_letters / (float)count_words;
    float S = 100 * (float)count_sentences / (float)count_words;
    float index = round(0.0588 * L - 0.296 * S - 15.8);
    
    if (index < 1)
    {
        printf("Before Grade 1");
    }
    
    else if (1 <= index && index <= 16)
    {
        printf("Grade %.0f", index);
    }
    
    else if (index > 16)
    {
        printf("Grade 16+");
    }
    
    printf("\n");
}