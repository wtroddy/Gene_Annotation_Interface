#!/usr/bin/env python
"""BINF 690 | Annotation Project - Input Option References
Master reference dictionaries of appropriate options throughout the script
"""

inputOutputFormatOpts = {1: ["csv", "Comma Seperated Values (.csv)"],
                         2: ["tsv", "Tab Seperated Values (.tsv)"],
                         3: ["json", "JavaScript Object Notation (.json)"]
                         }

inputTypeOpts = {1: ["single_GeneID", "enter a single gene ID"],
                 2: ["multiple_GeneIDs", "enter a list of gene ID's"],
                 3: ["file_upload", "upload a file with gene ID(s)"]
                 }

inputIDOpts = {1: ["ENSEMBL_ID", "Ensemble ID"],
               2: ["P_ENTREZGENEID", "Entrez ID"],
               3: ["KEGG_ID", "KEGG ID"],
               4: ["NF100", "UNIREF 100 ID"],
               5: ["UPARC", "UNIPARC ID"],
               6: ["ACC", "Uniprot Accession ID (ACC)"],
               }

inputSourceFormatOpts = {1: ["NCBI_Taxonomy", "NCBI Taxonomy", "NF100"],
                         2: ["ENSEMBL_ID", "Ensembl", "ENSEMBL_ID"],
                         3: ["KEGG_ID", "KEGG", "KEGG_ID"],
                         4: ["NF100", "UNIREF 100", "NF100"],
                         5: ["ALL", "All Above Sources", "ALL"]
                         }