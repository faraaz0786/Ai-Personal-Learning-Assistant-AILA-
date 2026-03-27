import asyncio
import httpx
import time

BASE_URL = "http://localhost:8002/api/v1"

async def send_request(client, session_id, topic):
    headers = {"X-Session-ID": session_id}
    print(f"Sending request for topic: {topic}")
    start = time.perf_counter()
    resp = await client.post(
        f"{BASE_URL}/learn/explain",
        json={"topic": topic, "subject": "Technology"},
        headers=headers
    )
    latency = time.perf_counter() - start
    print(f"Status: {resp.status_code}, Latency: {latency:.2f}s")
    if resp.status_code == 422:
        print(f"Detail: {resp.text}")
    return resp

async def test_concurrency():
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Fire 5 concurrent requests for SAME topic but DIFFERENT sessions
        topic = "Quantum Computing Basics"
        print(f"\n--- Testing Concurrency for Topic: {topic} ---")
        
        async def session_wrapped_request():
            # Create unique session for each request
            s_resp = await client.post(f"{BASE_URL}/sessions")
            sid = s_resp.json()["id"]
            return await send_request(client, sid, topic)

        tasks = [session_wrapped_request() for _ in range(5)]
        responses = await asyncio.gather(*tasks)
        
        for r in responses:
            if r.status_code != 200 and r.status_code != 503: # 503 is expected if key invalid
                print(f"Unexpected status: {r.status_code}")

if __name__ == "__main__":
    asyncio.run(test_concurrency())
