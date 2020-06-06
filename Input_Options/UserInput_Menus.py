#!/usr/bin/env python
"""BINF 690 | Annotation Project - User Input Menus
   class of menu options and their associated functions 
   User should respond with a numeric value from the list 
   The list and master input options are maintained in input_options.python
"""

### Import Packages
from __future__ import print_function
from Input_Options import input_options
import csv
import json

inputTypeOpts = input_options.inputTypeOpts
inputIDOpts = input_options.inputIDOpts
inputSourceFormatOpts = input_options.inputSourceFormatOpts
inputOutputFormatOpts = input_options.inputOutputFormatOpts

### def a invalid menu option class 
class InvalidMenuOption(Exception):
    pass

### Input Type Menu
def inputTypeMenu():
    # blank object to fill 
    input_type_selection = ""
    """
    function to identify what path they user wants to take
    
    Paramaters: None
    
    Returns: integer representing the users selection 
    
    """

    try:
        print("Welcome to the Gene Annotation Interface!")
        print("Do you want to:")
        for k in inputTypeOpts.keys():
            print("  ",k,": ",inputTypeOpts[k][1],"?",sep="")
        print("  0: exit program\n")

        input_type_selection = raw_input("  enter the menu item number you would like to use: ")
        print("\n")
        input_type_selection = int(input_type_selection)
                   
    except(ValueError, TypeError):
        print("User Input Error:")
        print("  excpecting a number value (1-3 or 0) to exist")
        print("  the input received was %s" %(input_type_selection))
        print("  please try again\n")
    
    finally:
        return(input_type_selection)
        
### Gene ID Input
def inputIDString():
    """
    method to retrieve an input from the user
    
    returns a string that the user input
    """
    print("Gene ID Input")        
    input_gene_id = raw_input("  enter your geneID: ")
    print("\n")
        
    return input_gene_id

### Gene ID Format
def inputIdFormatMenu():
    """Gene ID Format Menu
       Method to get the ID of the gene from the user 
       expected responses 1 - 6, 0 to return to the main level
       the function will return input_format_selection 
    """
    
    # preset a blank var to output in case of an error
    input_format_selection = ""
    
    print("What format is your gene ID in?")
    for k in inputIDOpts.keys():
        print("  ",k,": ",inputIDOpts[k][1],sep="")
    print("  0: return to main menu\n")

    input_format_selection = raw_input("  enter the menu item number with the format of your gene ID(s): ")
    print("\n")
    
    ### try block
    try:
        input_format_selection = int(input_format_selection)

    ### exceptions for all other errors
    except(ValueError, TypeError): #, InvalidMenuOption):
        print("User Input Error:")
        print("  excpecting a number value (1-6 or 0) to exist")
        print("  the input received was %s" %(input_format_selection))
        print("  please try again\n")
        
    finally:
        return(input_format_selection)
        
### Annotation Type Menu
def inputAnnotationSourceMenu():
    """
    function to get the annotation source from the user
    
    Paramaters: None
    
    Returns: integer representing the users selection 
    
    """
    # blank object to fill
    input_source_selection = ""

    try:
        print("Which annotation source would you like data from?")
        for k in inputSourceFormatOpts.keys():
            print("  ",k,": ",inputSourceFormatOpts[k][1],sep="")
        print("  0: return to main menu\n")

        input_source_selection = raw_input("  enter the menu item number of the source you would like: ")
        print("\n")
        input_source_selection = int(input_source_selection)
            
    except(ValueError, TypeError):
        print("User Input Error:")
        print("  excpecting a number value (1-6 or 0) to exist")
        print("  the input received was %s" %(input_source_selection))
        print("  please try again\n")
        
    finally:
        return input_source_selection       

### Output Format Menu
def inputOutputFormatMenu():
    """
    function to get the output file details from the user
    
    Paramaters: None
    
    Returns: 
    outdir, str: directory to store file in
    outfname, str: filename to write out 
    input_outputformat_selection, int: file extension for writing the data 
    
    """                    
    # run in
    print("Okay - lets get some information about the output file")
    # ask the user which directory they want it saved in
    print("Where do you want this file saved? (e.g. please provide a directory path and include a trailing '\\')")
 
    # take the input
    outdir = raw_input("  directory path: ")
    print("\n")
    
    # ask the user what name they want it saved in
    print("What do you want to name this file? (do not include a file extension)")
    # take the input
    outfname = raw_input("  file name: ")
    print("\n")
    
    # ask the user which file format they want their output in
    print("Which output format would you like?")
    # print out the list of options from the input_options master
    for k in inputOutputFormatOpts.keys():
        print("  ",k,": ",inputOutputFormatOpts[k][1],sep="")
    # add 0 as an option to return to the main menu
    print("  0: return to main menu\n")
    
    # ask the user to input the number of the value they want
    input_outputformat_selection = raw_input("  enter the menu item number of the format you would like: ")
    print("\n")
    # convert to a numeric value
    input_outputformat_selection = int(input_outputformat_selection)
                
    return(input_outputformat_selection, outdir, outfname)
    
