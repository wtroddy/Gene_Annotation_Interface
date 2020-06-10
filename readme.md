# Annotation Project 

## Description
Collection of python programs that will convert gene ID's and return relevant data from other sources.

## Prior to Running
Required Packages:

A full list of the packages used for this are:
- import urllib
- import urllib2
- import xml.etree.ElementTree as ET
- import csv
- import json
- import requests
- import sys
- import re
- from bioservices.kegg import KEGG
- from __future__ import print_function

Locally Imported:
- from API_dir.API_Class import API
- from Input_Options.UserInput import UserInput 
- from Input_Options import input_options
- from Input_Options import UserInput_Menus
	
## To Run:
The driver script is "annotation_interface_menu.py" run this file with the planned dir structure.

## Dir Structure
	+- Annotation_Interface (dir holding final version for submission)	
	|	|
	|	+- API_dir (dir holding API classes, functions)
	|	|	|
	|	|	+- API_class.py, IdManager.py
	|	|	|
	|	+- Input_Options (dir holding UI, menus, and input details)
	|	|	|
	|	|	+- input_options.py, UserInput.py, UserInput_Menus.py
	|	|	|
	|	+- testing (dev, test I/O data)
	|	|	|
	|	+- annotation_interface_menu.py
	
## Future Improvements 
Future changes will include enhanced support of API callers including threshold limiting and API keys. 
