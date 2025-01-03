import sys

children = 10

child_requests = [list(map(int, sys.stdin.readline().strip().split())) for _ in range(children)]

print(child_requests)

x = {(k, i): f"{k}{i} "
     for k, child_request in enumerate(child_requests, start=1)
     for i in child_request}

print(x)