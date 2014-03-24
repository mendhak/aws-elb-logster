aws-elb-logster
===============

Logster module for AWS ELB logs. Extremely alpha, under development.

[Logster](https://github.com/etsy/logster) is a utility for reading log files and generating metrics in Graphite or Ganglia or Amazon CloudWatch. It comes with parsers for common log types such as Apache and Squid.  


###AWS ELB Logs

Amazon have introduced [access logs for Elastic Load Balancers](http://aws.typepad.com/aws/2014/03/access-logs-for-elastic-load-balancers.html). The log files are stored in an S3 bucket and their format is described in their documentation  [here](http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/access-log-collection.html). 


###Parser - ELBLogster.py

The `ELBLogster.py` parser will accept a line from an ELB access log and gather the following:

* HTTP status codes (200s, 300s, etc) - `http.200`, `http.206`, `http.304` ...
* Bytes Sent, Bytes Received - `bytes.sent`, `bytes.received`
* Country code (from IP address) - `country.IE`, `country.SG` ...
 

###IP to country code - geoip.py

`geoip.py` is a simple [wrapper](http://blog.brush.co.nz/2009/07/geoip/) around `GeoIP.dat` which in turn is a free downloadable database from [MaxMind](http://dev.maxmind.com/geoip/legacy/geolite/).  During a logster run, `ELBLogster.py` will download `GeoIP.dat` if it is stale, so that `geoip.py` can perform an IP to Country Code lookup. 

### Output

Current output when using `--output=graphite`, but this is subject to change.  

    graphiteserver:2003 eu-west-1.bytes.sent 633779898 1395667198
    graphiteserver:2003 eu-west-1.bytes.received 15582365 1395667198
    graphiteserver:2003 eu-west-1.country.KW 41 1395667198
    graphiteserver:2003 eu-west-1.country.SN 5 1395667198
    graphiteserver:2003 eu-west-1.country.SC 2 1395667198
    graphiteserver:2003 eu-west-1.country.SA 7 1395667198
    graphiteserver:2003 eu-west-1.country.MZ 6 1395667198
    graphiteserver:2003 eu-west-1.country.SG 2282 1395667198
    graphiteserver:2003 eu-west-1.country.SE 28 1395667198
    graphiteserver:2003 eu-west-1.country.AT 279 1395667198
    graphiteserver:2003 eu-west-1.http.200 31081 1395667198
    graphiteserver:2003 eu-west-1.http.206 27 1395667198
    graphiteserver:2003 eu-west-1.http.304 6975 1395667198
    graphiteserver:2003 eu-west-1.http.500 407 1395667198
    graphiteserver:2003 eu-west-1.http.302 503 1395667198
    graphiteserver:2003 eu-west-1.http.404 482 1395667198

### Usage

As with any other logster parser, place `ELBLogster.py` and `geoip.py` in your Python path, then run it

    sudo logster --metric-prefix=eu-west-1 --dry-run --output=graphite --graphite-host=graphiteserver:2003 ELBLogster ~/your-elb-log/2014-03-14.log 

I like to 'cheat' and place the files at the site packages for logster directly, for example `/usr/local/lib/python2.7/dist-packages/logster-0.0.1-py2.7.egg/logster/parsers/`

You may need to `pip install pytz requests` 

Remember that the AWS ELB logs are not contiguous - a new one is created every 5 or 60 minutes, so you must download and concatenate them yourself, then feed it to logster as shown above.  A simple example is shown in [this gist](https://gist.github.com/mendhak/9717352).

