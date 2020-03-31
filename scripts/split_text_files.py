import os
import io
import sys
import csv

# Checking a directory
def check_path(inputPath):
    try:
        if not os.path.exists(inputPath):
            print("[Error] Clickstream file does not exist. Path:[{}]".format(inputPath))
            sys.exit(1)
        else:
            print("Found a file - Path:{}".format(inputPath))
    except OSError:
        print ("[Error] Checking the directory %s failed" % inputPath)
        sys.exit(1)
        
def createPath(inputPath):
    try:
        if not os.path.exists(inputPath):
            print("[Warning] Created the path. Path:[{}]".format(inputPath))
            os.makedirs(inputPath)
    except OSError:
        print ("[Error] Creating the directory %s failed" % inputPath)
        sys.exit(1)
        
# Split the original text files.
def main(pathFile, date):
    index = 0
    lines_per_file = 50000
    chunkfile = None
    chunk_path = "./Outputs/text/" + date + "/"
    createPath(chunk_path)
    with open(pathFile, "r") as File:
        for lineno, line in enumerate(File):
            if lineno % lines_per_file == 0:
                if chunkfile:
                    chunkfile.close()
                index += 1
                strIndex = str(index)
                numStr = strIndex.zfill(4)
                chunk_filename = 'text_{}_{}.csv'.format(date, numStr)
                chunk_path = "../Outputs/text/" + date + "/" + chunk_filename
                chunkfile = open(chunk_path, "w")
            writer = csv.writer(chunkfile)
            writer.writerows(line)

    File.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("[Error] Invalid inputs")
        print("Example) 202001")
        sys.exit(1)

    pathfile = sys.argv[1]
    date = pathfile.split("-")[1]
    
    print("Path: {}, Date: {}".format(pathfile, date[0:6]))
    check_path(pathfile)
    
    main(pathfile, date[0:6])
    