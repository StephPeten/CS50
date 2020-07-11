#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    
    else
    {
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (argv[1][i] < 48 || argv[1][i] > 57)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        
        int k = atoi(argv[1]);
    
        string plaintext = get_string("plaintext: ");
        printf("ciphertext: ");
        
        for (int c = 0; c < strlen(plaintext); c++)
        {
            if (isupper(plaintext[c]))
            {
                printf("%c", (((plaintext[c] + k) - 65) % 26) + 65);
            }
            else if (islower(plaintext[c]))
            {
                printf("%c", (((plaintext[c] + k) - 97) % 26) + 97);
            }
            else
            {
                printf("%c", plaintext[c]);
            }
        }
        
        printf("\n");
    }
}