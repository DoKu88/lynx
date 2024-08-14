from moviepy.editor import VideoFileClip
import json
import assemblyai as aai
import os 

# Open the file
keys = None
with open('../data/keys.json', 'r') as f:
    # Load JSON data from file
    keys = json.load(f)

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
    key = speakerNameDict[utterance.speaker]
    if key not in dialogue:
      dialogue[key] = {"text": [utterance.text], "timestamps": [(utterance.start, utterance.end)]}
    else:
      dialogue[key]["text"].append(utterance.text)
      dialogue[key]["timestamps"].append((utterance.start, utterance.end))

  print("Dialogue extraction complete")
  return dialogue

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

videoFileNameSpeakers = "NoamChomsky_LexFridman"
videoDirectory = "../data/videoDownloads"
audioDirectory = "../data/audio"

videoFileName = os.path.join(videoDirectory, f"{videoFileNameSpeakers}.webm")
audioFileName = os.path.join(audioDirectory, f"{videoFileNameSpeakers}.wav")

print("videoFileName: ", videoFileName)
print("audioFileName: ", audioFileName)

videoToAudio(videoFileName, audioFileName, maxDuration=55)

speakerNames = videoFileNameSpeakers.split("_")
speakerNames.reverse()
speakerNameDict = {}
defaultSpeakerNames = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(len(speakerNames)):
  speakerNameDict[defaultSpeakerNames[i]] = speakerNames[i] 

dialogue = diatarizeDialogue(audioFileName, speakerNameDict)


for speaker in dialogue:
  print(f"Speaker: {speaker}")
  for i in range(len(dialogue[speaker]["text"])):
    print(f"Dialogue: {dialogue[speaker]['text'][i]}")
    print(f"Timestamps: {dialogue[speaker]['timestamps'][i]}")
    print("\n")

print("Done")