import logging
import os

import openai
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
from pathlib import Path
from model.candidate import Candidate
from model.position import Position
from model.stage import Stage
from logic.pdf_reader import PdfReader
from model.interviewer import Interviewer, InterviewerType
from logic import utils


class ResumeAI:
    OPENAI_API_KEY = "OPENAI_API_KEY"
    PROMPT = """
    Act as an HR expert providing services to the organization and its employees. Your tasks include supporting HR processes such as recruitment and onboarding, and providing advice to employees and managers. Your primary goal is to evaluate candidates based on their suitability for a given position.

    Tips Instructions:
    - Write all the information you can gather from the resume.
    - Write organizer with count numbers points for each question.
    - Write each subject in a two new lines.
    - Write each subject inside two stars, for example **item**.
    - Tell the candidate what they need to improve in their resume.
    - Suggest which positions they are more suitable for.
    - Provide advice on how to improve their resume.
    - Provide feedback on their experience and qualifications.
    - provide feedback on their education and experience.
    - Provide feedback on their skills and experience.
    - Provide feedback on that specific position.
    - If the tips contains many negative points, the score should be lower.
    - Summarize the candidate's resume in a few sentences.

    Scoring Instructions:
    - The score should range from 0 to 10.
    - A score of 0 indicates the candidate does not meet the basic requirements (e.g., incorrect degree or insufficient experience).
    - A score of 7 indicates the candidate meets all basic requirements.
    - Scores above 7 are for candidates who meet all basic requirements and also have desirable qualifications or experience. The maximum score of 10 is reserved for candidates who perfectly match both the required and preferred criteria.
    - If the tips contains many negative points, the score should be lower.
    - Be sure to consider the candidate's experience, education, and skills when assigning a score.
    - Consider the candidate's suitability for the position when assigning a score.
    - Consider the candidate's experience and qualifications when assigning a score.
    - Consider the candidate's skills and experience when assigning a score.
    - Be carefully with that score, it can be very important for the candidate.
    - 0 means the candidate is not suitable for the position.
    - 10 means the candidate is very suitable for the position.
    - 0 means the candidate can't hold that position and the colleges and etc doesn't know him in this area.
    - 10 means the candidate is very suitable for the position, did the candidate have all the requirements, and the experience needed, with the degree and the amount of years of experience.


    You should provide json format for the following questions:

    name: str - the name of the candidate
    linkdin_url: str - the linkdin url of the candidate (optional)
    email: str - the email of the candidate
    phone: str - the phone of the candidate
    city: str - the city of the candidate
    github: str - the github of the candidate (optional)
    bazz_words: list - list of the most important words in the resume, that can be used to search for the candidate in the future, for example programming languages, frameworks and etc.
    score: int - the score of the candidate (0-10) how much he is suitable for the position, if the candidate is not suitable for the position, or don't have enough experience, as asked, or the same degree or the amount of years of experience, the score should be 0.
                if the candidate is suitable for the position, the score should be between 1-10. and 10 means, the candidate is very suitable for the position, did the candidate have all the requirements, and the experience needed, with the degree and the amount of years of experience.
    summery: str - tips for the candidate how to improve his resume, What's to need to be done to get a higher score, 
                   or maybe which positions he is more suitable for, summery include all the relevant information for human HR and real human team leader.

    Format the output as JSON with the following keys:
    name
    linkdin_url
    email
    phone
    city
    summery
    bazz_words
    github
    score
    summery

    Position:
    {position}

    Candidate Resume:
    {resume}
    """

    def __init__(self, resume_pdf_path: Path, verbose: bool = False):
        self.pdf_converter = PdfReader(resume_pdf_path)
        self.candidate = resume_pdf_path
        self.llm_model = "gpt-4o"
        self.logger = utils.get_logger(logging.DEBUG if verbose else logging.INFO)
        self._init_openapi()
        self.interviewer = Interviewer(
            InterviewerType.AI,
            "hr_ai_model",
            "password",
            "HR AI Model",
            "General AI",
        )
        self.style = "American English in a calm and respectful tone, each title should be in a new line and bold."

    def _init_openapi(self):
        load_dotenv(find_dotenv())
        openai.api_key = os.getenv(self.OPENAI_API_KEY)

    def _get_completion(self, prompt: str, model: str):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(model=model, messages=messages, temperature=0, )
        return response.choices[0].message["content"]

    def _get_response_schema(self) -> list[ResponseSchema]:
        gift_schema = ResponseSchema(name="name", type="str", required=True,
                                     description="the name of the candidate")
        linkdin_url_schema = ResponseSchema(name="linkdin_url", type="str", required=False,
                                            description="the linkdin url of the candidate")
        email_schema = ResponseSchema(name="email", type="str", required=True,
                                      description="the email of the candidate")
        phone_schema = ResponseSchema(name="phone", type="str", required=True,
                                      description="the phone of the candidate, without dashs (minus sign), only numbers")
        city_schema = ResponseSchema(name="city", type="str", required=True,
                                     description="the city of the candidate")
        github_schema = ResponseSchema(name="github", type="str", required=False,
                                       description="the github of the candidate")
        score_schema = ResponseSchema(name="score", type="int", required=True,
                                      description="the score of the candidate (0-10) "
                                                  "how much he is suitable for the position")
        summery_scheme = ResponseSchema(name="summery", type="str", required=True,
                                     description="tips for the candidate how to improve his resume,"
                                                 "What's to need to be done to get a higher score, "
                                                 "or maybe which positions he is more suitable for, "
                                                 "summery include all the relevant information for human "
                                                 "HR and real human team leader.")
        bazz_words_schema = ResponseSchema(name="bazz_words", type="list", required=False,
                                     description="list of the most important words in the resume, that can be used to search for the candidate in the future, for example programming languages, frameworks and etc.")
        response_schemas = [
            gift_schema,
            linkdin_url_schema,
            email_schema,
            phone_schema,
            city_schema,
            github_schema,
            score_schema,
            summery_scheme,
            bazz_words_schema
        ]
        return response_schemas

    def summary(self) -> str:
        prompt = f"""
        Summary the candidate data base on his resume:
        what is the candidate's name?
        How many years of experience does the candidate have?
        where the candidate lives?
        what is the candidate's email?
        relevant experience to what kind of positions the candidate can apply?
        short summery about the candidate approximately 20 words?
        long summery about the candidate?
        Write it in a style of {self.style}

        candidate information:

        {self.pdf_converter.convert_to_text()}
        """
        return self._get_completion(prompt, self.llm_model)

    def compute(self, position: Position) -> Candidate:
        text_resume = self.pdf_converter.convert_to_text()
        response_schema = self._get_response_schema()
        output_parser = StructuredOutputParser.from_response_schemas(response_schema)
        format_instructions = output_parser.get_format_instructions()

        prompt_template = ChatPromptTemplate.from_template(template=ResumeAI.PROMPT)
        messages = prompt_template.format_messages(position=position.description, resume=text_resume)

        chat = ChatOpenAI(temperature=0.0, model=self.llm_model)
        response = chat(messages)
        output_dict = output_parser.parse(response.content)

        self.logger.debug(response)
        self.logger.debug(format_instructions)
        self.logger.debug(output_dict)

        stage = Stage(
            self.interviewer,
            output_dict["summery"],
            output_dict["score"],
            type="Entry Stage"
        )

        candidate = Candidate(
            output_dict["name"],
            output_dict["email"].lower(),
            output_dict["phone"],
            output_dict["city"],
            self.summary(),
            output_dict["bazz_words"],
            {position: [stage]},
            linkdin_url=output_dict.get("linkdin_url"),
            github_url=output_dict.get("github"),
        )

        return candidate
