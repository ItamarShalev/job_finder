from pathlib import PurePosixPath
import requests
from bs4 import BeautifulSoup
from model.position import Position


class LinkedInJobDetailError(RuntimeError):
    pass


def get_linkedin_job_details(url):
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise LinkedInJobDetailError("Failed to retrieve the webpage.")

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1', {'class': 'topcard__title'})
    if not title:
        raise LinkedInJobDetailError("Job title is missing.")
    title = title.get_text(strip=True)

    company = soup.find('a', {'class': 'topcard__org-name-link'})
    if not company:
        raise LinkedInJobDetailError("Company name is missing.")
    company = company.get_text(strip=True)

    location = soup.find('span', {'class': 'topcard__flavor topcard__flavor--bullet'})
    if not location:
        raise LinkedInJobDetailError("Job location is missing.")
    location = location.get_text(strip=True)

    description = soup.find('div', {'class': 'description__text description__text--rich'})
    if not description:
        raise LinkedInJobDetailError("Job description is missing.")
    description = description.get_text(strip=True)

    position = Position(
        linkdin_url=PurePosixPath(url),
        name=title,
        open_by="",
        company=company,
        location=location,
        description=description
    )

    return position
