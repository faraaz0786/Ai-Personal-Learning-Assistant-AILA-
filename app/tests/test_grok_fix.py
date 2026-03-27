import asyncio
import httpx
import sys

async def main():
    async with httpx.AsyncClient() as client:
        print("Creating session...")
        session_resp = await client.post("http://localhost:8000/api/v1/sessions")
        session_id = session_resp.cookies.get("session_id")
        print(f"Session ID: {session_id}")
        
        print("\nRequesting RAG explanation...")
        payload = {"topic": "Quantum Computing"}
        explain_resp = await client.post(
            "http://localhost:8000/api/v1/learn/explain",
            json=payload,
            cookies={"session_id": session_id},
            timeout=30.0
        )
        
        print(f"Status: {explain_resp.status_code}")
        print("Response JSON:")
        try:
            print(explain_resp.json())
        except Exception:
            print(explain_resp.text)

if __name__ == "__main__":
    asyncio.run(main())
