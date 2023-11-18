import socketio
import asyncio
import time
import threading
from emotion_webcam import FaceAnalyzer
from transcribe_emotion_fix import SpeechAnaylzer
from queue import Queue


class ControlledThread:
    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.thread = None
        self.stop_event = threading.Event()

    def start(self):
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while not self.stop_event.is_set():
            self.target(*self.args, **self.kwargs)

    def stop(self):
        self.stop_event.set()
        self.thread.join()


async def client():
    sio = socketio.AsyncClient()
    running_event = asyncio.Event()

    def facialEmotion(analyzer):
        time.sleep(2)
        analyzer.run()

    def transcribeEmotion(analyzer):
        analyzer.transcribe()

    async def handle_threads():
        face_analyzer = FaceAnalyzer()
        speech_analyzer = SpeechAnaylzer()
        # speech_analyzer = SpeechAnalyzer()
        face_analyzer.start_camera()
        p1 = ControlledThread(facialEmotion, face_analyzer)
        p2 = ControlledThread(transcribeEmotion, speech_analyzer)
        p1.start()
        p2.start()

        await running_event.wait()  # Wait until the event is set to stop

        p1.stop()
        p2.stop()
        face_analyzer.stop_camera()
        print("Speech Emotion Result:", speech_analyzer.transcription)
        print("Facial Emotion Result:", face_analyzer.data)
        await sio.emit('command', face_analyzer.data)

    @sio.event
    async def connect():
        print('Connected to the server.')
        print('My SID is', sio.sid)
        passcode = input("type the passcode: ")
        await sio.emit('passcode', passcode)

    @sio.event
    async def disconnect():
        print('Disconnected from the server.')

    @sio.event
    async def connection(data):
        print('Connection established.', data)

    @sio.event
    async def command(data):
        if data == "Start":
            running_event.clear()
            asyncio.create_task(handle_threads())
        else:
            running_event.set()

    await sio.connect('http://ec2-15-223-56-147.ca-central-1.compute.amazonaws.com:8080')
    await sio.wait()
    await sio.disconnect()

asyncio.run(client())
