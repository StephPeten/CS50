#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int AVgrey;


    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            AVgrey = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.000);

            image[i][j].rgbtRed = AVgrey;
            image[i][j].rgbtGreen = AVgrey;
            image[i][j].rgbtBlue = AVgrey;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed;
    int sepiaGreen;
    int sepiaBlue;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            if (width > 255)
            {
                sepiaBlue = 255;
            }

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }

    return;
}

// Reflect image horizontally

void swap(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE tmp;

    tmp = *a;
    *a = *b;
    *b = tmp;


}

void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int n = 1;
        for (int j = 0; j < width / 2; j++, n++)
        {
            swap(&image[i][j], &image[i][width - n]);
        }
    }

    return;
}



// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE gimage[height][width];
 
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {   
            gimage[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            if (j == 0 && i > 0 && i < height - 1)
            {
                image[i][j].rgbtRed = round((gimage[i - 1][j].rgbtRed + gimage[i - 1][j + 1].rgbtRed + gimage[i][j].rgbtRed + gimage[i][j + 
                                             1].rgbtRed + gimage[i + 1][j].rgbtRed + gimage[i + 1][j + 1].rgbtRed) / 6.0);
                image[i][j].rgbtGreen = round((gimage[i - 1][j].rgbtGreen + gimage[i - 1][j + 1].rgbtGreen + gimage[i][j].rgbtGreen + gimage[i][j +
                                               1].rgbtGreen + gimage[i + 1][j].rgbtGreen + gimage[i + 1][j + 1].rgbtGreen) / 6.0);
                image[i][j].rgbtBlue = round((gimage[i - 1][j].rgbtBlue + gimage[i - 1][j + 1].rgbtBlue + gimage[i][j].rgbtBlue + gimage[i][j +
                                              1].rgbtBlue + gimage[i + 1][j].rgbtBlue + gimage[i + 1][j + 1].rgbtBlue) / 6.0);
            }

            else if (j == width - 1 && i > 0 && i < height - 1)
            {
                image[i][j].rgbtRed = round((gimage[i - 1][j - 1].rgbtRed + gimage[i - 1][j].rgbtRed + gimage[i][j - 1].rgbtRed +
                                             gimage[i][j].rgbtRed + gimage[i + 1][j - 1].rgbtRed + gimage[i + 1][j].rgbtRed) / 6.0);
                image[i][j].rgbtGreen = round((gimage[i - 1][j - 1].rgbtGreen + gimage[i - 1][j].rgbtGreen + gimage[i][j - 1].rgbtGreen +
                                               gimage[i][j].rgbtGreen + gimage[i + 1][j - 1].rgbtGreen + gimage[i + 1][j].rgbtGreen) / 6.0);
                image[i][j].rgbtBlue = round((gimage[i - 1][j - 1].rgbtBlue + gimage[i - 1][j].rgbtBlue + gimage[i][j - 1].rgbtBlue +
                                              gimage[i][j].rgbtBlue + gimage[i + 1][j - 1].rgbtBlue + gimage[i + 1][j].rgbtBlue) / 6.0);
            }

            else if (j > 0 && j < width - 1 && i == 0)
            {
                image[i][j].rgbtRed = round((gimage[i][j - 1].rgbtRed + gimage[i][j].rgbtRed + gimage[i][j + 1].rgbtRed + gimage[i + 1][j -
                                             1].rgbtRed + gimage[i + 1][j].rgbtRed + gimage[i + 1][j + 1].rgbtRed) / 6.0);
                image[i][j].rgbtGreen = round((gimage[i][j - 1].rgbtGreen + gimage[i][j].rgbtGreen + gimage[i][j + 1].rgbtGreen + gimage[i + 1][j -
                                               1].rgbtGreen + gimage[i + 1][j].rgbtGreen + gimage[i + 1][j + 1].rgbtGreen) / 6.0);
                image[i][j].rgbtBlue = round((gimage[i][j - 1].rgbtBlue + gimage[i][j].rgbtBlue + gimage[i][j + 1].rgbtBlue + gimage[i + 1][j -
                                              1].rgbtBlue + gimage[i + 1][j].rgbtBlue + gimage[i + 1][j + 1].rgbtBlue) / 6.0);
            }

            else if (j > 0 && j < width - 1 && i == height - 1)
            {
                image[i][j].rgbtRed = round((gimage[i - 1][j - 1].rgbtRed + gimage[i - 1][j].rgbtRed + gimage[i - 1][j + 1].rgbtRed + gimage[i][j -
                                             1].rgbtRed + gimage[i][j].rgbtRed + gimage[i][j + 1].rgbtRed) / 6.0);
                image[i][j].rgbtGreen = round((gimage[i - 1][j - 1].rgbtGreen + gimage[i - 1][j].rgbtGreen + gimage[i - 1][j + 1].rgbtGreen +
                                               gimage[i][j - 1].rgbtGreen + gimage[i][j].rgbtGreen + gimage[i][j + 1].rgbtGreen) / 6.0);
                image[i][j].rgbtBlue = round((gimage[i - 1][j - 1].rgbtBlue + gimage[i - 1][j].rgbtBlue + gimage[i - 1][j + 1].rgbtBlue +
                                              gimage[i][j - 1].rgbtBlue + gimage[i][j].rgbtBlue + gimage[i][j + 1].rgbtBlue) / 6.0);
            }

            else if (j == 0 & i == 0)
            {
                image[i][j].rgbtRed = round((gimage[i][j].rgbtRed + gimage[i][j + 1].rgbtRed + gimage[i + 1][j].rgbtRed + gimage[i + 1][j +
                                             1].rgbtRed) / 4.0);
                image[i][j].rgbtGreen = round((gimage[i][j].rgbtGreen + gimage[i][j + 1].rgbtGreen + gimage[i + 1][j].rgbtGreen + gimage[i + 1][j +
                                               1].rgbtGreen) / 4.0);
                image[i][j].rgbtBlue = round((gimage[i][j].rgbtBlue + gimage[i][j + 1].rgbtBlue + gimage[i + 1][j].rgbtBlue + gimage[i + 1][j + 
                                              1].rgbtBlue) / 4.0);
            }

            else if (j == width - 1 && i == 0)
            {
                image[i][j].rgbtRed = round((gimage[i][j - 1].rgbtRed + gimage[i][j].rgbtRed + gimage[i + 1][j - 1].rgbtRed + gimage[i + 
                                             1][j].rgbtRed) / 4.0);
                image[i][j].rgbtGreen = round((gimage[i][j - 1].rgbtGreen + gimage[i][j].rgbtGreen + gimage[i + 1][j - 1].rgbtGreen + gimage[i +
                                               1][j].rgbtGreen) / 4.0);
                image[i][j].rgbtBlue = round((gimage[i][j - 1].rgbtBlue + gimage[i][j].rgbtBlue + gimage[i + 1][j - 1].rgbtBlue + gimage[i + 
                                              1][j].rgbtBlue) / 4.0);
            }

            else if (j == 0 && i == height - 1)
            {
                image[i][j].rgbtRed = round((gimage[i - 1][j].rgbtRed + gimage[i - 1][j + 1].rgbtRed + gimage[i][j].rgbtRed + gimage[i][j +
                                             1].rgbtRed) / 4.0);
                image[i][j].rgbtGreen = round((gimage[i - 1][j].rgbtGreen + gimage[i - 1][j + 1].rgbtGreen + gimage[i][j].rgbtGreen + gimage[i][j + 
                                               1].rgbtGreen) / 4.0);
                image[i][j].rgbtBlue = round((gimage[i - 1][j].rgbtBlue + gimage[i - 1][j + 1].rgbtBlue + gimage[i][j].rgbtBlue + gimage[i][j + 
                                              1].rgbtBlue) / 4.0);
            }

            else if (j == width - 1 && i == height - 1)
            {
                image[i][j].rgbtRed = round((gimage[i - 1][j - 1].rgbtRed + gimage[i - 1][j].rgbtRed + gimage[i][j - 1].rgbtRed +
                                             gimage[i][j].rgbtRed) / 4.0);
                image[i][j].rgbtGreen = round((gimage[i - 1][j - 1].rgbtGreen + gimage[i - 1][j].rgbtGreen + gimage[i][j - 1].rgbtGreen +
                                               gimage[i][j].rgbtGreen) / 4.0);
                image[i][j].rgbtBlue = round((gimage[i - 1][j - 1].rgbtBlue + gimage[i - 1][j].rgbtBlue + gimage[i][j - 1].rgbtBlue + 
                                              gimage[i][j].rgbtBlue) / 4.0);
            }

            else if (j > 0 && j < width - 1 && i > 0 && i < height - 1)
            {
                image[i][j].rgbtRed = round((gimage[i - 1][j - 1].rgbtRed + gimage[i - 1][j].rgbtRed + gimage[i - 1][j + 1].rgbtRed + gimage[i][j -
                                             1].rgbtRed + gimage[i][j].rgbtRed + gimage[i][j + 1].rgbtRed + gimage[i + 1][j - 1].rgbtRed + gimage[i + 1][j].rgbtRed + gimage[i +
                                                     1][j + 1].rgbtRed) / 9.0);
                image[i][j].rgbtGreen = round((gimage[i - 1][j - 1].rgbtGreen + gimage[i - 1][j].rgbtGreen + gimage[i - 1][j + 1].rgbtGreen +
                                               gimage[i][j - 1].rgbtGreen + gimage[i][j].rgbtGreen + gimage[i][j + 1].rgbtGreen + gimage[i + 1][j - 1].rgbtGreen + gimage[i +
                                                       1][j].rgbtGreen + gimage[i + 1][j + 1].rgbtGreen) / 9.0);
                image[i][j].rgbtBlue = round((gimage[i - 1][j - 1].rgbtBlue + gimage[i - 1][j].rgbtBlue + gimage[i - 1][j + 1].rgbtBlue +
                                              gimage[i][j - 1].rgbtBlue + gimage[i][j].rgbtBlue + gimage[i][j + 1].rgbtBlue + gimage[i + 1][j - 1].rgbtBlue + gimage[i +
                                                      1][j].rgbtBlue + gimage[i + 1][j + 1].rgbtBlue) / 9.0);
            }

        }
    }

    return;
}