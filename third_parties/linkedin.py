import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/ankurjaiswalofficial/376ee474e995abacd8f1ebd27ac23334/raw/6296029945013d3dfacc765a6e7931673a72c00a/ankur-jaiswal.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )
    else:
        PROXYCURL_API_KEY = os.environ["PROXYCURL_API_KEY"]

        headers = {'Authorization': 'Bearer ' + PROXYCURL_API_KEY}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'url': linkedin_profile_url,
        }
        response = requests.get(api_endpoint,
                                params=params,
                                headers=headers,
                                timeout=10
                                )
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for groups_dict in data.get("groups"):
            groups_dict.pop("profile_pic_url")
    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url='https://linkedin.com/in/ankurjaiswalofficial/',
            mock=True
        )
    )
