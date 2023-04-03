import streamlit as st

from app.page import GenerateExamPage, PageEnum, QuestionsPage, ResultsPage


@st.cache_resource(ttl=60 * 60 * 24)
def get_app():
    """
    Create a new app instance if it doesn't exist yet
    :return: App instance
    """
    return App()


class App:
    """
    App class that models all the app functionality
    """

    def __init__(self):
        self.pages = {
            PageEnum.GENERATE_EXAM: GenerateExamPage(),
            PageEnum.QUESTIONS: QuestionsPage(),
            PageEnum.RESULTS: ResultsPage()
        }

        self.current_page = self.pages[PageEnum.GENERATE_EXAM]

        self._questions = None
        self._answers = {}

    def render(self):
        """
        Render the app
        """
        self.current_page.render(self)

    @property
    def questions(self):
        return self._questions

    @questions.setter
    def questions(self, value):
        self._questions = value

    def add_answer(self, question_index: int, answer_index: int):
        """
        Add an answer to the answers dictionary
        :param question_index: index of the question
        :param answer_index: index of the answer
        """
        self._answers[question_index] = answer_index

    def get_answer(self, question_index: int):
        """
        Get the answer for a question
        :param question_index: index of the question
        :return: index of the answer if it exists, None otherwise
        """
        return self._answers.get(question_index, None)

    def change_page(self, page: PageEnum):
        """
        Change the current page and rerun the app
        :param page: Page to change to
        """
        self.current_page = self.pages[page]
        st.experimental_rerun()

    def reset(self):
        """
        Reset the app
        """
        self._questions = None
        self._answers = {}
        self.pages[PageEnum.QUESTIONS].number_of_question = 0
        self.pages[PageEnum.RESULTS].clarifications = {}
        self.current_page = self.pages[PageEnum.GENERATE_EXAM]

        st.experimental_rerun()
