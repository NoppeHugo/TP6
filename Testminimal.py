import subprocess
destination = "google.com"
result = subprocess.run(["tracert", destination], capture_output=True, text=True)
print(result.stdout)
