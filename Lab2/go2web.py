import socket
import validators
import ssl
import json
import os

from bs4 import BeautifulSoup

KNOWN_FLAGS = ["-u", "-s", "-h"]

def main():
    while(True):
        print("> ", "")
        inputCommand = input()
        commandWords = inputCommand.split()

        if commandWords[1] == "-h":
            help()
            continue

        if not isCommandValid(commandWords):
            continue

        if commandWords[1] == "-u":
            getUrl(commandWords[2])
            continue

        if commandWords[1] == "-s":
            search(commandWords[2:])
            continue   

def help():
    print("Available commands are:\n\
            go2web -h               # show help\n\
            go2web -u <URL>         # make request to URL and print the response\n\
            go2web -s <search-term> # search the term and print top 5 results")
 
def search(searchString):
    request_url = f"/customsearch/v1?key=AIzaSyD1TY-uJDXAl4m01lCC-orZUfga_D2e_zw&cx=f2ff5f215d5484786&q={searchString}&start=1&num=5"
    request = "GET " + request_url + " HTTP/1.1\r\nConnection:close\r\nHost:www.googleapis.com\r\n\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        sslClient = ssl.wrap_socket(client)
        sslClient.connect(("www.googleapis.com", 443))  
        sslClient.send(request.encode())  

        chunks = []
        while True:
            data = sslClient.recv(2048)
            if not data:
                break
            chunks.append(data.decode())       
        stringResult = ''.join(chunks)

        response = stringResult[stringResult.find("{"):].replace("\n", "").replace("\r", "")[:-1]
        jsonResult = json.loads(response)
        for index, item in enumerate(jsonResult["items"]):
            print(str(index + 1), end=". ")
            print(item["title"])
        
        
        while True:
            print("Type a number from 1 to 5, if you want to open a link, type 'c' to close")
            print(": ", "")
            inputCommand = input()

            if(inputCommand == 'c'):
                break
            
            try:
                urlNumber = int(inputCommand)
                if urlNumber > 0 and urlNumber <= 10:
                    getUrl(list(jsonResult["items"])[urlNumber - 1]["link"])
                else:
                    print("!!! Unkown command")
            except ValueError:
                print("!!! Unkown command")


def getUrl(url):
    urlWithoutProtocol = url.replace("http://", "").replace("https://", "")
    [host, path] =  urlWithoutProtocol.split("/", 1) if "/" in urlWithoutProtocol else [urlWithoutProtocol, ""]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        sslClient =  ssl.create_default_context().wrap_socket(client, server_hostname=host)

        # connect the client 
        sslClient.connect((host, 443))  
        
        # send request 
        request = "GET /" + path + " HTTP/1.1\r\naccept: text/html\r\nConnection: close\r\nHost:" + host + "\r\n\r\n"
        sslClient.send(request.encode())  

        response = b""
        while True:
            data = sslClient.recv(1024)
            response += data
            if not data or response.endswith(b'\r\n0\r\n\r\n'):
                break
        soup = BeautifulSoup(response[response.lower().find(b"<html"):], 'html.parser')
        print(os.linesep.join([s for s in soup.get_text().splitlines() if s]))

    

def isCommandValid(commandWords):
    if len(commandWords) < 2:
        print("!!! Unknown or incorrect command, please check the 'go2web -h' to see all the available commands")
        return False
    if commandWords[0] != "go2web":
        print("!!! First word of the command should be 'go2web' \nPlease check the 'go2web -h' to see all the available commands")
        return False
    if commandWords[1] not in KNOWN_FLAGS:
        print(f"!!! Unknown flag '{commandWords[1]}'\nPlease check the 'go2web -h' to see all the available commands")
        return False; 
    if commandWords[1] == "-u":
        if len(commandWords) != 3:
            print("!!! Incomplete command, please check the 'go2web -h' to see all the available commands")
            return False
        
        isUrlValid = validators.url(commandWords[2]) or validators.domain(commandWords[2])
        if not isUrlValid:
            print("!!! Incorrect URL, please check the URL and try again")
            return False

    if commandWords[1] == "-h":
        if len(commandWords) > 2:
            print("!!! Incorrect command \nPlease check the 'go2web -h' to see all the available commands")
            return False 
    
    if commandWords[1] == '-s':
        if len(commandWords) <= 2:
            print("!!! Incorrect command \nSearch command should contain a <search_tearm>")
            return False         

    return True 

main()