from setuptools import find_packages,setup

setup(
    name='interview_guide',
    version='0.0.1',
    author='Pratap Kumar',
    author_email='pratapmahatha9d@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)