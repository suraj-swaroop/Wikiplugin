import os
import io
import sys
import gzip

# Checking a directory
def check_paht(inputPath):
    try:
        if not os.path.exists(inputPath):
            print("[Error] Clickstream file does not exist. Path:[{}]".format(inputPath))
            sys.exit(1)
        else:
            print("Found a file - Path:{}".format(inputPath))
    except OSError:
        print ("[Error] Checking the directory %s failed" % inputPath)
        sys.exit(1)
        
        
# Split the original clickstream file.
def main(pathFile, date):
    index = 0
    lines_per_file = 50000
    chunkfile = None
    with gzip.open(pathFile, "rb") as gzFile:
        for lineno, line in enumerate(gzFile):
            if lineno % lines_per_file == 0:
                if chunkfile:
                    chunkfile.close()
                index += 1
                strIndex = str(index)
                numStr = strIndex.zfill(4)
                chunk_filename = 'clickstream_{}_{}.txt'.format(date, numStr)
                chunk_path = "../download/clickstream/" + date + "/" + chunk_filename
                chunkfile = open(chunk_path, "wb")
            chunkfile.write(line)
        if chunkfile:
            chunkfile.close()

    gzFile.close()


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv[1]) != 6 :
        print("[Error] Invalid inputs")
        print("Example) 202001")
        sys.exit(1)

    date = sys.argv[1]
    fileName = "clickstream-enwiki-" + date[0:4] + "-" + date[4:6] + ".tsv.gz"
    pathfile = "../download/clickstream/" + date + "/" + fileName 
    
    check_paht(pathfile)
    main(pathfile, date)
       