#!/usr/bin/env python
# coding=utf-8
import webapp2
import logging
import urllib
import time
import sys
from google.appengine.api import mail
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.runtime import apiproxy_errors
def urlfetch_QQ_isExsit(url):
    try:
        deadline=10
        response = urlfetch.fetch(url, method='GET',payload=None, headers={}, allow_truncated=False,follow_redirects=False, deadline=10)
        #self.response.out.write(response.content)
    except apiproxy_errors.OverQuotaError as e:
        logging.error('OverQuotaError(deadline=%s, url=%r)', deadline, url)
        time.sleep(5)
    except urlfetch.DeadlineExceededError as e:
        logging.error('DeadlineExceededError(deadline=%s, url=%r)', deadline, url)
        time.sleep(1)
    except urlfetch.DownloadError as e:
        logging.error('DownloadError(deadline=%s, url=%r)', deadline, url)
    except urlfetch.ResponseTooLargeError as e:
        logging.error('ResponseTooLargeError(deadline=%s, url=%r) response(%r)', deadline, url, response)
    except Exception as e:
        logging.error('%s(deadline=%s, url=%r)',str(e), deadline, url)
    else:
        return response.content
def gae_sendmail(toadress):
    message = mail.EmailMessage(sender='<goagent.helloworld@gmail.com>',
                            subject=unicode('使用GoAgent看YouTube视频,上BBC学英语','utf8'))

    message.to = toadress
    message.body = ''
    fd = open('goagent.html', 'rb')
    message.html = fd.read()
    fd.close()

    message.attachments =  [('goagenthome.jpg',db.Blob(open("goagenthome.jpg", "rb").read())),
                            ('IE_set.jpg',db.Blob(open("IE_set.jpg", "rb").read())),
                            ('ie_con_proxy.jpg',db.Blob(open("ie_con_proxy.jpg", "rb").read())),
                            ('proxy_set.jpg',db.Blob(open("proxy_set.jpg", "rb").read()))]
    try:
        message.send()
    except Exception as e:
        logging.error('Mail sent fail by gae,please check code.')
        return False
    else:
        logging.info('Congratulations!Mail have been sent successfully by gae.')
        #self.response.out.write('Congratulations!Mail have been sent successfully by gae.')
        return True
"""
class Queryed(db.Model):
  previous_response = db.StringProperty()

def NeedToSendMail(response):
    # check if we need to sendmail,maybe we have sent to the same addr before
    Queryeds = db.Query(Queryed)
    previous_response = Queryeds.get()
    if previous_response == None:
        logging.warning("No result queried,maybe it's the first time to query.")
        previous_response = Queryed()
        previous_response.previous_response = response
        previous_response.put()
        return True
    else:

        if response == previous_response.previous_response:
            logging.warning('urlfetch result %s same as last time',response)
            return False
            #sys.exit(0)
        else:
            previous_response.previous_response = response
            previous_response.put()
            logging.info('You add new query result %s to db',response)
            return True
"""
class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write('<html><head> \
                                <title>SpreadGoAent</title> \
                            </head><body>')

    url = "http://scola.hp.af.cm/"
    response = urlfetch_QQ_isExsit(url)

    response = response.split('|')

    try:
        int(response[0])
    except ValueError:
        logging.warning('urlfetch result is not QQ num,please check goagent.aws.af.cm server')
    else:
        numtoadr = lambda f: '<%s@qq.com>' %f
        addr = map(numtoadr, response)


    """
    logging.debug('You need to sendmail to %s@qq.com by gae',response[1:])
    self.response.out.write('You need to sendmail to %s@qq.com by gae.' %response[1:])

    retval = gae_sendmail(response[1:])
    if retval:
        self.response.out.write('Congratulations!Mail have been sent successfully by gae.')
    else:
        self.response.out.write('Sorry!Mail have not sent by gae.')

    logging.info('Mailbox %s@qq.com not found',response[1:])
    self.response.out.write('Mailbox %s@qq.com not found' %response[1:])
    """


    #response = urllib.urlopen('http://scola.hp.af.cm/').read()




    self.response.out.write("""
      </body>
      </html>""")
#if __name__ == '__main__':
logging.basicConfig(level=logging.INFO, format='%(levelname)s - - %(asctime)s %(message)s', datefmt='[%b %d %H:%M:%S]')
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
