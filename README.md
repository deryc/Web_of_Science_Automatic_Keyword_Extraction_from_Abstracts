# Web_of_Science_Automatic_Keyword_Extraction_from_Abstracts
Uses Web of Science metadata and extracts keywords from the abstracts.

When downloading Web of Science records:  
1.) Click export  
2.) Select "Other file formats"  
3.) Select "All records on page" or fill in the optional numerical values  
4.) Under Record Content, select "Full Record and Cited References"  
5.) Under File Format, select "Tab delimited UTF-8" for Windows or Mac  

You can find an example file in this repository.

This is the only type of Web of Science record this script can analyze.
Because your data set might be larger than the maximum of 500 record limit per download,
you can concatenate multiple Web of Science records into a single plain text file.

If you experience trouble with the encoding of your file,
open it in a text editor that allows you to change the encoding to UTF-8.
This often occurs with files that are encoded UTF-8, with BOM.

This script produces a text file where the keywords are extracted and ranked using user specified sensativity measures.
