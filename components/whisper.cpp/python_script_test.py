from pywhispercpp.model import Model

model = Model('base.en', n_threads=6)
segments = model.transcribe('file.mp3', speed_up=True)
for segment in segments:
    print(segment.text)