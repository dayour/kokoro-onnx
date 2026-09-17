---
title: Streaming and cancellation
---

`create_stream` yields `(audio, sample_rate)` chunks as batches finish. It is
not an audio-device driver and does not itself schedule playback.

```python
import asyncio
from contextlib import aclosing
from kokoro_onnx import Kokoro

async def main():
    tts = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    try:
        async with aclosing(tts.create_stream(
            "First sentence. A second sentence follows.",
            voice="af_heart",
        )) as stream:
            async for audio, sample_rate in stream:
                print(len(audio), sample_rate)
    finally:
        tts.voices.close()

asyncio.run(main())
```

The runtime performs inference in a background thread. Closing the generator
prevents subsequent batches; an already-running inference call finishes. Do not
promise immediate GPU cancellation or terminate an unrelated process to stop
one stream.

## Application responsibilities

Bound playback queues, retain the sample rate, and propagate producer exceptions.
Concatenate chunks in order for file output. Avoid adding a second layer of
punctuation padding unless it is intentional.

For long-form narration, evaluate latency, peak memory, and boundary quality
separately. A low real-time factor does not guarantee natural joins.
