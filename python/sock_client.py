# -*- coding:utf-8 -*-

import sys;
import socket;

IS_DEBUG = False;

ENC_UTF8 = "UTF-8";
ENC_ISO_8859 = "ISO-8859-1";

BYTE_LEN = 4096;

NEW_LINE = "\r\n";

def log( text ) :
    if IS_DEBUG : print( text );
    
def usage() :
    print( "Usage : py " + sys.argv[ 0 ] + " -ip <ip>\
 [ -p | -port ] <port> [ -d | -dirpath ] <dirpath>" );
    sys.exit( -1 );

def putsockdata( sock, data ) :
    if sock is None : return "";

    log( "put data : " + data );
    sock.send( data.encode(ENC_UTF8) );
    
def getsockdata( sock ) :
    if sock is None : return "";

    data = sock.recv( BYTE_LEN );
    log( b"recv data : " + data );

    return data.decode( ENC_UTF8 ).rstrip( NEW_LINE );

def sockopen( ip, port, dirpath ) :
    if ip == "" or port == "" : usage();

    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM );
    sock.connect( (ip, port) );

    data = getsockdata( sock );

    if data : print( data );

    while True :
        sendata = input( "command : " );

        if sendata == "" : continue;
        
        putsockdata( sock, sendata );
        recvdata = getsockdata( sock );

        if recvdata == "" : break;
        
        print( recvdata );
        
    sock.close();

if __name__ == "__main__" :
    argv = sys.argv[ 1: ];
    arglen = len( argv );

    if arglen not in ( 4, 6 ) : usage();

    conf = { "ip": "", "port": "", "dirpath": "" };
    opts = [ "-ip", "-port", "-p", "-dirpath", "-d" ];
    
    for li in range( 0, arglen, 2 ) :
        opt = argv[ li ]
        val = argv[ li + 1 ];
        
        if opt not in opts : usage();

        if opt in ( "-ip" ) : conf[ "ip" ] = val;
        
        if opt in ( "-p", "-port" ) : conf[ "port" ] = val;

        if opt in ( "-d", "-dirpath" ) : conf[ "dirpath" ] = val;

    sockopen( ip = conf[ "ip" ], port = int( conf["port"] ), dirpath = conf[ "dirpath" ] );
    
