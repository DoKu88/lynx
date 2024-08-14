from moviepy.editor import VideoFileClip
import os 
import utils
from utils import keys


# given a video file, extract the audio and save it to a file
def videoToAudio(videoFile, audioFileName, maxDuration=None):
  video = VideoFileClip(videoFile)

  subclip = None
  duration = video.duration

  if maxDuration is None:
    subclip = video.subclip(0, duration)
  else:
    subclip = video.subclip(0, min(maxDuration, duration))

  audio = subclip.audio

  # create audio file 
  with open(audioFileName, 'wb') as f:
    pass
  audio.write_audiofile(audioFileName)

if __name__ == '__main__':
  videoDirectory = "../data/videoDownloads"
  audioDirectory = "../data/audio"

  videoFileNames = utils.getFileNames(videoDirectory, acceptedExtensions=(".webm", ".mp4"))

  # can later do a map reduce to parallelize this
  for fileName in videoFileNames:
    # main assumption is that all video files will be structured the same way
    videoFileNameSpeakers = fileName.split("_")
    videoId = videoFileNameSpeakers.pop().split(".")[0] # videoId is the last element in the list
    audioFileName = fileName.split(".")[0] + ".wav"

    videoFileName = os.path.join(videoDirectory, fileName)
    audioFileName = os.path.join(audioDirectory, audioFileName)

    print("videoFileName: ", videoFileName)
    print("audioFileName: ", audioFileName)
    print("videoFileNameSpeakers: ", videoFileNameSpeakers)
    print("videoId: ", videoId)

    # convert video to audio
    videoToAudio(videoFileName, audioFileName, maxDuration=55)

  print("Done")