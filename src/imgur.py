import os
import pycurl
import xml.parsers.expat

from lookit import liblookit

IMGUR_ALLOWED = ['JPEG', 'GIF', 'PNG', 'APNG', 'TIFF', 'BMP', 'PDF', 'XCF']

class ImgurUploader:
    def __init__(self):
        self.response = ''
        self.current_key = None
        self.mapping = {}

    def xml_ele_start(self, name, attrs):
        self.current_key = str(name)

    def xml_ele_end(self, name):
        self.current_key = None

    def xml_ele_data(self, data):
        if self.current_key is not None:
            self.mapping[self.current_key] = str(data)

    def curl_response(self, buf):
        self.response = self.response + buf

    def upload(self, image):
        # Note: This key is specific for Lookit. If you want to use
        # the Imgur API in your application, please register for a new
        # API key at: http://imgur.com/register/api/
        client_id = 'cde2ab3f2b4972c'
        key = os.getenv('IMGUR_CLIENT_ID', client_id)

        c = pycurl.Curl()
        values = [('image', (c.FORM_FILE, image))]
        c.setopt(pycurl.HTTPHEADER, ['Authorization:  Client-ID ' + key])
        c.setopt(c.URL, 'https://api.imgur.com/3/upload.xml')
        c.setopt(c.HTTPPOST, values)
        c.setopt(c.WRITEFUNCTION, self.curl_response)
        c.setopt(c.USERAGENT, 'liblookit/' + liblookit.VERSION_STR)

        c.perform()
        c.close()

        p = xml.parsers.expat.ParserCreate()

        p.StartElementHandler = self.xml_ele_start
        p.EndElementHandler = self.xml_ele_end
        p.CharacterDataHandler = self.xml_ele_data

        p.Parse(self.response)
