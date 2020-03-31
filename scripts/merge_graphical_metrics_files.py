import os, glob
import pandas as pd


# Checking a directory
def check_path(inputPath):
    try:
        if not os.path.exists(inputPath):
            print("[Warning] Create the path. Path:[{}]".format(inputPath))
            os.makedirs(inputPath)
    except OSError:
        print ("[Error] Checking the directory %s failed" % inputPath)
        sys.exit(1)
        

if __name__ == '__main__':
    path = "../Outputs/clickstream/"
    outFile = "merged_clickstream.csv"
    check_path(path)
    
    if os.path.exists(path + outFile):
        os.remove(path + outFile)

    # Merge all csv files in ./Outputs/clickstream/ directory
    all_files = glob.glob(os.path.join(path, "*.csv"))
    df_merged = pd.concat([pd.read_csv(f) for f in all_files ])
    df_merged.to_csv(path + "merged_clickstream.csv", mode='a', index=False, encoding='utf-8')
