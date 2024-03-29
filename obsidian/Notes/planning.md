## Workflow (tentative and subject to change ofc)
* Implement voice recognition input for attorneys to verbalize notes at review/tagging time. Speech input is easier than written input, so why not?
* Transcribe spoken observations for compatibility with data science models and integration with key documents.
* Construct a detailed factual narrative from key documents, emphasized by transcribed attorney notes.
* Highlight critical elements in documents, guided by attorney insights, for focused narrative generation.
* Facilitate rapid creation of editable first drafts, streamlining the e-discovery process. 

**_The summary above was generated by a large language model using the transcription of my pitch in the Zoom meeting for the hackathon._**


#### Transcript from hackathon pitch
This text was transcribed from the audio of the pitch:

> I will admit that the title is a bit fuzzy, but that is intentional, because I still have to give it more thought myself. But essentially, this entire idea is predicated on the notion that speech input is easier than written input.
> I was imagining a user in the middle of their tagging or review process and maybe they can speak their observations of salient events, or salient facts, verbally, into a microphone. This input, obviously, will be transcribed, so that we can make it amenable to some of the components or models that the Data Science team already works with.
> So the hope is that when you have completed your tagging and you have your key documents at the end of it, you will also have a nice transcript of your attorney's observation notes to go with it. This is the first phase.
> For the next phase, we will create a factual narrative based on the key documents. And certain parts of these key documents will be put even more in focus, and emphasised by, by the transcriptions of the user's notes...or observations as I called it before. Because I anticipate that as a way to give your generation model some signal about what is the most critical part in your key document.  So ultimately, your factual narrative could be a statement of facts, deposition summaries, or memos along with the necessary citations to the documents that provide the evidence for those facts (and that is indeed the kind of thing we already do in GenSearch).
> And our user, with the help of this feature, should be able to quickly turn a blank page into a strong, editable, first draft with this factual narrative that we have generated. 
> And that's the long and short of it.


## Planning stuff

For the hackathon, a proof of concept of the AI capabilities will be great but if we can also give a POC of a path to production (e.g. containerization of Whisper and deployment as a Heroku app or something, idk), that would be a great sell.

We can decide the scope and complexity as we go based on how hard we find the project overall and how many people we end up taking on in the team.

* Figure out a way to record audio at 16 kHz and bit depth of 16. Preferred format is .wav.
* Check if ffmpeg works well with Python. This could also help with input conversion to the required format (above).
* Find if there is a way whisper can be built with Apple CoreML support. If Whisper's encoder can be executed on Apple Silicon for audio encoding speed up, we will get a big speedup.
* Should we run the Whisper transcription in a docker container? That way we can run it as a service in K8s. (Get Nick's advice on this later)
* Check if Gradio has microphone support. Will not matter if a UI person joins team, because we will probably write the frontend in React then. Not a React fan but a UI written in the same framework as R11 should make our work a stronger POC. Gradio can be our insurance plan.
* Run tests to compare quantized model with more parameters v/s unquantized model with fewer parameters. What is the performance v/s speed tradeoff?
* Live-streamed realtime transcriptions: The "realtime" part of this makes it extremely hard. Seems almost impossible but it would be INSANE if we can do it.
* For Karan: read [Whisper](https://cdn.openai.com/papers/whisper.pdf) paper properly.

## References
- [Whisper: Robust Speech Recognition via Large-Scale Weak Supervision](https://cdn.openai.com/papers/whisper.pdf)
