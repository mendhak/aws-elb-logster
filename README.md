aws-elb-logster
===============

Logster module for AWS ELB logs. Extremely alpha, under development.


###AWS ELB Logs

Amazon have introduced [access logs for Elastic Load Balancers](http://aws.typepad.com/aws/2014/03/access-logs-for-elastic-load-balancers.html). The log files are stored in an S3 bucket during configuration and their format is atypical.  You can find documentation on the file format [here](http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/access-log-collection.html). 

###ELBLogster.py

The `ELBLogster.py` parser will accept a line from an ELB access log and gather the following:

* HTTP status codes (200s, 300s, etc)
* Bytes Sent, Bytes Received
* Country code (from IP address)
 

###geoip.py

`geoip.py` is a simple [wrapper](http://blog.brush.co.nz/2009/07/geoip/) around `GeoIP.dat` which in turn is a free downloadable database from [MaxMind](http://dev.maxmind.com/geoip/legacy/geolite/).  `ELBLogster.py` will download `GeoIP.dat` if it is stale, so that `geoip.py` can perform an IP to Country Code lookup. 

### Output

Current output when using `--output=graphite`, but this is subject to change

    127.0.0.1:8135 http_1xx 0.0 1395537387
    127.0.0.1:8135 http_2xx 1470.71428571 1395537387
    127.0.0.1:8135 http_3xx 396.857142857 1395537387
    127.0.0.1:8135 http_4xx 14.0 1395537387
    127.0.0.1:8135 http_5xx 14.7142857143 1395537387
    127.0.0.1:8135 sent_bytes 109896399 1395537387
    127.0.0.1:8135 rcvd_bytes 2145653 1395537387
    127.0.0.1:8135 country.BE 2 1395537387
    127.0.0.1:8135 country.FR 862 1395537387
    127.0.0.1:8135 country.BG 1 1395537387
    127.0.0.1:8135 country.DE 1370 1395537387
    127.0.0.1:8135 country.BH 2 1395537387
    127.0.0.1:8135 country.HU 1 1395537387
    127.0.0.1:8135 country.BR 1 1395537387
    127.0.0.1:8135 country.FI 8 1395537387
