from moviepy.editor import VideoFileClip
import json
import assemblyai as aai
import os 
import utils
from utils import keys

# given an audio file return the diarized dialogue
# in the form of a dictionary with the speaker as the key
# and the value as a list of dialogue snippets and timestamps
def diatarizeDialogue(audioFileName, speakerNameDict):
  # diatarize the audio file
  aai.settings.api_key = keys["api_keys"]["assemblyai"]["api_key"]
  config = aai.TranscriptionConfig(speaker_labels=True)
  transcriber = aai.Transcriber()

  print("Transcribing audio file..")
  transcript = transcriber.transcribe(audioFileName, config=config)
  print("Transcription complete")

  # extract the diaglogue from the transcript & store in dictionary
  dialogue = {}

  print("Extracting dialogue from transcript..")
  for utterance in transcript.utterances:

    if utterance.speaker not in speakerNameDict:
      import pdb; pdb.set_trace()
      print("Speaker not in speakerNameDict")
      print("Speaker: ", utterance.speaker)
      print("utterance: ", utterance.text)
      print("timestamps: ", utterance.start, " ", utterance.end)
      continue 

    key = speakerNameDict[utterance.speaker]
    if key not in dialogue:
      dialogue[key] = {"text": [utterance.text], "timestamps": [(utterance.start, utterance.end)]}
    else:
      dialogue[key]["text"].append(utterance.text)
      dialogue[key]["timestamps"].append((utterance.start, utterance.end))

  print("Dialogue extraction complete")
  return dialogue

'''
Right now, we just assume that Led Fridman talks first and then the guest.
However, for other podcasts this is not the case. 
Need to add a check to see if the first speaker is the host or the guest from the transcript. 
This will allow us to generalize this function to other podcasts as well.

For now, let's just assume we're doing Lex Fridman podcasts
'''

if __name__ == '__main__':
  audioDirectory = "../data/audio"
  defaultSpeakerNames = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

  audioFileNames = utils.getFileNames(audioDirectory, acceptedExtensions=(".wav"))

  # can later do a map reduce to parallelize this
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
    dialogue = diatarizeDialogue(audioFileName, speakerNameDict)

    for speaker in dialogue:
      print(f"Speaker: {speaker}")
      for i in range(len(dialogue[speaker]["text"])):
        print(f"Dialogue: {dialogue[speaker]['text'][i]}")
        print(f"Timestamps: {dialogue[speaker]['timestamps'][i]}")
        print("\n")

    # Save the dialogue to a file

  print("Done")