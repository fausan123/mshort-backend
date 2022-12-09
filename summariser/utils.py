import requests
from decouple import config

errors = list()
def read_file(filename, chunk_size=5242880):
     with open(filename, 'rb') as _file:
         while True:
             data = _file.read(chunk_size)
             if not data:
                 break
             yield data

def assemblyai_transcript(filename):
  headers = {'authorization': config('AAI_KEY')}
  t_headers = {'authorization': config('AAI_KEY'), 'content-type': "application/json"}
  
  response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(filename))
  
  upload_url = response.json()['upload_url']
  response = requests.post("https://api.assemblyai.com/v2/transcript", 
                           json={"audio_url": upload_url}, headers=t_headers)

  transcript_id = response.json()['id']

  return transcript_id

def get_aaitranscript(id):
  headers = {'authorization': config('AAI_KEY')}
  response = requests.get(f"https://api.assemblyai.com/v2/transcript/{id}", headers=headers)

  status = response.json()['status']
  while (status != 'completed'):
    if (status == 'error'):
      errors.append(response)
      return "Error Occurred !!" 
    response = requests.get(f"https://api.assemblyai.com/v2/transcript/{id}", headers=headers)
    status = response.json()['status']

  return response.json()['text']