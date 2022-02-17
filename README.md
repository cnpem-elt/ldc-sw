# LDC SW - Leakage Detection Circuit Software

## What is LDC?
The Leakage Detection Circuit is an electronic board developed by the **Electronics Systems and Instrumentation 
Group** (SEI) of the **National Center of Research and Materials** ([CNPEM](https://cnpem.br/)) in Brazil.<br>
The board measures the leakage current of the Sirius power supplies then sends its values to store and plot in Sirius
Archiver.<br>
The objective of this application is to detect any problem with current leak and help to monitor the supplies during
their operation.

## What is LDC Software?
This module was provided to test the functionalities of the LDC Board and validate the project concept.<br>
It handles the communication between a bench power supply with SCPI, [PyDRS](https://pypi.org/project/pydrs/) and the
LDC Board itself.<br>
The code is divided by three principal scripts:
- SCPI Commands
- LDC Commands
- Accuracy Test

These three scripts communicate between themselves to provide the entire functionality of testing the LDC Board 
properly. To explain better what LDC SW does, there are a few first concepts.

### SCPI Communication
The **SCPI Commands** module handles the communication between the bench power supply and the LDC SW, providing 
functions to control Keysight equipments with the [PyVISA](https://pyvisa.readthedocs.io/en/latest/) library.

### PyDRS Communication
With the **LDC Commands** script, the PyDRS module is connected to a testing assembly containing an **IIB** and a 
communication module that sends the BSMP packages to the connected PC.<br>
All the BSMP communication is handled by LDC SW with the PyDRS module.

### Accuracy Test
This is the module that provides the general test of the LDC Board. It assembles the functionalities of the other two
codes and generates plots and sample data of the tests.

## Prerequisites
- [python==3.6](https://www.python.org/downloads/release/python-3612/) **at least**
- matplotlib==3.5.1
- numpy==1.22.2
- pydrs==1.1.1
- PyVISA==1.11.3

All prerequisites can be found in the
[_requirements.txt_](https://github.com/cnpem-elt/ldc-sw/blob/enhancement/requirements.txt) file.

## Installation Guide
Firstly clone the project repository from [Github](https://github.com/cnpem-elt/ldc-sw/tree/main) to 
**your_local_folder** with the following command:
```command
git clone https://github.com/cnpem-elt/ldc-sw.git
```
Then, go to the **ldc-sw** folder in your computer and install the prerequisites for this module by running the 
requirements file with the following command:
```command
python -m pip install -r requirements.txt
```
After these steps, all the configurations to use ldc-sw should be installed.