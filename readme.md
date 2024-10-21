# Exam Generator using GPT-3.5 and Streamlit

Welcome to the Exam Generator, a powerful tool that leverages the GPT-3.5 language model to create quizzes on any topic of your choice. This application is built using Python and Streamlit, making it easy to create, customize, and share quizzes with others.

If you're looking to explore a platform that offers this and much more, with a generous free trial, be sure to check out [EduGlowUp](https://eduglowup.com).

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Obtaining OpenAI API Keys](#obtaining-openai-api-keys)
- [Setting Secrets](#setting-secrets)
- [Executing the App](#executing-the-app)
- [Contributing](#contributing)
- [License](#license)

## Requirements

To use the Exam Generator, you need the following:

- Python 3.8 or higher
- An OpenAI API key to access GPT-3.5

## Installation

1. Clone the repository to your local machine:

```
git clone https://github.com/alexfdez1010/exam-generator.git
```

2. Change to the project directory:

```
cd exam-generator
```

3. Create a virtual environment and activate it:

```
python3 -m venv venv
source venv/bin/activate
```

Alternatively, you can use `conda` to create a virtual environment:

```
conda create -n exam-generator python=3.9
conda activate exam-generator
```

4. Install the required packages from `requirements.txt`:

```
pip install -r requirements.txt
```

## Obtaining OpenAI API Keys

To obtain the necessary API key and organization from OpenAI, follow these steps:

1. Go to the [OpenAI website](https://www.openai.com/).
2. If you don't have an account, click "Sign up" and create one.
3. Once logged in, navigate to the [API key management page](https://platform.openai.com/account/api-keys).
4. Click "Create new secret key" and note down the generated API key (you would not see the key again).
5. On the same page, find your organization ID under the "Settings" section.

You now have the API key and organization ID required for the Exam Generator.

## Setting Secrets

Create new directory `.streamlit` in the root directory of the project and create a new file `secrets.toml` inside it.

```
mkdir .streamlit
touch .streamlit/secrets.toml
```

Open the `secrets.toml` file and add the following lines:

```
OPENAI_TOKEN = <yout-token>
OPENAI_ORG = <your-org>
```

## Executing the App

After installing dependencies and setting secrets, execute the Exam Generator app by running:

```
streamlit run main.py
```

The Exam Generator app should now be accessible in your web browser at `http://localhost:8501`.

## Contributing

We welcome contributions to improve the Exam Generator. If you'd like to contribute, please fork the repository and create a pull request with your proposed changes. We'll review and merge the changes as appropriate.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
