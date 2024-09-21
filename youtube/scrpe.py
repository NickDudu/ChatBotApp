import polars as pl
from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript('CxwjfPIsvmI')
print(transcript)
output = ''
for x in transcript:
  sentence = x['text']
  output += f' {sentence}\n'
print(output)