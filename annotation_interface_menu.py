#!/usr/bin/env python
"""BINF 690 | Annotation Project - Driver Menu
Main menu driver for all annotation options
run this menu to get user prompts and annotate your genes

Requirements:
    this file assumes that it is in the main directory,
    with two sub directorys for 
    1. API_dir, with the API scripts housed in it
    2. Input_Options with the UI and input drivers in it
"""

### Import Packages
import sys
import re
from API_dir.API_Class import API
from Input_Options.UserInput import UserInput 
from Input_Options import input_options
from Input_Options import UserInput_Menus

### Initialize Classes 
inputIDOpts = input_options.inputIDOpts
inputSourceFormatOpts = input_options.inputSourceFormatOpts
inputOutputFormatOpts = input_options.inputOutputFormatOpts

UIn = UserInput()
UIn.__init__()

API_Caller = API()
API_Caller.__init__()

### def a invalid menu option class 
class InvalidMenuOption(Exception):
    pass

### Run initial Menu 
UIn.setUploadType(UserInput_Menus.inputTypeMenu())

### Main Menu Looper
while True:
    # initial try-er
    try:
        #############################################
        ###### Check the input type for errors ######
        if (UIn.getUploadType() == 0):
            break
            sys.exit(0)
            
        elif (1 <= UIn.getUploadType() <= 2):
            ##################################
            ##### Get the Gene ID Inputs #####
            if (UIn.getUploadType() == 1):
            ### run submenu for gene ID input
                UIn.setGeneID(UserInput_Menus.inputIDString())
            
            ### run submenu for multiple gene IDs
            elif (UIn.getUploadType() == 2):
                print("Please input your IDs below seperated by either spaces or new line characters")
                print("After we read in your list, please review it to make sure everything looks okay before moving forward.")
                multiple_gene_input = UserInput_Menus.inputIDString()
                multiple_gene_input = re.split(r"\n|\s",multiple_gene_input)   
                
                print("Okay, we got {N} IDs from you. They were:\n\t {inlist}\n"
                      .format(N=len(multiple_gene_input),
                              inlist=(multiple_gene_input)))
                print("Does everything look okay? Enter Y for 'Yes' or N for 'No'")
                input_confirmation = raw_input("  Y/N: ")
                
                if (input_confirmation.upper()=="Y"):
                    pass
                elif(input_confirmation.upper()=="N"):
                    print("no worries, let's try again.")
                    raise InvalidMenuOption()
                else:
                    print("your input didn't make sense, let's start over.")
                    raise InvalidMenuOption()

            ##################################
            ##### Get the Gene ID Format #####
            ### run the user input menu
            UIn.setIDFormat(UserInput_Menus.inputIdFormatMenu())
                
            ### check the input for the next menu
            # if 0, back to the main menu
            if (UIn.getIDFormat() == 0):
                print("going back to the main menu!\n\n")
                UIn.setUploadType(UserInput_Menus.inputTypeMenu())
            # if within the range of options
            elif(1 <= UIn.getIDFormat() <= 6):
                ###################################
                ##### get the output file info ####   
                OutputFileDetails = UserInput_Menus.inputOutputFormatMenu()
                
                # check logic to see if they have a correctly formatted input
                if (OutputFileDetails[0] == 0):
                    print("going back to the main menu!\n\n")
                    UIn.setUploadType(UserInput_Menus.inputTypeMenu())
                    
                elif(1 <= OutputFileDetails[0] <= 3):
                    # set the outfile format
                    UIn.setOutFileFormat(OutputFileDetails[0])
                    # set the outdir 
                    UIn.setOutFileDir(OutputFileDetails[1])
                    # set the out filename
                    UIn.setOutFileName(OutputFileDetails[2])
                else:
                    print("The output format was not in the list, please try again.")
                    raise InvalidMenuOption()
                    
                ############################################
                ##### run submenu for Annotation Souce  ####
                UIn.setAnnotationSource(UserInput_Menus.inputAnnotationSourceMenu())
                ## back to main menu
                if (UIn.getAnnotationSource() == 0):
                     UIn.setUploadType(UserInput_Menus.inputTypeMenu())
                    
                elif(1 <= UIn.getAnnotationSource() <= 5):
                    
                    ####################################################
                    ##### get the annotations for a single gene ID  #### 
                    if (UIn.getUploadType() == 1):
                        print("Okay! Hang tight while the annotation(s) get extracted! \n Progress:  \n\t"),
                        # run the retriever to get the data 
                        OutData = UIn.runAnnotationRetriever()
                        # output the data
                        UserInput_Menus.WriteOutputFile(OutData, UIn.getOutFileFormat(), UIn.getOutFileDir(), UIn.getOutFileName())
                        # write a confirmation message
                        print("""\nYour input gene {gene} that is formatted as {GIS} was searched in {AnS} and output as a {OUTF} file\n"""
                                  .format(gene = UIn.getGeneID(),
                                          GIS = inputIDOpts[UIn.getIDFormat()][0],
                                          AnS = inputSourceFormatOpts[UIn.getAnnotationSource()][1],
                                          OUTF = inputOutputFormatOpts[UIn.getOutFileFormat()][1]
                                          )
                            )

                    ####################################################
                    ##### get the annotations for multiple gene IDs  ####                     
                    elif (UIn.getUploadType() == 2):
                        # print the confirmation message
                        print("Okay! Hang tight while the annotation(s) get extracted! \n Progress:  \n\t"),
                        
                        # preset lists to fill in a loop through the inputs
                        OutData_inputGeneId = []
                        OutData_Input_IdFormat = []
                        OutData_Output_AnnotationSource = []
                        OutData_Output_IdFormat = []
                        OutData_output_geneIDs = []
                        OutData_output_annotation = []
                        
                        # loop through the input ids retrieving data as needed
                        for ids in multiple_gene_input:
                            UIn.setGeneID(ids)
                            OutData = UIn.runAnnotationRetriever()
                            # fill in OutData Lists
                            OutData_inputGeneId.append(OutData["Input_GeneId"])
                            OutData_Input_IdFormat.append(OutData["Input_IdFormat"])
                            OutData_Output_AnnotationSource.append(OutData["Output_AnnotationSource"])
                            OutData_Output_IdFormat.append(OutData["Output_IdFormat"])
                            OutData_output_geneIDs.append(OutData["Output_GeneId"])
                            OutData_output_annotation.append(OutData["Annotation"])
                        
                        # merge the output into a single dictionary for the output writer handler
                        OutData_Merged = {"Input_GeneId":OutData_inputGeneId,
                                        "Input_IdFormat":OutData_Input_IdFormat,
                                        "Output_AnnotationSource":OutData_Output_AnnotationSource,
                                        "Output_IdFormat":OutData_Output_IdFormat,
                                        "Output_GeneId":OutData_output_geneIDs,
                                        "Annotation":OutData_output_annotation
                                        }
                        
                        ## confirmation message 
                        print("""\nYour input genes {gene} that is formatted as {GIS} was searched in {AnS} and output as a {OUTF} file\n"""
                                  .format(gene = multiple_gene_input,
                                          GIS = inputIDOpts[UIn.getIDFormat()][0],
                                          AnS = inputSourceFormatOpts[UIn.getAnnotationSource()][1],
                                          OUTF = inputOutputFormatOpts[UIn.getOutFileFormat()][1]
                                          )
                            )
                        ### output  data
                        UserInput_Menus.WriteOutputFile(OutData_Merged, UIn.getOutFileFormat(), UIn.getOutFileDir(), UIn.getOutFileName())
                                  
                else:
                    print("The annotation selection was not in the list, please try again.")
                    raise InvalidMenuOption()
                
            # otherwise through an erro
            else:
                print("The input ID format was not in the list, please try again.")
                raise InvalidMenuOption()
        
        elif (UIn.getUploadType() == 3):
            InputFile = UserInput_Menus.inputUploadFileMenu()
            
            ### check for the number of inputs
            ## Gene IDs Only
            # if three columns then we don't have file output info 
            if (len(InputFile[0])==3):
                ## print start message for user
                print("Okay, the IDs were uploaded! But we need some more information from you.\n")
                ## get the out file details
                OutputFileDetails = UserInput_Menus.inputOutputFormatMenu()
                ## set static variables for use
                UIn.setOutFileFormat(OutputFileDetails[0])      # set the outfile format
                UIn.setOutFileDir(OutputFileDetails[1])         # set the outdir 
                UIn.setOutFileName(OutputFileDetails[2])        # set the out filename
                
                ## return to main menu option
                if (UIn.getOutFileFormat() == 0):
                    print("going back to the main menu!\n\n")
                    UIn.setUploadType(UserInput_Menus.inputTypeMenu())
                    
                ## run the annotation retriever
                else:
                    # print start message for user
                    print("Okay! Hang tight while the annotation(s) get extracted! \n Progress:  ")
                    # setup blank lists to store looped data
                    OutData_inputGeneId = []
                    OutData_Input_IdFormat = []
                    OutData_Output_AnnotationSource = []
                    OutData_Output_IdFormat = []
                    OutData_output_geneIDs = []
                    OutData_output_annotation = []
                    
                    # loop through lines in the input file 
                    for InputLines in InputFile:
                        # set the variables from file
                        UIn.setGeneID(InputLines[0])                    # gene id to annotate
                        UIn.setIDFormat(int(InputLines[1]))             # gene id format
                        UIn.setAnnotationSource(int(InputLines[2]))     # target annotation source
                        # run annotation retriever 
                        OutData = UIn.runAnnotationRetriever()
                        # fill in OutData Lists
                        OutData_inputGeneId.append(OutData["Input_GeneId"])
                        OutData_Input_IdFormat.append(OutData["Input_IdFormat"])
                        OutData_Output_AnnotationSource.append(OutData["Output_AnnotationSource"])
                        OutData_Output_IdFormat.append(OutData["Output_IdFormat"])
                        OutData_output_geneIDs.append(OutData["Output_GeneId"])
                        OutData_output_annotation.append(OutData["Annotation"])     
                        
                    ## merge looped output for file writing
                    OutData_Merged = {"Input_GeneId":OutData_inputGeneId,
                                    "Input_IdFormat":OutData_Input_IdFormat,
                                    "Output_AnnotationSource":OutData_Output_AnnotationSource,
                                    "Output_IdFormat":OutData_Output_IdFormat,
                                    "Output_GeneId":OutData_output_geneIDs,
                                    "Annotation":OutData_output_annotation
                                    }
                    ### output  data
                    UserInput_Menus.WriteOutputFile(OutData_Merged, UIn.getOutFileFormat(), UIn.getOutFileDir(), UIn.getOutFileName())
                        
            ## Gene IDs + Output Information
            # if 6 columns then we have the output information s
            elif(len(InputFile[0])==6):
                print("Okay! Hang tight while the annotation(s) get extracted! \n Progress:  \n\t"),
                for InputLines in InputFile:
                    ## set variables required for loopin'
                    UIn.setGeneID(InputLines[0])                    # gene id to annotate
                    UIn.setIDFormat(int(InputLines[1]))             # gene id format
                    UIn.setAnnotationSource(int(InputLines[2]))     # target annotation source
                    UIn.setOutFileFormat(int(InputLines[3]))        # format of output file
                    UIn.setOutFileDir((InputLines[4]))              # directory for the output file
                    UIn.setOutFileName((InputLines[5]))             # name of output file 
                    # run the annotation retrievers
                    OutData = UIn.runAnnotationRetriever()
                    # Output data
                    UserInput_Menus.WriteOutputFile(OutData, UIn.getOutFileFormat(), UIn.getOutFileDir(), UIn.getOutFileName())
                    
            else:
                print("The input file did not have either 3 or 6 columns. Please check your input file.")
                print("the number of columns received was:  ", len(InputFile[0]))
                InvalidMenuOption()

        else:
            raise InvalidMenuOption()
            
        
        ### final output and leaver statement
        print("\nthank you for using the annotation interface!")
        break
       
    except:
        print("\nThere was an error, please try again.\n")
        UIn.setUploadType(UserInput_Menus.inputTypeMenu())
      
