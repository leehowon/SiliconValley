# -*- coding:utf-8 -*-

import os;
import socket;
import datetime;

IS_DEBUG = False;

ENC_UTF8 = "UTF-8";
ENC_ISO_8859 = "ISO-8859-1";

BYTE_LEN = 4096;
IP = "127.0.0.1";
PORT = 3030;

NEW_LINE = "\r\n";
COMMANDS = [ "cd", "cat", "ll", "pwd", "q", "quit" ];

OS_PATH = os.path;

def log( text ) :
    if IS_DEBUG : print( text );

def pwd() :
    return NEW_LINE + OS_PATH.abspath( "." ) + NEW_LINE + NEW_LINE;

def listdir( path = "." ) :
    try :
        if path != "." : os.chdir( path );
    
        lists = os.listdir();
        data = pwd();

        if len( lists ) == 0 :
            return data + "This Directory is empty.";
        
        for li in lists :
            stat = os.stat( li );
            data += getdate( stat.st_ctime );

            if OS_PATH.isdir( li ) : data += " <DIR> ";
            else : data += "       ";

            data += li + NEW_LINE;

        return data;
    except NotADirectoryError :
        return path + " is not Directory";
    except FileNotFoundError :
        return "FileNotFound Error";
    except PermissionError :
        return "Permission Error";

def putsockdata( sock, data ) :
    if sock is None : return "";

    log( "put data : " + data );
    sock.send( data.encode(ENC_UTF8) );

def getdate( timestamp = 0 ) :
    return datetime.datetime.fromtimestamp( timestamp ).strftime( "%Y-%m-%d %H:%M:%S" );

def getcontent( filename ) :
    if OS_PATH.isfile( filename ) is False : return filename + " is not File.";
    else :
        data = b"";
        file = open( filename, "rb" );
        
        while True :
            temp = file.read( BYTE_LEN );

            if temp == b"" :
                file.close();
                break;

            data += temp;

        try :
            return data.decode( ENC_UTF8 );
        except UnicodeDecodeError :
            return data.decode( ENC_ISO_8859 );

def getsockdata( sock ) :
    if sock is None : return "";

    data = sock.recv( BYTE_LEN );
    log( b"recv data : " + data );
    
    return data.decode( ENC_UTF8 ).rstrip( NEW_LINE );

def socklisten():
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM );
    sock.bind( (IP, PORT) );
    sock.listen( 1 );
    conn, addr = sock.accept();
    log( addr );
    putsockdata( conn, "HI!\r\nWelcome to File System." + NEW_LINE + "\
You can usable this commands [ " + ", ".join(COMMANDS) + " ]" );
    
    while True :
        data = getsockdata( conn );
        
        if not data : break;

        arr = data.split(" ");
        command = arr[0];
        arguments = arr[1:];

        if command == "cd" :
            putsockdata( conn, listdir(arguments[0]) );
        elif command == "cat" :
            putsockdata( conn, getcontent(arguments[0]) );
        elif command == "ll" :
            putsockdata( conn, listdir() );
        elif command == "pwd" :
            putsockdata( conn, pwd() );
        elif command == "q" or command == "quit" :
            putsockdata( conn, NEW_LINE );
        else :
            putsockdata( conn, "try input commands." );

    conn.close();

if __name__ == "__main__" :
    socklisten();
