import cli as c
import processing as p

confidence = c.verification if c.verification else 0

if not c.auto:
    print("-- AutoArchive pre-alpha --")
    print("An experimental demonstration of using generalized large language models as data-oriented natural language interface\n")

    print("The following files have been selected to move: ----")
    for i in range(len(c.input_files)):
        if i <= 4:
            print(c.input_files[i], end="")
        else:
            if i == 5:
                print(f"... + {len(c.input_files) - 1 - i} other files ...")

    print("\n\nThe following folders are available to store in: ----")
    for i in range(len(c.output_folders)):
        if i <= 4:
            print(c.output_folders[i], end="\t")
        else:
            if i == 5:
                print(f"\n... + {len(c.output_folders) - 1 - i} other locations ...")

    proceed = input("\n\nWould you like to proceed? With this operation? (Y/N) ").lower()
else:
    proceed = "yes"

if proceed not in ("n", "no"):
    process = p.Processor()

    process.process(c.input_files, c.output_folders, confidence, c.rename, c.move, c.verbose, c.debug)
else:
    print("\nProcess aborted.")