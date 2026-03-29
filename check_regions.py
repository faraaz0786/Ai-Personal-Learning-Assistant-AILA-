import socket

project_ref = "eapmxlzuszoknkkoegmc"
regions = [
    "us-east-1", "us-east-2", "us-west-1", "us-west-2",
    "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3",
    "ap-south-1", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1"
]

print(f"Searching for pooler for {project_ref}...")

for region in regions:
    host = f"aws-0-{region}.pooler.supabase.com"
    try:
        # We check if it resolves. This doesn't guarantee the tenant is there,
        # but it confirms the regional pooler exists.
        addr = socket.getaddrinfo(host, 6543, family=socket.AF_INET)
        print(f"📍 Region {region:15} | IPv4 Found: {addr[0][4][0]}")
    except:
        pass
