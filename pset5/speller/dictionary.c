// Implements a dictionary's functionality

#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>
#include <ctype.h>



#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Number of words in total
int totalword = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    
    char Lword[LENGTH+1];
    
    for (int s = 0; s < LENGTH; s++)
    {
        Lword[s] = tolower(word[s]);
    }
    
    
    for (node *cursor = table[hash(Lword)]; cursor != NULL; cursor = cursor->next)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    
    int h = word[0] - 'a';
    
    return h;
}
    

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    
    char *Zword = malloc(LENGTH);
    if (Zword == NULL)
    {
        return false;
    }
    
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    
    while (fscanf(file, "%s", Zword) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        
        strcpy(n->word, Zword);
        totalword++;
        
        n->next = table[hash(Zword)];
        
        table[hash(Zword)] = n;
    }
    
    fclose(file);
    free(Zword);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    
    return totalword;
}
    

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    
    for (int i = 0; i < 26; i++)
    {
        node *cursor = table[i];
        
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
        
        free(cursor);
    }
    
    return true;
}