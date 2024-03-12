# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 16:54:13 2024

@author: thiag
"""
import subprocess
import os


working_dir = 'C:\ATP\atpdraw\work\VAO_01_estocastico.atp'
command = r"runAtp.exe" ,r'"' + working_dir

subprocess.run([r"C:\ATP\tools\runATP.exe" ,r'"' + working_dir + '"'])


print('acabou')