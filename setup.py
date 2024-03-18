import setuptools

AUTHOR = 'Ruiqi-Alaina'
AUTHOR_EMAIL = 'alaina@gmail.com'
REPO_NAME = "AirPollution"
PROJECT_NAME = 'AirPollution'

setuptools.setup(
    name = PROJECT_NAME,
    version = '0.0.0',
    author = AUTHOR,
    author_email= AUTHOR_EMAIL,
    url=f'http://github.com/{AUTHOR}/{REPO_NAME}',
    packages = setuptools.find_packages(),
)