#!/usr/bin/env python
"""BINF 690 | Annotation Project - IdManager
class to manage id data, getter, setter, converter functions include
"""

### Import Packages
import urllib
import urllib2



class IdManager():
    """
    IdManager is the class that handles all getter/setter/converter functions for specific IDs, see specific functions for more details
    """
    ######### Constructor #########
    def __init__ (self):
        self.taxa_id = ""
        self.uniref_id = ""
        self.ensembl_id = ""
        self.kegg_id = ""
        
    ######### Set Methods #########
    # taxonomy 
    def setTaxaID (self, taxa_id):
        self.taxa_id = taxa_id
        
    # uniref id
    def setUniRefID (self, uniref_id):
        self.uniref_id = uniref_id
        
    # Ensembl ID    
    def setEnsemblID (self, ensembl_id):
        self.ensembl_id = ensembl_id

    # Kegg ID    
    def setKeggID (self, kegg_id):
        self.kegg_id = kegg_id

    ######### Get Methods #########
    # taxonomy ID 
    def getTaxaID (self):
        return self.taxa_id
    
    # uniref ID 
    def getUniRefID (self):
        return self.uniref_id
    
    # Ensembl ID
    def getEnsemblID (self):
        return self.ensembl_id
    
    # Kegg ID
    def getKeggID (self):
        return self.kegg_id

    ######### UniProt Converter Function #########
    def UniProtConvert(self, informat, outformat, ids):
        ### static variables
        uniprot_url = "https://www.uniprot.org/uploadlists/"
        
        params = {
        "from":informat,
        "to":outformat,
        "format":"tab",
        "query":ids
        }
        
        data = urllib.urlencode(params)
        request = urllib2.Request(uniprot_url, data)
        response = urllib2.urlopen(request)
        
        uniprot_data = []
        line_counter = 0
        
        for line in response.readlines():
            line_counter += 1
            if line_counter == 1:
                pass
            else:
                uniprot_data.append(line.rstrip("\n").split("\t")[1])
        
        return uniprot_data
    
    ######### Converter Function Wrapper #########
    def IDConversionHandler(self, informat, outformat, ids):
        out_id = []
        
        if informat == outformat:
            out_id.append(ids)
        elif informat == "ID":                                                      #### UPDATE THE UNIPROT ID IN DICTIONARY!!!
            out_id = self.UniProtConvert(informat, outformat, ids)
            #update the out id format into a string
            #out_id = " ".join(out_id)
            #print("ID Input: ", out_id)
        else:
            acc_id = self.UniProtConvert(informat, "ACC", ids)
            # remove any duplicates
            acc_id = list(set(acc_id))
            acc_id = " ".join(acc_id)
            #print("acc_id output: ", acc_id)
            out_id = self.UniProtConvert("ACC", outformat, acc_id)
            # remove any duplicates
            out_id = list(set(out_id))
            #out_id = " ".join(out_id)
            #print("mismatched output: ", out_id)
        return out_id

    ######### UniRef100 - NCBI Taxo Converter Function #########
    def TaxonRetriever(self):
        uniref_id = self.uniref_id
        
        # static variables
        uniref_url = "https://www.uniprot.org/uniref/"

        uniref_id_url = uniref_url+uniref_id+".tab"
        response = urllib2.urlopen(uniref_id_url)
        
        taxo_convert = []
        line_counter = 0
        
        for line in response.readlines():
            line_counter += 1
            if line_counter == 1:
                pass
            else:
                id_data = line.rstrip("\n").split("\t")
                taxo_convert.append(id_data[5])        
        
        #self.taxa_id = taxo_convert
        return taxo_convert
    