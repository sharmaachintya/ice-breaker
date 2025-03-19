import pprint
import requests

pprint.pprint(requests.get("https://gist.githubusercontent.com/sharmaachintya/5b09e5d301c7b1cf094ffeffd5d98a59/raw/caeb534287eb7b3c8daa2b3d0f5ff4752bcf1e96/ice-breaker-scrapin.json").json())