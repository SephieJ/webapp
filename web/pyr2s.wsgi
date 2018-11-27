#!/data/vhosts/tirsolutions.com/web.r2s.tirsolutions.com/venv/bin/python
import sys, os

activate_this = '/data/vhosts/tirsolutions.com/web.r2s.tirsolutions.com/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert (0,'/data/vhosts/tirsolutions.com/web.r2s.tirsolutions.com')
os.chdir("/data/vhosts/tirsolutions.com/web.r2s.tirsolutions.com")

#sys.path.append('/data/vhosts/tirsolutions.com/web.r2s.tirsolutions.com')

from main import app as application
