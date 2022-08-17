"""
Created by MZI-Anonymous
Purpose: speeding up dictionary attack(password cracking) using multiprocessing .
by dividing large wordlist files into small pieces to handle much faster.
"""

import argparse
import os
import sys
import logging
import subprocess
import platform
import random
import threading
import time
import shutil

mainFolderName = "w_lists"
baseFolderLocation_onWindows = "C:\\Users\\Mehmet\\Desktop"
baseFolderLocation_onLinux = "/HOME"
baseFolderLocation = ""

wordLimitSize = 200000  # word limit size per file

filesReady = []
FilesReadyLocation = "C:\\Users\\Mehmet\\Desktop\\FilesReady.txt"
mainFolderLocation = baseFolderLocation_onWindows + os.sep + mainFolderName
logging.basicConfig(filename="logfile-1.log")


def analyze_files(input_files):
    global filesReady
    files_to_divide = []
    print("attention to:", input_files)
    for file in input_files:
        with open(file, "r", encoding='latin-1') as File:
            line_count = len(File.readlines())
            print(line_count)
        if line_count < wordLimitSize * 2:
            print("{} has ben added to filesReady list.".format(file))
            filesReady.append(file)
            print(f"filesReady:{filesReady}")
        else:
            files_to_divide.append(file)  # the files to be break down into small pieces.
            print("{} has ben added to files_to_divide list.".format(file))
            print(f"files_to_divide:{files_to_divide}")
    return files_to_divide.copy()


def divide_files(files: list, output_location=mainFolderLocation, word_count_per_file=wordLimitSize):
    global filesReady
    logging.info("divide_files function started executing...")
    file_count_to_create = 0
    print(f"output_location: {output_location}")
    if os.path.exists(output_location):
        print(f"{output_location} is already exist! New data wil be override! Are you sure?")
        answer = input("'Y' or 'N':")
        if answer == 'Y' or 'y':
            shutil.rmtree(output_location)

            print("Removed output folder")
            logging.info("Removed output folder.")
        elif answer == 'N' or 'n':
            print("exiting...")
            sys.exit()
        else:
            print("type error")
            print("exiting...")
            sys.exit()

    os.mkdir(output_location)
    logging.info("Directory-{}- Created".format(output_location.split(os.sep)[-1]))
    start_point = os.getcwd()
    os.chdir(output_location)
    logging.info("Moved to {}".format(output_location))
    m = 0
    a = 0
    b = 0
    c = 0
    print("loop is starting")
    print(files)
    print(type(files))
    for file in files:
        with open(file, "r", encoding='latin-1') as MainFile:
            read_file = MainFile.readlines()
            print(f"file contains {len(read_file)} words")
            x = wordcount = len(read_file)
            y = word_count_per_file
            z = result = int(x/y)
            k = remainder = x % y
            n = file_count_to_create = 0
            print(f"x={x}, y={y}, z={z}, k={k}")
            if k == 0:
                n = z
                for i in range(n):
                    filename = str(file).split('\\')[-1] + f"-{m}.txt"
                    b = y * (i+1)
                    a = b - y
                    with open(filename, "w", encoding='utf-8') as ChildFile:
                        m += 1
                        ChildFile.writelines(read_file[a:b])
                    filesReady.append(mainFolderLocation + os.sep + filename)
                    print(f"{mainFolderLocation + os.sep + filename} added to filesReady list.")
            else:
                n = z
                for i in range(n):
                    filename = str(file).split('\\')[-1] + f"-{m}.txt"
                    b = y * (i + 1)
                    a = b - y
                    if i != n-1:
                        c = b
                    else:
                        c = b + k
                    with open(filename, "w", encoding='utf-8') as ChildFile:
                        m += 1
                        ChildFile.writelines(read_file[a:c])
                    filesReady.append(mainFolderLocation + os.sep + filename)
                    print(f"{mainFolderLocation + os.sep + filename} added to filesReady list.")


def get_input_files(file_location: str):
    files_input = []
    if os.path.exists(file_location):
        print(f"{file_location} exists.")
        logging.info("path exist.")
        if not os.path.isdir(file_location):
            print(f"{file_location} is a file location.")
            logging.info(f"{file_location} is a file location.")
            files_input.append(file_location)
            return files_input.copy()
        else:
            print(f"{file_location} is a folder location.")
            logging.info(f"{file_location} is a folder location.")

            # for root, dirs, files in os.walk(path):
            #     for name in files:
            #         print(os.path.join(root, name))
            os.environ["COMSPEC"] = 'pwsh'  # to be able to use powershell 7.

            command = [f'(Get-ChildItem -Path "{file_location}" -File -Recurse).FullName']
            p = subprocess.Popen(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE)
            out = p.communicate()[0].split("\n")[:-1]
            print(f"out: {out}")
            files_input.extend(out)
            print(f"files_input: {files_input}")
            return files_input.copy()
    else:
        print(f"{file_location} does not exist or invalid!")
        logging.info(f"{file_location} does not exist or invalid!")
        sys.exit()


# def get_file_word_count(filepath:str):
#     with open(filepath, "r", encoding='latin-1') as File:
#         line_count = len(File.readlines())
#     return line_count


# def identifier(basename: str):
#     id_used = []
#     while True:
#         random_id = random.randint(0, 10000)
#         if random_id not in id_used:
#             with open('C:\\Users\\Mehmet\\IDs.txt', 'w') as f:
#                 f.w()
#             return random_id


# def execute_pwsh_cmd(command: list):
#     os.environ["COMSPEC"] = 'pwsh'  # to be able to use powershell 7.
#     p = subprocess.Popen(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="divide files into small pieces to handle at the same time.")
    parser.add_argument("-p", "--path", help="wordlist(s) location be either a folder or a file", type=str)
    parser.add_argument("-o", "--output", help="folder name for divided wordlist files", type=str,
                        default=mainFolderLocation)
    args = parser.parse_args()
    path = str(args.path)
    output = str(args.output)

    divide_files(analyze_files(get_input_files(path)))

    if os.path.exists("C:\\Users\\Mehmet\\Desktop\\files.txt"):
        os.remove("C:\\Users\\Mehmet\\Desktop\\files.txt")
        print("files.txt removed")

    with open("C:\\Users\\Mehmet\\Desktop\\files.txt", "w") as files:
        files.write("\n".join(filesReady))
