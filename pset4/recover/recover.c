#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Format -> ./recover card.xxx\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        return 1;
    }
    
    FILE *img;
    unsigned char *buffer = malloc(512);
    int total = 0;
    char filename[8];
    
    while (fread(buffer, 512, 1, file))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (total > 0)
            {
                fclose(img);
            }
            
            sprintf(filename, "%03i.jpg", total);
            
            img = fopen(filename, "w");
            
            total ++;
        }
            
        if (total > 0)
        {
            fwrite(buffer, 512, 1, img);
        }
    }

    fclose(file);
    free(buffer);
    return 0;
}