import ConfigParser
import pusher

config = ConfigParser.RawConfigParser()
config.read('env.cfg')

app_id = config.get('DevKey', 'DEV_APP_ID')
app_key = config.get('DevKey', 'DEV_APP_KEY')
secret = config.get('DevKey', 'DEV_SECRET')
cluster = config.get('DevKey', 'DEV_CLUSTER')
