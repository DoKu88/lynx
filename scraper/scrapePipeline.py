import generateTranscripts
import utils
from utils import keys
import videoAudioConverter
import youtubeScraper
import os

def main():

  videoDirectory = "../data/videoDownloads"
  audioDirectory = "../data/audio"

  # get the video metadata
  channel_videos = youtubeScraper.get_channel_videos('https://www.youtube.com/@lexfridman')
  video_metadata_lst = youtubeScraper.get_metadata_from_videos(channel_videos, 'lex_fridman')

  # download the videos
  # Need to parallelize 
  youtubeScraper.download_videos(video_metadata_lst[:3], videoDirectory)

  # convert the videos to audio
  # Need to parallelize
  videoAudioConverter.video_to_audio_directory(videoDirectory, audioDirectory, maxDuration=500)

  # diatarize the dialogue
  # Need to parallelize
  audioFileNames = utils.getFileNames(audioDirectory, acceptedExtensions=(".wav"))
  defaultSpeakerNames = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

  for fileName in audioFileNames:
      # main assumption is that the audio files will all be structured the same way
      audioFileNameSpeakers = fileName.split("_")
      videoId = audioFileNameSpeakers.pop().split(".")[0] # videoId is the last element in the list
    
      audioFileName = os.path.join(audioDirectory, fileName)

      print("audioFileName: ", audioFileName)
      print("videoFileNameSpeakers: ", audioFileNameSpeakers)
      print("videoId: ", videoId)

      speakerNameDict = {}
      for i in range(len(audioFileNameSpeakers)):
        speakerNameDict[defaultSpeakerNames[i]] = audioFileNameSpeakers[i] 

      # diatarize the dialogue
      dialogue = generateTranscripts.diatarizeDialogue(audioFileName, speakerNameDict)

      for speaker in dialogue:
        print(f"Speaker: {speaker}")
        for i in range(len(dialogue[speaker]["text"])):
          print(f"Dialogue: {dialogue[speaker]['text'][i]}")
          print(f"Timestamps: {dialogue[speaker]['timestamps'][i]}")
          print("\n")

      # Save the dialogue to a file

if __name__ == '__main__':
  main()



