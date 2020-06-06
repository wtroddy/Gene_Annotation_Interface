#!/usr/bin/env python
"""BINF 690 | Annotation Project - API_Class
class to manage API caller functions 
"""

### Import Packages
import urllib
import urllib2
import xml.etree.ElementTree as ET
import csv
import requests
import sys
from bioservices.kegg import KEGG
from API_dir.IdManager import IdManager

class API(IdManager):
    """
    API Class that manages functions for each possible caller
    Each function calls details defined in IdManager
    This class solely manages the interaction with the API caller and is not used to manage the input settings
    """
    ######### Constructor #########
    def __init__ (self):
        IdManager.__init__(self)

    ######### NCBI Taxonomy Function #########
    def NCBITaxonomy(self):
              
        ncbi_esum_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    
        taxa_params = {
        "db":"taxonomy",
        "id":self.taxa_id
        }
        
        data = urllib.urlencode(taxa_params)
        ncbi_request = urllib2.Request(ncbi_esum_url, data)
        ncbi_response = urllib2.urlopen(ncbi_request)
        ncbi_page = ncbi_response.read()
        
        ncbi_tree = ET.fromstring(ncbi_page)
        
        taxa_data = {}
        
        for child in ncbi_tree:
            ItemDict = {}
            for i in child:
                if i.tag=="Id":
                    ID = i.text
                if i.tag=="Item":
                    ItemName = i.attrib["Name"]
                    ItemValue = i.text
                    ItemDict[ItemName] = ItemValue
                taxa_data[ID] = ItemDict

        return taxa_data

    
    ######### UniRef100 Function #########
    def UniRef100(self):
        uniref_id = self.uniref_id
        
        # static variables
        #uniref_url = "https://www.uniprot.org/uniref/UniRef100_"

        uniref_url = "https://www.uniprot.org/uniref/"
        uniref_id_url = uniref_url+uniref_id+".tab"
        response = urllib2.urlopen(uniref_id_url)
        
        # dict method
        uniref_data = []
        
        csv_reader = csv.DictReader(response, delimiter='\t')
            	
        for line in csv_reader:
            uniref_data.append(dict(line))        
        
        return uniref_data 
    
    ######### Ensembl Function #########    
    def Ensembl(self):
        
        ensembl_id = self.ensembl_id
        
        ensembl_url = "https://rest.ensembl.org"
        ensembl_req = "/lookup/id/"+ensembl_id+"?"
                
        ensembl_request = requests.get(ensembl_url+ensembl_req, headers={ "Content-Type" : "application/json"})
        
        if not ensembl_request.ok:
          ensembl_request.raise_for_status()
          sys.exit()
         
        ensembl_output = ensembl_request.json()
        return ensembl_output

    ######### KEGG Function #########    
    def KeggAPI(self):
        kegg_data = KEGG().parse(KEGG().get(self.kegg_id))        
        return kegg_data
    
