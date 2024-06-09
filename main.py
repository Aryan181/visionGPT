import cv2
import base64
import os
from queue import Queue
from threading import Thread
from openai import OpenAI



'''
Example prompts --> 
a) Counting fingers - Count the number of fingers the person is holding up. Just count and give me the count. Response should just be 1, 2, 6. All numbers. If no fingers just print 0. Just the count. Nothing else. Don't print or say anything else. 
b) Seeing what clothes a person is wearing - Tell me if the person is wearing a blue jacket. Respond with YES or NO. That's it. Nothing else. YES or NO
'''

# Set the API key and model name
MODEL = "gpt-4o"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<insert API key here >"))

def process_frame(frame):
    # Encode the frame as base64
    encoded_frame = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode('utf-8')

    # Send the frame to the model for processing
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "<Insert prompt from above>"},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f'data:image/jpg;base64,{encoded_frame}', "detail": "low"}}
            ]}
        ],
        temperature=0,
        stream=True
    )

    # Process the model's response
    for chunk in response:
        print(chunk.choices[0].delta.content)

# Open the default camera
video = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    success, frame = video.read()
    if not success:
        break

    # Process the frame in a separate thread
    processing_thread = Thread(target=process_frame, args=(frame,))
    processing_thread.daemon = True
    processing_thread.start()

    # Display the camera feed in a pop-up window
    cv2.imshow("Camera Feed", frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
video.release()
cv2.destroyAllWindows()