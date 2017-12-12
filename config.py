# noinspection PyCompatibility
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
api_key = config['DEFAULT']['API_KEY']
home = config['DEFAULT']['HOME']
if __name__ == '__main__':
    config['DEFAULT'] = {'API_KEY': input('Enter the API KEY:'),
                         'HOME': input("Enter coordinates of home/location:")}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
