import unittest
from pathlib import PurePosixPath
import requests_mock

from logic.linkdin_api import get_linkedin_job_details, LinkedInJobDetailError
from model.position import Position


class TestLinkedinJobDetails(unittest.TestCase):

    @requests_mock.Mocker()
    def test_get_linkedin_job_details_basic(self, mock):
        url = "https://www.linkedin.com/jobs/view/test-job-id/"

        mock_html = '''
        <html>
            <body>
                <h1 class="topcard__title">Software Engineer</h1>
                <a class="topcard__org-name-link">Tech Company</a>
                <span class="topcard__flavor topcard__flavor--bullet">San Francisco, CA</span>
                <div class="description__text description__text--rich">Job description text here.</div>
            </body>
        </html>
        '''
        mock.get(url, text=mock_html)

        expected_position = Position(
            linkdin_url=PurePosixPath(url),
            name='Software Engineer',
            open_by='',
            company='Tech Company',
            location='San Francisco, CA',
            description='Job description text here.'
        )

        result = get_linkedin_job_details(url)
        self.assertEqual(result, expected_position)

    @requests_mock.Mocker()
    def test_get_linkedin_job_details_no_description(self, mock):
        url = "https://www.linkedin.com/jobs/view/test-job-id/"

        mock_html = '''
        <html>
            <body>
                <h1 class="topcard__title">Software Engineer</h1>
                <a class="topcard__org-name-link">Tech Company</a>
                <span class="topcard__flavor topcard__flavor--bullet">San Francisco, CA</span>
                <!-- No description provided -->
            </body>
        </html>
        '''
        mock.get(url, text=mock_html)

        with self.assertRaises(LinkedInJobDetailError):
            get_linkedin_job_details(url)

    @requests_mock.Mocker()
    def test_get_linkedin_job_details_missing_company(self, mock):
        url = "https://www.linkedin.com/jobs/view/test-job-id/"

        mock_html = '''
        <html>
            <body>
                <h1 class="topcard__title">Software Engineer</h1>
                <!-- No company name provided -->
                <span class="topcard__flavor topcard__flavor--bullet">San Francisco, CA</span>
                <div class="description__text description__text--rich">Job description text here.</div>
            </body>
        </html>
        '''
        mock.get(url, text=mock_html)

        with self.assertRaises(LinkedInJobDetailError):
            get_linkedin_job_details(url)

    @requests_mock.Mocker()
    def test_get_linkedin_job_details_missing_title(self, mock):
        url = "https://www.linkedin.com/jobs/view/test-job-id/"

        mock_html = '''
        <html>
            <body>
                <!-- No title provided -->
                <a class="topcard__org-name-link">Tech Company</a>
                <span class="topcard__flavor topcard__flavor--bullet">San Francisco, CA</span>
                <div class="description__text description__text--rich">Job description text here.</div>
            </body>
        </html>
        '''
        mock.get(url, text=mock_html)

        with self.assertRaises(LinkedInJobDetailError):
            get_linkedin_job_details(url)

    @requests_mock.Mocker()
    def test_get_linkedin_job_details_missing_location(self, mock):
        url = "https://www.linkedin.com/jobs/view/test-job-id/"

        mock_html = '''
        <html>
            <body>
                <h1 class="topcard__title">Software Engineer</h1>
                <a class="topcard__org-name-link">Tech Company</a>
                <!-- No location provided -->
                <div class="description__text description__text--rich">Job description text here.</div>
            </body>
        </html>
        '''
        mock.get(url, text=mock_html)

        with self.assertRaises(LinkedInJobDetailError):
            get_linkedin_job_details(url)

    @requests_mock.Mocker()
    def test_get_linkedin_job_details_nonexistent_url(self, mock):
        url = "https://www.linkedin.com/jobs/view/nonexistent-job-id/"

        mock.get(url, status_code=404)

        with self.assertRaises(LinkedInJobDetailError):
            get_linkedin_job_details(url)


if __name__ == '__main__':
    unittest.main()