### Write Output File Menu
def WriteOutputFile(Data, FileFormat_Selection, FileDir, FileName):
    """Write Output File Function
    
    This function will write out either a csv, tsv, or json file depending on input
    
    Paramaters:
    Data (dict): input the dictionary you want to write. 
                 this should be output from the annotation retriever.
                 it's anticipated that the fields in the dict are:
                    fields = ["Input_GeneId", "Input_IdFormat", "Output_AnnotationSource",
                               "Output_IdFormat", "Output_GeneId", "Annotation"] 
    FileFormat_Selection: the user defined file format - this can be called from UIn.getOutFileFormat()
    FileDir: the directory to store the output file - this can be called from UIn.getOutFileDir()
    FileName: the name of the file to output - this can be called from UIn.getOutFileName()
    
    Returns:
    Writes a file to defined directory 
    
    """
    FileFormat = inputOutputFormatOpts[FileFormat_Selection][0]
    
    file_dir_name_format = FileDir+FileName+"."+FileFormat
    
    fields = ["Input_GeneId", "Input_IdFormat", "Output_AnnotationSource",
              "Output_IdFormat", "Output_GeneId", "Annotation"]    
    
    ### CSV
    if (FileFormat_Selection==1):
        # open file and write
        with open(file_dir_name_format, 'wb') as csv_file:
            #writer = csv.DictWriter(tsv_file, fieldnames = fields, delimiter="\t")
            writer = csv.writer(csv_file, delimiter=",")
            writer.writerow(fields)
            writer.writerows(zip(*[Data[f] for f in fields]))

    ### TSV
    elif (FileFormat_Selection==2):
        # open file and write
        with open(file_dir_name_format, 'wb') as tsv_file:
            #writer = csv.DictWriter(tsv_file, fieldnames = fields, delimiter="\t")
            writer = csv.writer(tsv_file, delimiter="\t")
            writer.writerow(fields)
            writer.writerows(zip(*[Data[f] for f in fields]))

    ### JSON            
    elif (FileFormat_Selection==3):
        # open file and write
        with open(file_dir_name_format, 'wb') as json_file:
            json.dump(Data, json_file, sort_keys=True, indent=4)
      
### Upload File Menu
def inputUploadFileMenu():
    """Write Output File Function
    
    This function will write prompt the user to provide information about their file to input 
    
    Paramaters: none, all driven by input
                only CSV's are acceptable input 
    
    Returns:
    input_data, list: a list of the read in file 
    
    """
    try:
        print("Gene ID File Upload")
        print("Please upload a csv with the following columns: ")
        print("   gene_id , id_format , annotation_source , output_file_format* , output_path* , output_filename*")
        print("   inputs for id_format, annotation_source, and output_file_format should be numerical keys")
        print("   * indicates that this is an optional column for the input file\n")
        print("Allowable ID Formats are: ")
        for id_keys in inputIDOpts:
            print("\tKey Value: ", id_keys, " will return: ", inputIDOpts[id_keys])
        print("\n")

        print("Allowable Annotation Sources are: ")
        for annotation_keys in inputSourceFormatOpts:
            print("\tKey Value: ", annotation_keys, " will return: ", inputSourceFormatOpts[annotation_keys])
        print("\n")
        
        print("Allowable Output Formats are: ")
        for format_keys in inputOutputFormatOpts:
            print("\tKey Value: ", format_keys, " will return: ", inputOutputFormatOpts[format_keys])
        print("\n")
        
        # ask the user which directory they want it saved in
        print("What is the path to your input file? please provide a directory path and filename (e.g. 'C:\User\MyFolder\SomeCoolGenes.csv')")
    
        # take the input
        infile = raw_input("  directory path: ")
        print("\n")
        
        input_data = []
        
        with open(infile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    pass
                    line_count += 1
                else:
                    input_data.append(row)
                    
        return input_data

    except:
        print("There was an issue when reading your file. Please make sure you provided the correct path and it was a CSV file")
    
    
    