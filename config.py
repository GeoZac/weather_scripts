import configparser

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['DEFAULT']['API_KEY']
home = (config['DEFAULT']['HOME'])
