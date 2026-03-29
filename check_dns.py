import socket

def test_host(host):
    print(f"Testing {host}...")
    try:
        # AF_INET for IPv4
        addr = socket.getaddrinfo(host, 5432, family=socket.AF_INET)
        print(f"  ✅ IPv4 Found: {addr[0][4][0]}")
    except Exception as e:
        print(f"  ❌ No IPv4: {e}")

project_id = "eapmxlzuszoknkkoegmc"
hosts = [
    f"db.{project_id}.supabase.co",
    f"db.{project_id}.supabase.com",
    f"{project_id}.supabase.co",
    f"{project_id}.supabase.com",
    "aws-0-ap-south-1.pooler.supabase.com",
]

for h in hosts:
    test_host(h)
