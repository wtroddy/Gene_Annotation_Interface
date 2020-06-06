#!/usr/bin/env python
"""BINF 690 | Annotation Project - User Input Handler
class of objects to manage the users input and data management
this class includes the getter, setter, and retriever functions that call on the API class
"""

from API_dir.API_Class import API
from Input_Options import input_options

inputIDOpts = input_options.inputIDOpts
inputSourceFormatOpts = input_options.inputSourceFormatOpts
inputOutputFormatOpts = input_options.inputOutputFormatOpts

API_Caller = API()
API_Caller.__init__()

class UserInput():
    """BINF 690 | Annotation Project - User Input Handler
    class of objects to manage the users input and data management
    this class includes the getter, setter, and retriever functions that call on the API class
    """  
    ######### Constructor #########
    def __init__ (self):
        self.upload_type = ""
        self.gene_id = ""
        self.id_format = ""
        self.outfile_format = ""
        self.outfile_dir = ""
        self.outfile_name = ""
        self.annotation_source = ""

    ######### Set Methods #########
    # Upload Type 
    def setUploadType (self, upload_type):
        self.upload_type = upload_type
        
    # Gene ID 
    def setGeneID (self, gene_id):
        self.gene_id = gene_id
        
    # ID Format    
    def setIDFormat (self, id_format):
        self.id_format = id_format

    # Out File Format    
    def setOutFileFormat (self, outfile_format):
        self.outfile_format = outfile_format
        
    # Out File Directory    
    def setOutFileDir (self, outfile_dir):
        self.outfile_dir = outfile_dir

    # Out File Name    
    def setOutFileName (self, outfile_name):
        self.outfile_name = outfile_name       
        
    # Annotation Source    
    def setAnnotationSource (self, annotation_source):
        self.annotation_source = annotation_source
        

    ######### Get Methods #########
    # Upload Type
    def getUploadType (self):
        return self.upload_type
        
    # Gene ID 
    def getGeneID (self):
        return self.gene_id
        
    # ID Format    
    def getIDFormat (self):
        return self.id_format

    # Out File Format  
    def getOutFileFormat (self):
        return self.outfile_format

    # Out File Directory    
    def getOutFileDir (self):
        return self.outfile_dir

    # Out File Name    
    def getOutFileName (self):
        return self.outfile_name
        
    # Annotation Source  
    def getAnnotationSource (self):
        return self.annotation_source
    
    #### Annotation Retriever Driver ####
    def runAnnotationRetriever(self):
        """
        annotation retriever: this is the workhorse of the scripts, it doesn't require any input but requires that appropriate getter/setter options have already been ran
        """
        ### vars to fill in as we go
        # set blank lists
        output_dictionary_inputGeneId = []
        output_dictionary_Input_IdFormat = []
        output_dictionary_Output_AnnotationSource = []
        output_dictionary_Output_IdFormat = []
        output_dictionary_output_geneIDs = []
        output_dictionary_output_annotation = []
        tax_ids_search = []
        
        if (self.getAnnotationSource() == 1) or (self.getAnnotationSource() == 2) or (self.getAnnotationSource() == 3) or (self.getAnnotationSource() == 4):
            
            ### call the conversion handler function to determine if this needs to be converted
            ConvertedID = API_Caller.IDConversionHandler(inputIDOpts[self.getIDFormat()][0],                    # Set the User Input ID Format
                                                         inputSourceFormatOpts[self.getAnnotationSource()][2],  # Set the Required ID Format  
                                                         self.getGeneID()                                       # Pass in the current GeneID
                                                         )
                    
            for ids in ConvertedID:
                print("-"),
                output_dictionary_inputGeneId.append(self.getGeneID())
                output_dictionary_Input_IdFormat.append(inputIDOpts[self.getIDFormat()][0])
                output_dictionary_Output_AnnotationSource.append(inputSourceFormatOpts[self.getAnnotationSource()][1])
                output_dictionary_Output_IdFormat.append(inputSourceFormatOpts[self.getAnnotationSource()][0])         
    
                ### NCBI Taxonomy
                if (inputSourceFormatOpts[self.getAnnotationSource()][0] == "NCBI_Taxonomy"):
                    # Set the converted IDs as UniRef 100 values 
                    API_Caller.setUniRefID(ids)
                    
                    # Call the Taxon Retriever to convert the uniref 100 values to taxaIDs
                    retrieved_taxa_ids = API_Caller.TaxonRetriever()
                                    
                    # expand the taxa ids into a single list
                    for tax_ids in retrieved_taxa_ids:
                        if tax_ids:
                            tax_ids_search.append(tax_ids)
                    
                    # simplify into unique values only 
                    tax_ids_converted = list(set(tax_ids_search))
                    # join into a single string for API handler
                    tax_ids_joined = ",".join(tax_ids_converted)
                    # set the taxa ID
                    API_Caller.setTaxaID(tax_ids_joined)
                    
                    ## call the API and outut results
                    output_dictionary_output_geneIDs.append(API_Caller.getTaxaID())
                    output_dictionary_output_annotation.append(API_Caller.NCBITaxonomy())
                                
                ### Ensembl
                elif (inputSourceFormatOpts[self.getAnnotationSource()][0] == "ENSEMBL_ID"):
                    id_str = ids
                    API_Caller.setEnsemblID(ids)
                    output_dictionary_output_geneIDs.append(API_Caller.getEnsemblID())
                    output_dictionary_output_annotation.append(API_Caller.Ensembl())            
                
                ### KEGG
                elif (inputSourceFormatOpts[self.getAnnotationSource()][0] == "KEGG_ID"):
                    id_str = str(ids)
                    API_Caller.setKeggID(id_str)
                    output_dictionary_output_geneIDs.append(API_Caller.getKeggID())
                    output_dictionary_output_annotation.append(API_Caller.KeggAPI())            
                
                ### Uniref
                elif (inputSourceFormatOpts[self.getAnnotationSource()][0] == "NF100"):
                    id_str = str(ids)
                    API_Caller.setUniRefID(id_str)
                    output_dictionary_output_geneIDs.append(API_Caller.getUniRefID())
                    output_dictionary_output_annotation.append(API_Caller.UniRef100())
                    
            
            #Output_Data
            Output_Data = {"Input_GeneId":output_dictionary_inputGeneId,
                            "Input_IdFormat":output_dictionary_Input_IdFormat,
                            "Output_AnnotationSource":output_dictionary_Output_AnnotationSource,
                            "Output_IdFormat":output_dictionary_Output_IdFormat,
                            "Output_GeneId":output_dictionary_output_geneIDs,
                            "Annotation":output_dictionary_output_annotation,
                            }

            #return Output_Data                                  
            return Output_Data


        elif (self.getAnnotationSource() == 5):
            ### loop through each option
            
            #####################
            ###### NCBI ######
            # call the conversion handler function to determine if this needs to be converted
            ConvertedID = API_Caller.IDConversionHandler(inputIDOpts[self.getIDFormat()][0],                    # Set the User Input ID Format
                                                         "NF100",                                               # Set the Required ID Format  
                                                         self.getGeneID()                                       # Pass in the current GeneID
                                                         )
            for ids in ConvertedID:
                print("-"),
                output_dictionary_inputGeneId.append(self.getGeneID())
                output_dictionary_Input_IdFormat.append(inputIDOpts[self.getIDFormat()][0])
                output_dictionary_Output_AnnotationSource.append("NCBI Taxonomy")
                output_dictionary_Output_IdFormat.append("taxa_id")         

                # Set the converted IDs as UniRef 100 values 
                API_Caller.setUniRefID(ids)
                
                # Call the Taxon Retriever to convert the uniref 100 values to taxaIDs
                retrieved_taxa_ids = API_Caller.TaxonRetriever()
                                
                # expand the taxa ids into a single list
                for tax_ids in retrieved_taxa_ids:
                    if tax_ids:
                        tax_ids_search.append(tax_ids)
                
                # simplify into unique values only 
                tax_ids_converted = list(set(tax_ids_search))
                # join into a single string for API handler
                tax_ids_joined = ",".join(tax_ids_converted)
                # set the taxa ID
                API_Caller.setTaxaID(tax_ids_joined)
                
                ## call the API and outut results
                output_dictionary_output_geneIDs.append(API_Caller.getTaxaID())
                output_dictionary_output_annotation.append(API_Caller.NCBITaxonomy())            
            
            #####################
            ###### Ensembl ######
            # call the conversion handler function to determine if this needs to be converted
            ConvertedID = API_Caller.IDConversionHandler(inputIDOpts[self.getIDFormat()][0],                    # Set the User Input ID Format
                                                         "ENSEMBL_ID",                                          # Set the Required ID Format  
                                                         self.getGeneID()                                       # Pass in the current GeneID
                                                         )
            for ids in ConvertedID:
                print("-"),
                output_dictionary_inputGeneId.append(self.getGeneID())
                output_dictionary_Input_IdFormat.append(inputIDOpts[self.getIDFormat()][0])
                output_dictionary_Output_AnnotationSource.append("Ensembl")
                output_dictionary_Output_IdFormat.append("ENSEMBL_ID")         
                id_str = ids
                API_Caller.setEnsemblID(ids)
                output_dictionary_output_geneIDs.append(API_Caller.getEnsemblID())
                output_dictionary_output_annotation.append(API_Caller.Ensembl())
            
            #####################
            ###### KEGG_ID ######
            # call the conversion handler function to determine if this needs to be converted
            ConvertedID = API_Caller.IDConversionHandler(inputIDOpts[self.getIDFormat()][0],                    # Set the User Input ID Format
                                                         "KEGG_ID",                                             # Set the Required ID Format  
                                                         self.getGeneID()                                       # Pass in the current GeneID
                                                         )
            for ids in ConvertedID:
                print("-"),
                output_dictionary_inputGeneId.append(self.getGeneID())
                output_dictionary_Input_IdFormat.append(inputIDOpts[self.getIDFormat()][0])
                output_dictionary_Output_AnnotationSource.append("KEGG")
                output_dictionary_Output_IdFormat.append("KEGG_ID")         

                id_str = ids
                API_Caller.setEnsemblID(ids)
                output_dictionary_output_geneIDs.append(API_Caller.getKeggID())
                output_dictionary_output_annotation.append(API_Caller.KeggAPI())      

            #####################
            ###### Uniref ######
            # call the conversion handler function to determine if this needs to be converted
            ConvertedID = API_Caller.IDConversionHandler(inputIDOpts[self.getIDFormat()][0],                    # Set the User Input ID Format
                                                         "NF100",                                               # Set the Required ID Format  
                                                         self.getGeneID()                                       # Pass in the current GeneID
                                                         )
            for ids in ConvertedID:
                print("-"),
                output_dictionary_inputGeneId.append(self.getGeneID())
                output_dictionary_Input_IdFormat.append(inputIDOpts[self.getIDFormat()][0])
                output_dictionary_Output_AnnotationSource.append("UniRef_100")
                output_dictionary_Output_IdFormat.append("NF100")         
                id_str = str(ids)
                API_Caller.setUniRefID(id_str)
                output_dictionary_output_geneIDs.append(API_Caller.getUniRefID())
                output_dictionary_output_annotation.append(API_Caller.UniRef100())



            #####################
            ###### Output All Data ######
            #Output_Data
            Output_Data = {"Input_GeneId":output_dictionary_inputGeneId,
                            "Input_IdFormat":output_dictionary_Input_IdFormat,
                            "Output_AnnotationSource":output_dictionary_Output_AnnotationSource,
                            "Output_IdFormat":output_dictionary_Output_IdFormat,
                            "Output_GeneId":output_dictionary_output_geneIDs,
                            "Annotation":output_dictionary_output_annotation,
                            }

            #return Output_Data                                  
            return Output_Data
                    
            
        else:
            print ("you didn't pick an appropriate input. please try again")          