from abc import abstractmethod
from typing import Optional

import streamlit as st

from model.question import Question
from utils.api import get_questions, clarify_question
from utils.generate_document import questions_to_pdf


class PageEnum:
    """
    Enum for pages
    """
    GENERATE_EXAM = 0
    QUESTIONS = 1
    RESULTS = 2


class Page:

    @abstractmethod
    def render(self, app):
        """
        Render the page (must be implemented by subclasses)
        """


class GenerateExamPage(Page):

    description = """
    This app generates exams with questions and answers, powered by GPT-3.5 (a.k.a. ChatGPT), 
    and can generate questions and answers on any topic. You can download the questions as a 
    PDF file or take the exam within the app. However, the quality of the generated questions 
    and answers may vary depending on the topic. If you are unsure about the accuracy of any of 
    the questions, you can request clarifications from the AI in the results page. In most cases, 
    the AI will be able to rectify any mistakes. However, if you are still unsure, it is recommended 
    that you search for the topic on the internet or ask an expert.

    The app is intended for learning purposes only, to help students practice and test their knowledge 
    with immediate feedback. It is not intended to generate exams for real-world applications. Please 
    note that the app is not responsible for any damage caused by its use.
    """

    def render(self, app):
        """
        Render the page
        """
        st.title("Generate exam")

        st.markdown(self.description)

        topics = st.text_input(
            "Topics",
            placeholder="Topics to include in the exam",
            help="It is recommended to use a comma-separated list of topics"
        )

        number_of_questions = st.number_input(
            "Number of questions",
            min_value=5,
            max_value=30,
            value=10,
            help="Number of questions that will be generated"
        )

        number_of_answers = st.number_input(
            "Number of answers",
            min_value=3,
            max_value=5,
            value=4,
            help="Number of possible answers that will be generated for each question"
        )

        if st.button("Generate", help="Generate the questions according to the parameters"):

            st.warning("Generating questions. This may take a while...")
            try:
                app.questions = get_questions(topics, number_of_questions, number_of_answers)
            except Exception:
                st.error("An error occurred while generating the questions. Please try again")

        if app.questions is not None:

            st.info(
                f"An exam with {len(app.questions)} questions has been generated. You "
                f"can download the questions as a PDF file or take the exam in the app."
            )

            left, center, right = st.columns(3)

            with left:

                questions_to_pdf(app.questions, "questions.pdf")
                st.download_button(
                    "Download",
                    data=open("questions.pdf", "rb").read(),
                    file_name="questions.pdf",
                    mime="application/pdf",
                    help="Download the questions as a PDF file"
                )

            with right:
                if st.button("Start exam", help="Start the exam"):
                    app.change_page(PageEnum.QUESTIONS)


class QuestionsPage(Page):

    def __init__(self):
        self.number_of_question = 0

    def render(self, app):
        """
        Render the page
        """
        st.title("Questions")

        question = app.questions[self.number_of_question]

        answer = self.__render_question(question, app.get_answer(self.number_of_question))

        app.add_answer(self.number_of_question, answer)

        left, center, right = st.columns(3)

        if self.number_of_question != 0:
            with left:
                if st.button("Previous", help="Go to the previous question"):
                    self.__change_question(self.number_of_question - 1)

        with center:
            if st.button("Finish", help="Finish the exam and go to the results page"):
                app.change_page(PageEnum.RESULTS)

        if self.number_of_question != len(app.questions) - 1:
            with right:
                if st.button("Next", help="Go to the next question"):
                    self.__change_question(self.number_of_question + 1)

    @staticmethod
    def __render_question(question: Question, index_answer: Optional[int]) -> int:
        """
        Render a question and return the index of the answer selected by the user
        :param question: Question to render
        :param index_answer: Index of the answer selected by the user (if any)
        :return: Index of answer selected by the user
        """
        if index_answer is None:
            index_answer = 0

        st.write(f"**{question.id}. {question.question}**")
        answer = st.radio("Answer", question.answers, index=index_answer)

        index = question.answers.index(answer)

        return index

    def __change_question(self, index: int):
        """
        Change the current question and rerun the app
        :param index: Index of the question to change to
        """
        self.number_of_question = index
        st.experimental_rerun()


class ResultsPage:

    def __init__(self):
        self.clarifications = {}

    def render(self, app):
        """
        Render the page
        """
        st.title("Results")

        num_correct = self.__get_correct_answers(app)

        st.write(f"### Number of questions: {len(app.questions)}")
        st.write(f"### Number of correct answers: {num_correct}")
        st.write(f"### Percentage of correct answers: {num_correct / len(app.questions) * 100:.2f}%")

        for index, question in enumerate(app.questions):
            self.__render_question(question, app.get_answer(index))

        left, right = st.columns(2)

        with left:

            if st.button("Generate new exam"):
                app.reset()
                app.change_page(PageEnum.GENERATE_EXAM)

        with right:

            questions_to_pdf(app.questions, "questions.pdf")
            st.download_button(
                "Download",
                data=open("questions.pdf", "rb").read(),
                file_name="questions.pdf",
                mime="application/pdf",
                help="Download the questions as a PDF file"
            )

    def __render_question(self, question: Question, user_answer: int):
        """
        Render a question with the correct answer
        :param question: Question to render
        :param user_answer: Index of the answer selected by the user
        """
        st.write(f"**{question.id}. {question.question}**")

        if question.correct_answer == user_answer:
            for index, answer in enumerate(question.answers):
                if index == user_answer:
                    st.write(f":green[{chr(ord('a') + index)}) {answer}]")
                else:
                    st.write(f"{chr(ord('a') + index)}) {answer}")

        else:
            for index, answer in enumerate(question.answers):
                if index == user_answer:
                    st.write(f":red[{chr(ord('a') + index)}) {answer}]")
                elif index == question.correct_answer:
                    st.write(f":green[{chr(ord('a') + index)}) {answer}]")
                else:
                    st.write(f"{chr(ord('a') + index)}) {answer}")

        clarify_button = st.button(
            "Clarify the question",
            help="Get more information about the question",
            key=f"clarify_question_{question.id}"
        )

        if not clarify_button:
            return

        if question.id not in self.clarifications:
            st.warning("This can take a while...")
            self.clarifications[question.id] = clarify_question(question)

        st.write(self.clarifications[question.id])

    @staticmethod
    def __get_correct_answers(app):
        """
        Get the number of correct answers
        :param app: App instance
        :return: Number of correct answers
        """
        correct_answers = 0
        for index, question in enumerate(app.questions):
            if question.correct_answer == app.get_answer(index):
                correct_answers += 1

        return correct_answers
