import requests
import json

url = 'https://freetts.com/text-to-speech'
headers = {
    'Accept': 'text/x-component',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Next-Action': 'f6a37f3b9ffdb01ba2da16f264fdabab4a254f61',
    'Next-Router-State-Tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22(functions)%22%2C%7B%22children%22%3A%5B%22text-to-speech%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Ftext-to-speech%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
    'Origin': 'https://freetts.com',
    'Referer': 'https://freetts.com/text-to-speech',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

cookies = {
    '_ga': 'GA1.1.178648365.1735196411',
    '_ga_R18J4BQM3E': 'GS1.1.1735218037.2.1.1735218956.0.0.0',
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjE4MDQ0LCJ1c2VybmFtZSI6ImFrYXJzaHJhaTA1QGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiNTg2MjEzM0FDRjVDNUNGQUJBRUI3QUUxQUM4NkM4NjMiLCJpYXQiOjE3MzUyMTg5NTl9.jfePIWgBmJhAnFWP5G-qHPWbG3CLGPBvr-22KMfqomg',
    '__gads': 'ID=a782842f65aa4547:T=1735196416:RT=1735218960:S=ALNI_MZsm2VPYBZmOEiCEnBTLNCzh3CePw',
    '__gpi': 'UID=00000fb902ebda8b:T=1735196416:RT=1735218960:S=ALNI_MbsdkMWnXahgtCwFgK3bzXttxV22g',
    '__eoi': 'ID=35d861bb3580a812:T=1735196416:RT=1735218960:S=AA-AfjYWySUk_SiFTPIyT4PT_iUa',
    'FCNEC': '%5B%5B%22AKsRol8ERe3461fJ7AQWBuOqKHiVJDY-SCPpNQUyWIoyXVFltsOaCpc1BzZsMJE6aqlcJKU5ebljGVHtJ7LK6LHcMirt1OzaSDLM85B5xOlaWt8uU4VpCWKQLsy8V0a1cDgyKvtoMr3YYQYvx6qnOdZscwJian94Ng%3D%3D%22%5D%5D',
}
def tcy_op(tcy_text,output_file):
    body = f'''[
        {{
            "text": "{tcy_text}",
            "type": 0,
            "ssml": 0,
            "voiceType": "Standard",
            "languageCode": "kn-IN",
            "voiceName": "kn-IN-Standard-A",
            "gender": "FEMALE",
            "speed": "1.0",
            "pitch": "0",
            "volume": "0",
            "format": "mp3",
            "quality": 0,
            "isListenlingMode": 1,
            "displayName": "Anjali Mehta"
        }}
    ]'''

    response = requests.post(url, headers=headers, cookies=cookies, data=body)

    # print("Status Code:", response.status_code)
    # print("Response Headers:", response.headers)
    # print("Response Text:", response.text)

    response_lines = response.text.splitlines()
    data_line = response_lines[1].split(":", 1)[1]

    data = json.loads(data_line)
    audio_url = data["data"]["audiourl"]

    # print("Audio URL:", audio_url)

    audio_response = requests.get(audio_url)
    if audio_response.status_code == 200:
        with open(output_file, "wb") as file:
            file.write(audio_response.content)
        return 0
    else:
        return 1
