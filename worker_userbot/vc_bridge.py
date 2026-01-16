import subprocess
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import RawAudioStream

class VCBridge:
    def __init__(self, app):
        self.calls = PyTgCalls(app)
        self.proc = None
        self.volume = 1.0

    def set_volume(self, vol):
        self.volume = max(0.1, min(vol, 3.0))
        print("Volume:", self.volume)

    async def start(self, chat_id):
        if self.proc:
            await self.stop()

        self.proc = subprocess.Popen(
            [
                "ffmpeg",
                "-f", "s16le",
                "-ar", "48000",
                "-ac", "2",
                "-i", "pipe:0",
                "-filter:a", f"volume={self.volume}",
                "-f", "s16le",
                "pipe:1",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        await self.calls.join_group_call(
            chat_id,
            RawAudioStream(self.proc.stdout, 48000, 2)
        )

        print("🔊 Joined VC:", chat_id)

    async def stop(self):
        if self.proc:
            self.proc.terminate()
            self.proc = None
        for call in self.calls.calls:
            await self.calls.leave_group_call(call)
        print("⛔ VC Left")
