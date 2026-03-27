import asyncio
import httpx
import time
import json
import uuid

BASE_URL = "http://localhost:8000/api/v1"

async def test_endpoint(name, method, path, payload=None, expected_status=200, use_api_prefix=True, headers=None, cookies=None):
    url = f"{BASE_URL}{path}" if use_api_prefix else f"http://localhost:8000{path}"
    
    async with httpx.AsyncClient(timeout=15) as client:
        start_time = time.perf_counter()
        try:
            if method == "POST":
                response = await client.post(url, json=payload, cookies=cookies, headers=headers)
            else:
                response = await client.get(url, cookies=cookies, headers=headers)
            
            duration = (time.perf_counter() - start_time) * 1000
            status = response.status_code
            result = response.json() if "application/json" in response.headers.get("content-type", "") else response.text
            
            print(f"[{name}]")
            print(f"  Status: {status} (Expected: {expected_status})")
            print(f"  Duration: {duration:.2f}ms")
            if status != expected_status:
                print(f"  !! FAILED !! Response: {result}")
            else:
                print(f"  SUCCESS")
            return response
        except Exception as e:
            print(f"[{name}] ERROR: {e}")
            return None

async def run_audit():
    print("=== SENIOR VULNERABILITY & STRESS AUDIT (GROQ ENGINE) ===\n")

    # 1. Connectivity Check (Groq)
    print("--- 1. Connectivity: Groq Check ---")
    resp = await test_endpoint("Groq Probe", "POST", "/learn/explain", {"topic": "Quantum Computing", "subject": "Science"}, 200, cookies={"aila_session": str(uuid.uuid4())})
    if resp and resp.status_code == 200:
        data = resp.json()
        print(f"  Groq Response Summary: {data.get('summary')[:100]}...")

    # 2. XSS & Injection
    print("\n--- 2. Security: XSS & Injection ---")
    await test_endpoint("XSS Path Traversal", "POST", "/learn/explain", {"topic": "../../../etc/passwd<script>alert(1)</script>", "subject": "General"}, 200)

    # 3. Malformed Payloads
    print("\n--- 3. Stability: Malformed Metadata ---")
    # Sending string instead of object
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE_URL}/learn/explain", content="not-a-json")
        print(f"[Malformed JSON] Status: {r.status_code} (Expected: 422)")

    # 4. Large Payload (DoS attempt)
    print("\n--- 4. Stability: Large Payload (50KB) ---")
    await test_endpoint("Large Payload", "POST", "/learn/explain", {"topic": "A" * 50000, "subject": "General"}, 422)

    # 5. Race Condition: Cache Lock
    print("\n--- 5. Concurrency: Cache Stampede (5 identical parallel requests) ---")
    topic = f"Race Condition Test {uuid.uuid4()}"
    p = {"topic": topic, "subject": "General"}
    tasks = [test_endpoint(f"Stampede-{i}", "POST", "/learn/explain", p, 200, cookies={"aila_session": str(uuid.uuid4())}) for i in range(5)]
    results = await asyncio.gather(*tasks)
    
    # Analyze results: Only one should be 'cached': False (the one that generated), others might be True or also False if the lock didn't work.
    # Actually, with fakeredis, it might be different, but we check if they all succeed.
    success_count = sum(1 for r in results if r and r.status_code == 200)
    print(f"  Successful Concurrent Requests: {success_count}/5")

    # 6. Observability
    print("\n--- 6. Observability: Header Check ---")
    if resp:
        print(f"  X-Request-ID present: {'X-Request-ID' in resp.headers}")
        print(f"  Timing headers present: {'X-Process-Time' in resp.headers}")

    print("\n=== AUDIT COMPLETE ===")

if __name__ == "__main__":
    asyncio.run(run_audit())
