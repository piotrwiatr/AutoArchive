import argparse
import json
import os

def getSubDirectories(directory, depth):

    if depth <= 0:
        return []
    
    contents = os.listdir(directory)
    directories = [directory + '/' + d for d in contents if os.path.isdir(directory + '/' + d)]
    allDir = directories.copy()

    if directories:
        for each in directories:
            allDir += getSubDirectories(each, depth - 1)

    return allDir

parser = argparse.ArgumentParser()
parser.add_argument("include", nargs='*', help="relative or absolute paths to files or folders containing files to add to process.")
parser.add_argument("-r", "--rename", help="enable smart rename",
                    action="store_true")
parser.add_argument("-m", "--move", help="enable smart move",
                    action="store_true")
parser.add_argument("-d", "--defaults", help="include default output paths specified in `defaults.json`",
                    action="store_true")
parser.add_argument("-x", "--exclude", help="relative or absolute paths to files or folders to exclude from processing",
                    action="extend", nargs="+", type=str)
parser.add_argument("-o", "--output", help="relative or absolute paths to folders to be considered for output",
                    action="extend", nargs="+", type=str)
parser.add_argument("-v", "--verbose", help="request confirmation for files '-v' requests review for files ChatGPT identifies as being unsure, '-vv' requests review for all files",
                    action="count")
parser.add_argument("-c", "--confirm", help="request confirmation for files '-c' requests review for files ChatGPT identifies as being unsure, '-cc' requests review for all files",
                    action="count")
parser.add_argument("-b", "--debug", help="supply a debug file listing all file modifications, debug file stored in the path indicated by `defaults.json`",
                    action="store_true")
parser.add_argument("-a", "--auto", help="skip confirmation",
                    action="store_true")
args = parser.parse_args()

rename = args.rename
move = args.move
verification = args.confirm
verbose = args.verbose
auto = args.auto

if args.debug:
    with open('defaults.json', 'r') as fh:
        defaults = json.load(fh)
    debug = defaults['debug']
else:
    debug = None

output_folders = []

input_files = []

if args.defaults:
    with open('defaults.json', 'r') as fh:
        defaults = json.load(fh)

    for folder in defaults['directories']:

        output_folders.append(folder[0])

        if folder[1] == True:
            output_folders += getSubDirectories(folder[0], folder[2])

if args.output:
    for each in args.output:

        if os.path.isdir(each):
            output_folders.append(os.path.abspath(each).replace('\\','/'))
        else:
            continue

if args.include:
    for each in args.include:

        print(each)

        if args.exclude:
            if each in list(args.exclude):
                continue

        if os.path.isdir(each):
            path = os.path.abspath(each).replace('\\', '/')
            contents = os.listdir(path)
            input_files += [path + '/' + f for f in contents if os.path.isfile(path + '/' + f) and not f.startswith('.')]

        elif os.path.isfile(each):

            path = os.path.abspath(each).replace('\\', '/')

            input_files.append(path)

            found = False
            for i in range(len(path)):
                if (path[len(path) - 1 - i] == "/" or path[len(path) - 1 - i] == "\\") and not found:
                    fol = path[0:len(path) - 1 - i]
                    if os.path.isdir(fol):
                        output_folders.append(fol)
                        found = True

