from pyannote.audio import Pipeline
from moviepy.editor import VideoFileClip
import json
import pickle
import assemblyai as aai

# Open the file
keys = None
with open('../data/keys.json', 'r') as f:
    # Load JSON data from file
    keys = json.load(f)

def tryAssemblyAI(audioFileName):
  aai.settings.api_key = keys["api_keys"]["assemblyai"]["api_key"]
  config = aai.TranscriptionConfig(speaker_labels=True)
  transcriber = aai.Transcriber()

  transcript = transcriber.transcribe(audioFileName, config=config)

  for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=keys["api_keys"]["huggingface"])

# send pipeline to GPU (when available)
import torch
#pipeline.to(torch.device("cuda"))

# Load the video file 
videoFile = "../data/videoDownloads/NoamChomsky_LexFridman.webm"
video = VideoFileClip(videoFile)

duration = video.duration
subclip = video.subclip(0, 55)

audio = subclip.audio
audio.write_audiofile("../data/audio.wav")

tryAssemblyAI("../data/audio.wav")

exit()
# apply pretrained pipeline
diarization = pipeline("../data/audio.wav")

transcriptFile = "../data/transcripts/NoamChomsky.pkl"
# Open the file in write-binary mode and pickle the object
with open(transcriptFile, 'wb') as file:
    pickle.dump(diarization, file)

# print the result
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
# start=0.2s stop=1.5s speaker_0
# start=1.8s stop=3.9s speaker_1
# start=4.2s stop=5.7s speaker_0
# ...