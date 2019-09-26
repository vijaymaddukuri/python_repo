value = "SEIPAAAAQACAAAAAAAAAAE9maWxlNjBtYgC6bztaHtspRxMSI0zZ0OHncA=="

hexstr = value.encode("utf-16")

import io
import gzip

# this raises IOError because `buf` is incomplete. It may work if you supply the complete buf
buf = "SEIPAAAAQACAAAAAAAAAAE9maWxlNjBtYgC6bztaHtspRxMSI0zZ0OHncA=="
with gzip.GzipFile(fileobj=io.BytesIO(buf)) as f:
    content = f.read()
    print(content.decode('utf-16'))

print('HB\x0f\x00\x00\x00@\x00\x80\x00\x00\x00\x00\x00\x00\x00Ofile60mb\x00\xbao;Z\x1e\xdb)G\x13\x12#L\xd9\xd0\xe1\xe7p')

