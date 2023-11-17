import socketio
import asyncio


async def client():
    sio = socketio.AsyncClient()

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
        print('Command received.', data)

    await sio.connect('http://ec2-15-223-56-147.ca-central-1.compute.amazonaws.com:8080')
    await sio.wait()
    await sio.disconnect()

asyncio.run(client())
