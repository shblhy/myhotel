import re
 
def from_pattern(pattern, type):
    def coerce(value, *args):
        value = str(value)
        match = pattern.search(value)
        if match is not None:
            return type(match.group(1), *args)
        raise ValueError("unable to coerce '%s' into a %s" % (value, type.__name__))
    return coerce
 
to_int = from_pattern(re.compile('([-+]?[0-9A-F]+)', re.IGNORECASE), int)

kilobytes = lambda x:int(x*1024)

megabytes = lambda x:int(x*1024*1024)

def chunked_encoder(fileish, chunk_limit=kilobytes(0.5)):#;megabytes(0.5)):
    def generator():
        while True:
            value = fileish.read(chunk_limit)
            bytesLen = len(value)
            if bytesLen:
                yield '%x\r\n' % bytesLen
                yield '%s\r\n' % value
            else:
                yield '0\r\n'
                yield '\r\n'
                return
    
    return generator()
 
 
# length_limit=20
def chunked_decoder(fileish, chunk_limit=megabytes(1)):
    def generator():
        while True:
            index = fileish.readline(len('%x' % chunk_limit))
 
            if not index:
                raise EOFError("unexpected blank line")
 
            length = coerce.to_int(index, 16)
 
            if not length:
                return
 
            if length > chunk_limit:
                raise OverflowError("invalid chunk size of '%d' requested, max is '%d'" % (length, chunk_limit))
 
            value = fileish.read(length)
 
            yield value
            
            tail = fileish.read(2)
 
            assert tail == "\r\n", "unexpected characters '%s' after chunk" % tail
 
    return generator()