
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_flow():
    session = requests.Session()
    
    print("1. Creating Session...")
    try:
        resp = session.post(f"{BASE_URL}/sessions/")
        resp.raise_for_status()
        session_data = resp.json()
        session_id = session_data['id']
        print(f"✅ Session Created: {session_id}")
        print(f"🍪 Session Cookies: {session.cookies.get_dict()}")
    except Exception as e:
        print(f"❌ Session Creation Failed: {e}")
        return

    print("\n2. Explaining Topic: 'Quantum Computing'...")
    try:
        resp = session.post(
            f"{BASE_URL}/learn/explain",
            json={"topic": "Quantum Computing", "session_id": session_id}
        )
        resp.raise_for_status()
        explanation = resp.json()
        print(f"✅ Explanation received: {explanation.get('summary')[:100]}...")
        topic_id = explanation.get('topic_id')
    except Exception as e:
        print(f"❌ Explanation Failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Response: {e.response.text}")
        return

    print("\n3. Generating Quiz...")
    try:
        resp = session.post(
            f"{BASE_URL}/learn/quiz",
            json={"topic_id": str(topic_id), "count": 3}
        )
        resp.raise_for_status()
        quiz = resp.json()
        print(f"✅ Quiz Generated with {len(quiz.get('questions', []))} questions.")
    except Exception as e:
        print(f"❌ Quiz Generation Failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Response: {e.response.text}")
        return

    print("\n✅ LOCAL FLOW VERIFIED!")

if __name__ == "__main__":
    test_flow()
