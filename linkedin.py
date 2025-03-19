import os
import requests
from dotenv import load_dotenv

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    '''
    Scrape information from LinkedIn
    '''
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/sharmaachintya/5b09e5d301c7b1cf094ffeffd5d98a59/raw/caeb534287eb7b3c8daa2b3d0f5ff4752bcf1e96/ice-breaker-scrapin.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )

    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )

    data = response.json().get("person")
    if data is not None:
        data = {
            i: j
            for i, j in data.items()
            if j not in ([], "", None)
        }
    else:
        data = {}


    return data
    
if __name__ == "__main__":
    print(
        scrape_linkedin_profile(linkedin_profile_url = "https://www.linkedin.com/in/achintya-sharma-aa3a191b1/")
    )
