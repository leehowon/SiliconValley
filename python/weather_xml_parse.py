import codecs;
import http.client;
import sys;
from xml.dom import minidom;

METHOD_GET = "GET";
ENC_UTF8 = "UTF-8";

def getText( nodelist ):
    rc = [];
    
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append( node.data );
        else :
            rc.extend( getText(node.childNodes) );

    return "".join( rc );

def getHttpContent( url, path = "" ):
    conn = http.client.HTTPConnection( url );
    conn.request( METHOD_GET, path );

    response = conn.getresponse();

    if response.status != 200 :
        print( "exit" );
        conn.close();
        return;

    #print( response.status, response.reason );
    buffersize = 4096;
    httptext = b"";
    size = response.length;
    
    while not response.closed and size > 0 :
        httptext += response.read( buffersize );
        size = response.length;

    conn.close();

    return httptext.decode( ENC_UTF8 );

def printWeather( xmlString ):
    doc = minidom.parseString( xmlString );
    locations = doc.getElementsByTagName( "location" );

    print( getText(doc.getElementsByTagName("pubDate")) + " 날씨\n" );
    
    for location in locations :
        print( " " + getText(location.getElementsByTagName("city")) );
        print( "------------------------------------" );
        
        data = location.getElementsByTagName( "data" );

        for d in data :
            print( "날짜 : " + getText(d.getElementsByTagName("tmEf")) );
            print( "날씨 : " + getText(d.getElementsByTagName("wf")) );
            print( "최저 : " + getText(d.getElementsByTagName("tmn")) );
            print( "최고 : " + getText(d.getElementsByTagName("tmx")) + "\n" );
            
        print("\n");
        
def main( url, path ):
    httptext = getHttpContent( url, path );

    if httptext is None or len( httptext ) < 1 :
        print( "no content" );
        return;

    printWeather( httptext );

if __name__ == "__main__" :
    url = "http://www.kma.go.kr";
    path = "/weather/forecast/mid-term-rss3.jsp?stnId=108";

    if len( sys.argv ) > 1 :
        url = "localhost:8080";
        path = "/weather.xml";

    main( url, path );
