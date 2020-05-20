#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import argparse
import shutil
from datetime import datetime



def main():
    global currentPath
    global maxDepth

    currentPath = os.getcwd()
    parser = prepareParser()
    args = parser.parse_args()

    currentPath = currentPath + args.path
    maxDepth = args.depth or 0

    if(not args.force and (currentPath in config.dangerousPaths)):
        print("Dangerous path detected, sort will not exitting")
        return
    
    if(args.safe and not (currentPath in config.safePaths)):
        print("Safe mode active, unsafe path detected, exitting")
        return

    # if(args.backup):
    #     backup()

    constructFolders()
    moves = sort()
    moveFiles(moves)
    print(f"Current path is {currentPath}")
    


def constructFolders():
    for folder in config.folders.keys():
        if(not os.path.exists(currentPath+os.sep+folder)):
            os.mkdir(currentPath+os.sep+folder)

def sort():
    print("Beginning Sort")
    count = 0
    moves = []
    startinglevel = currentPath.count(os.sep)
    for subdir, dirs, files in os.walk(currentPath, topdown=True):
        dirs[:] = [d for d in dirs if d not in config.folders.keys()]

        level = subdir.count(os.sep) - startinglevel
        if(level > maxDepth):
            print(f"Max allowed depth exceeded, returning with {count} sorted files")
            return moves

        for filename in files:
            if (filename == "sort.py"):
                continue
            filepath = subdir + os.sep + filename
            destination = currentPath + getDest(filename, filepath)
            if(os.path.exists(destination)):
                destination = currentPath + getDest(f"1{filename}", filepath)
            moves.append((filepath,destination))
            count+=1
    print(f"Sort Complete on {count} files")
    return moves

# def backup():
#     shutil.make_archive(f"{currentPath}{os.sep}backup{os.sep}{datetime.today()}", 'zip', currentPath)

def moveFiles(moves):
    for move in moves:
        os.rename(move[0], move[1])


def getDest(filename, filepath):
    for key, val in config.folders.items():
        if(filename.lower().endswith(val)):
            return f"{os.sep}{key}{os.sep}{filename}"
    return f"{os.sep}misc{os.sep}{filename}"

def prepareParser():
    parser = argparse.ArgumentParser(description="Sort files and sub dirs in a folder")
    parser.add_argument('-f', '--force', action='store_true', help="Force run in unsafe mode")
    parser.add_argument('path', help="Relative path to the folder to be sorted")
    parser.add_argument('-d', '--depth', type=int, help="Depth of sort (Default 0)")
    parser.add_argument('-s','--safe', help="Safe mode sort, (only allow the sort to run in configured directories)")
    parser.add_argument('-b', '--backup', action="store_true", help="Backup all sorted files in a zipped archive (currently inactive)")
    return parser


class config:
    folders = {
        "images": ("png", "jpg", "gif", "ps", "svg", "ico", "bmp", "jpeg"),
        "videos": ("mp4", "avi", "wmv", "m4v"),
        "spreadsheets": ("xlsx", "xls", "xlsm"),
        "docs": ("pdf", "docx", "txt", "pptx", "ppt", "doc", "tex"),
        "executable": ("exe", "py", "bin", "bat", "apk", "com", "msi", "jar"),
        "archives": ("rar", "zip", "iso", "7z", "pkg", "gz", "tar", "z", "bin"),
        "ebooks": ("epub", "mobi"),
        "misc": (),
        "backup": (),
    }
    dangerousPaths = (
        "/",
        ":\\",
        "/home",
        "/etc",
        "*:\\*\\*",
        "C:",
        "D:",
    )

    safePaths = (
        "/Downloads",
        "/Documents",
    )

if __name__ == "__main__":
    main()
