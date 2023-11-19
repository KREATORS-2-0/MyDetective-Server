import socketio
import asyncio
import time
import threading
from emotion_webcam import FaceAnalyzer
from transcribe_emotion_fix import SpeechAnaylzer
from queue import Queue
from eeg.lie_analyzer import LieAnalyzer


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
    face_analyzer = FaceAnalyzer()
    speech_analyzer= SpeechAnaylzer()
    lie_analyzer = LieAnalyzer()
    

    def facialEmotion(analyzer):
        time.sleep(2)
        analyzer.run()

    def transcribeEmotion(analyzer):
        analyzer.transcribe()
        
    def lieAnalyzing(analyzer):
        analyzer.append_data(print_data=False)

    async def handle_threads():
        
        try:
            p1 = ControlledThread(facialEmotion, face_analyzer)
            p2 = ControlledThread(transcribeEmotion, speech_analyzer)
            p3 = ControlledThread(lieAnalyzing, lie_analyzer)
        
            p1.start()
            p2.start()
            p3.start()
            await running_event.wait()  # Wait until the event is set to stop
            
            p3.stop()
            p1.stop()
            p2.stop()
            # print("Speech Emotion Result:", speech_analyzer.classify_emotion())
            # print("Facial Emotion Result:", face_analyzer.data)
            temp = speech_analyzer.classify_emotion()
            eegTemp, eegTemp_confidence = lie_analyzer.analyze()
            # eegTemp = ""
            # eegTemp_confidence = 0
            result= {"transcript": speech_analyzer.transcription, "emotion": temp}
            result2= {"EEG": eegTemp, "EEG_confidence": eegTemp_confidence*100}
            print(face_analyzer.data)
            await sio.emit('command', {"faceData": face_analyzer.data, "speechData": result,"EEGData": result2 })
            speech_analyzer.reset_data()
        except KeyboardInterrupt:
            print("Program halted.")
            face_analyzer.stop_camera()
            lie_analyzer.stop_streaming()
      

    

    @sio.event
    async def connect():
        print('Connected to the server.')
        print('My SID is', sio.sid)
        passcode = input("type the passcode: ")
        await sio.emit('passcode', passcode)

    @sio.event
    async def disconnect():
        print('Disconnected from the server.')
        face_analyzer.stop_camera()
        lie_analyzer.stop_streaming()

    @sio.event
    async def connection(data):
        print('Connection established.', data)
        face_analyzer.start_camera()
        lie_analyzer.start_streaming()
        
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
