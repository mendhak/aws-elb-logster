
import time
import geoip
from collections import defaultdict

from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException

class ELBLogster(LogsterParser):


    def country(self, ip, dbname='GeoIP.dat', cache=True, update=True):
        """Helper function that creates a GeoIP instance and calls country()."""
        g = None
        if cache: g = self.__geoip_cache.get(dbname)
        if g is None:
            if self.update_db:
                self.update_db(dbname=dbname)
            g = geoip.GeoIP(dbname)
            self.__geoip_cache[dbname] = g

        return g.country(ip)

    def update_db(self, src='http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz', dbname='GeoIP.dat', thresh=None):
        import os.path, datetime
        thresh = thresh or datetime.timedelta(days=7)
        try:
            mod_time = datetime.datetime.fromtimestamp(os.path.getctime(dbname))
        except OSError: mod_time = None
        cur_time = datetime.datetime.now()
        if not mod_time or cur_time-mod_time > thresh:
            import requests
            r = requests.get(src)
            data = r.content
            if src.endswith(".gz"):
                import gzip, StringIO #io.StringIO doesn't seem to do the job. StringIO.StringIO is legacy.
                s = StringIO.StringIO(data)
                data = gzip.GzipFile(fileobj=s).read()
            open(dbname, "wb").write(data)


    def __init__(self, option_string=None):

        self.__geoip_cache = {}

        '''Initialize any data structures or variables needed for keeping track
        of the tasty bits we find in the log we are parsing.'''
        self.sent_bytes = 0
        self.rcvd_bytes = 0
        self.countries = defaultdict(int)
        self.statuses  = defaultdict(int)
    
        
    def parse_line(self, line):
        '''This function should digest the contents of one line at a time, updating
        object's state variables. Takes a single argument, the line to be parsed.'''

        try:
            line_parts = line.split(' ')
            status = int(line_parts[7])

            self.sent_bytes += int(line_parts[10])
            self.rcvd_bytes += int(line_parts[9])
            country_code = self.country(line_parts[2].split(':')[0])

            self.countries[country_code] += 1
            self.statuses[status] += 1

        except Exception, e:
            print e
            raise LogsterParsingException, "regmatch or contents failed with %s" % e


    def get_state(self, duration):
        '''Run any necessary calculations on the data collected from the logs
        and return a list of metric objects.'''
        self.duration = duration

        # Return a list of metrics objects
        metric_objects = [
            MetricObject("bytes.sent", (self.sent_bytes), "Sent Bytes"),
            MetricObject("bytes.received", (self.rcvd_bytes), "Received Bytes"),
        ]

        for countrycode,countryhits in self.countries.items():
            metric_objects.append(MetricObject("country." + countrycode, countryhits, "Country hits"))

        for statuscode,statushits in self.statuses.items():
            metric_objects.append(MetricObject("http." + str(statuscode), statushits, "HTTP Status hits"))

        return metric_objects



