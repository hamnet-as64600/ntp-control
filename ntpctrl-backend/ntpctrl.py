#!/usr/bin/python3

### IMPORTS ###################################################################
import os
import sys
import json
import subprocess
import tornado.ioloop
import tornado.web

### GLOBALS ###################################################################

API_VERSION = "v0"
DEBUG = False

_SELFPATH_ = os.path.dirname(os.path.realpath(__file__))

TIME_CMD = 'date "+%F %T"'

GPS_DAEMON_CMD      = 'systemctl status gpsd.service'
GPS_CONF            = '/etc/default/gpsd'
GPS_SAMPLE_RAW_CMD  = 'gpspipe -r -n 50'
GPS_SAMPLE_JSON_CMD = 'gpspipe -r -n 50 | gpsdecode'

NTP_DAEMON_CMD = 'systemctl status ntp.service'
NTP_STAT_CMD   = 'ntpstat'
NTP_CONF       = '/etc/ntp.conf'
NTP_SOURCE_CMD = 'ntpq -np'

### REST ######################################################################

class time(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", "text/plain")
		proc = subprocess.Popen([TIME_CMD], shell=True, stdout=subprocess.PIPE)
		data, _ = proc.communicate()
		self.write( data.decode('utf-8') )


class gpsdDaemon(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", "text/plain")
		proc = subprocess.Popen([GPS_DAEMON_CMD], shell=True, stdout=subprocess.PIPE)
		data, _ = proc.communicate()
		self.write( data.decode('utf-8') )


class gpsdConfig(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", "text/plain")
		with open(GPS_CONF, 'r') as f:
			self.write(f.read())


class gpsdSampleRaw(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", "text/plain")
		proc = subprocess.Popen([GPS_SAMPLE_RAW_CMD], shell=True, stdout=subprocess.PIPE)
		data, _ = proc.communicate()
		self.write(data.decode('utf-8'))


class gpsdSampleJson(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", "application/json")
		proc = subprocess.Popen([GPS_SAMPLE_JSON_CMD], shell=True, stdout=subprocess.PIPE)
		data, _ = proc.communicate()
		data = data.decode('utf-8').splitlines()
		arr = []
		for elem in data:
			arr.append(json.loads(elem))
		self.write(json.dumps(arr, indent=4))


class ntpdDaemon(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", "text/plain")
		proc = subprocess.Popen([NTP_DAEMON_CMD], shell=True, stdout=subprocess.PIPE)
		data, _ = proc.communicate()
		self.write( data.decode('utf-8') )


class ntpdStatus(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", "text/plain")
		proc = subprocess.Popen([NTP_STAT_CMD], shell=True, stdout=subprocess.PIPE)
		data, _ = proc.communicate()
		self.write( data.decode('utf-8') )


class ntpdConfig(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", "text/plain")
		with open(NTP_CONF, 'r') as f:
			self.write(f.read())


class ntpdSources(tornado.web.RequestHandler):
	def get(self):
		self.set_header("Content-Type", "text/plain")
		proc = subprocess.Popen([NTP_SOURCE_CMD], shell=True, stdout=subprocess.PIPE)
		data, _ = proc.communicate()
		self.write( data.decode('utf-8') )


def make_app():
	return tornado.web.Application([
			(r"/time",             time),
			(r"/gpsd/daemon",      gpsdDaemon),
			(r"/gpsd/config",      gpsdConfig),
			(r"/gpsd/sample/raw",  gpsdSampleRaw),
			(r"/gpsd/sample/json", gpsdSampleJson),
			(r"/ntpd/daemon",      ntpdDaemon),
			(r"/ntpd/status",      ntpdStatus),
			(r"/ntpd/config",      ntpdConfig),
			(r"/ntpd/sources",     ntpdSources),
		])


### MAIN ######################################################################

if __name__ == "__main__":
	app = make_app()
	app.listen(8000)
	tornado.ioloop.IOLoop.current().start()
