import os
import json

# Global Variable to use by other modules
# Open the file
keys = None
with open('../data/keys.json', 'r') as f:
    # Load JSON data from file
    keys = json.load(f)

# given a directory of video files, return a list of video file names
def getFileNames(directory, acceptedExtensions):
  fileNames = []
  for file in os.listdir(directory):
    if file.endswith(acceptedExtensions):
      fileNames.append(file)

  return fileNames


