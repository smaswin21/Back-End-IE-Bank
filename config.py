from dotenv import load_dotenv
import os
import urllib.parse
from azure.identity import DefaultAzureCredential

load_dotenv()

class Config(object):
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APPINSIGHTS_CONNECTION_STRING = os.getenv('APPINSIGHTS_CONNECTION_STRING')
    APPINSIGHTS_INSTRUMENTATIONKEY = os.getenv('APPINSIGHTS_INSTRUMENTATIONKEY')

class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///local.db'
    DEBUG = True

class GithubCIConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = True

class DevelopmentConfig(Config):
    if os.getenv('ENV') == 'dev':
        credential = DefaultAzureCredential()
        SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}?sslmode=require'.format(
            dbuser=urllib.parse.quote('b60ac699-813d-45f7-a8b6-4080578c9f29'),
            dbpass=credential.get_token('https://ossrdbms-aad.database.windows.net/.default').token,
            dbhost=os.getenv('DBHOST'),
            dbname=os.getenv('DBNAME')
        )
    DEBUG = True

class UATConfig(Config):
    if os.getenv('ENV') == 'uat':
        credential = DefaultAzureCredential()
        SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}?sslmode=require'.format(
            dbuser=urllib.parse.quote(os.getenv('DBUSER')),
            dbpass=credential.get_token('https://ossrdbms-aad.database.windows.net/.default').token,
            dbhost=os.getenv('DBHOST'),
            dbname=os.getenv('DBNAME')
        )
    DEBUG = True
