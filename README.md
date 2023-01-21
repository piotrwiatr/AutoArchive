# AutoArchive
By Nathan Hart & Piotr Wiatr

AutoArchive automatically renames and relocates files based on their content and suggestions made by OpenAI's ChatGPT. AutoArchive was made as a project for DeltaHacks IX in 2023 by Piotr Wiatr and Nathan Hart. The goal of the project is to demonstrate how tasks that are easily expressed in human languages can be translated to complicated rigorously defined machine instructions through a natural language processor. As of 2023, ChatGPT is an incredibly powerful, general-purpose natural language processor that can be given explicit instructions to produce very specific results, such as returning a JSON object that contains information regarding the suggested name of a file along with its most suitable location (based on the content of the file and the list of available output folders). This program is a proof of concept, and suggests that general-purpose natural langauge processors may be an effective tool for prototyping complicated intelligent behaviour, without requiring a specific model to be trained for each application.

# Required Libraries
Due to the short development period of this project, a proper virtual environment was not created and thus no requirements.txt file was generated. If you wish to try out this particular software, ensure that you have the following libraries installed:

- openai
- PyPDF2
- python-pptx
- pytesseract
- textract
- cli
- numpy
- json

# How to use the script

Once all the libraries have been installed, open the "defaults.json" and modify the list to point to a list of output directories. The list should be in the format [directory name, recursively include subfolders (true/false), maximum recursion depth]. You can add more directories by appending more configurations to the "directories" list. 

In the chatgpt.py module, ensure that a valid OpenAI API key is provided, whether as a default parameter or by assigning openai.api_key to an environment variable. Please note that the more directories that are specified, the costlier each OpenAI request will be. (You can easily run out of credits if you do not limit your requests).

Finally, use python in a CLI to execute the script. You can use the --help argument to get a list of options. Primarily, you want to first specify a directory that contains all the files that you want to be renamed and/or relocated. Then, ensure you use the -d argument to grab the specified default output directories from the defaults.json file. -v stands for verbosity and will display the current process of the program. -r allows files to be renamed, -m allows files to be moved, -c allows the user to confirm whether a file should be moved/renamed if ChatGPT is uncertain about its suggestion (-cc allows the user to confirm ChatGPT's suggestion for every file. This is best for testing out the program). 

# Disclaimer
**Do NOT allow this program to run on documents containing sensitive information. It is submitted to OpenAI, and any content may be analyzed by the OpenAI team as plaintext.**
Due to the lack of sufficient development time, the software had to be principally programmed for our systems and may not produce consistent results on untested machines. Additionally, we are not responsible for how this script interfaces with your OpenAI account balance; an erroneous or sufficiently large request may result in excessive credit usage.
*There will be bugs in this code that may cause the program to crash, or behave unexpectedly. It is advised to test this in a virtual machine, if possible.*
It is also important to note that AutoArchive is meant to be a prototype, an example of how natural language processing can enable people to create things and complete complicated tasks without necessarily having the rigorous background to complete them. The ultimate goal of AutoArchive is to serve as a stepping stone, a demonstration of the utility of a natural language processor that is familiar with common human intentions and goals. 
