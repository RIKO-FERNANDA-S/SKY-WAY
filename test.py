# test_ws.py
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/api/v1/ws"
    try:
        async with websockets.connect(uri) as websocket:
            print(f"✅ Connected to {uri}")
            
            # Terima beberapa pesan telemetry
            for i in range(5):
                message = await websocket.recv()
                data = json.loads(message)
                print(f"📡 Received: {json.dumps(data, indent=2)}")
                
            # Kirim pesan ke server
            await websocket.send("Hello from test client!")
            response = await websocket.recv()
            print(f"📨 Server response: {response}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())