'''
Created on May 23, 2017

@author: kevin
'''


# from setuptools import setup, find_packages

# setup(
#     name = "ContinuousContractMaker",
#     version = "0.1",
#     packages=find_packages(),
#     entry_points={
#         'gui_scripts':[
#             'Continuous_Contract_Maker=rollover.main:StartMainWindow']
#     }
# )


# import py2exe
# from distutils.core import setup
#  
# setup(windows=[{"script":"main.pyw"}], 
#       options={"py2exe":{"includes":["sip"]}})


# from distutils.core import setup
# import py2exe
# 
# setup( console=[{"script": "rollover\main.py"}] )



import os
import sys
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = "F:\\OneDrive\\Programming\\Python\\Python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "F:\\OneDrive\\Programming\\Python\\Python36\\tcl\\tk8.6"
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'


executables = [
    Executable('rollover\\main.pyw', base=base)
]

setup(name='test',
      version='0.1',
      description='test',
      executables=executables
      )