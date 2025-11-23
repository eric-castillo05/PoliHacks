"""Small test helper to POST a WAV file to the /emotion endpoint.

Usage:
    python backend/test_emotion.py path/to/sample.wav

Make sure your backend is running (python backend/app.py) and the server is reachable at http://localhost:5001
"""
import sys
import requests

def main():
    if len(sys.argv) < 2:
        print("Usage: python backend/test_emotion.py path/to/sample.wav")
        sys.exit(2)
    wav_path = sys.argv[1]
    url = "http://localhost:5001/emotion"
    with open(wav_path, 'rb') as f:
        files = {'audio': ('sample.wav', f, 'audio/wav')}
        print(f"Posting {wav_path} to {url}...")
        r = requests.post(url, files=files, timeout=60)
        try:
            print('Status:', r.status_code)
            print(r.json())
        except Exception:
            print('Response:', r.text)

if __name__ == '__main__':
    main()
