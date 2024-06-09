# visionGPT

This is a simple repository containing scripts that use the GPT-4 Vision API. I’ve made this repo to add scripts that you can use to explore the vision API for various tasks.

## main.py

The `main.py` script lets you:
a) Stream your laptop feed’s camera frames into the Vision API.
b) Prompt the model to perform/analyze actions happening in the frames.

### Notable Features

Some interesting changes done to allow real-time analysis of the video frames:
- We’re using the streaming mode of the API to allow for responses to be rendered in real-time.
- This lets us get the model response immediately instead of waiting for the whole response to be generated.
