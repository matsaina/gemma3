import asyncio
import httpx
import time

URL = "http://127.0.0.1:8086/generate"
PROMPT = "Tell me a story about AI in Africa"
NUM_REQUESTS = 10  # number of concurrent requests

async def make_request(client, idx):
    start = time.time()
    try:
        response = await client.post(URL, json={"prompt": PROMPT, "max_tokens": 100})
        duration = time.time() - start
        print(f"Request {idx} completed in {duration:.2f}s")
        return duration
    except Exception as e:
        print(f"Request {idx} failed: {e}")
        return None

async def main():
    async with httpx.AsyncClient(timeout=120) as client:
        tasks = [make_request(client, i+1) for i in range(NUM_REQUESTS)]
        results = await asyncio.gather(*tasks)
    
    # Filter out failed requests
    durations = [r for r in results if r is not None]
    if durations:
        avg_time = sum(durations) / len(durations)
        print(f"\nAverage request time: {avg_time:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
