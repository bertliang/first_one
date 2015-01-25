/**
 * HTTP Server, Single Threaded,  starter code.  
 * Usage:  java HTTPServer [port#  [http_root_path]]
 **/

import java.io.*;
import java.net.*;
import java.util.*;

public final class HTTPServer {
    public static int serverPort = 35180;    // default port CHANGE THIS 35180-35189
    public static String http_root_path = "/cmshome/liangz10";    // rooted default path in your mathlab area
    public static Date d = null;

    public static void main(String args[]) throws Exception  {
	// ADD_CODE: allow the user to choose a different port, as arg[0] 
	if(args.length>0){
		serverPort = Integer.parseInt(args[0]);
	} 
    
    // ADD_CODE: allow the user to choose a different http_root_path, as arg[1] 
    if(args.length>1){
    	http_root_path = args[1];
    }

	
	// display error on server stdout if usage is incorrect
	if (args.length > 2) {
	    System.out.println("usage: java HTTPServer [port_# [http_root_path]]");
	    System.exit(0);
	}

	// ADD_CODE: create server socket
	ServerSocket singleSocket = null;
	Socket connectionSocket = null;

	singleSocket = new ServerSocket(serverPort);

	// ADD_CODE: display server stdout message indicating listening
	// on port # with server root path ...
	System.out.println("listening from port" + serverPort + http_root_path); 

	// server runs continuously
	while (true) {
	    try {
		// ADD_CODE: take a waiting connection from the accepted queue
		connectionSocket = singleSocket.accept();

		// ADD_CODE: display on server stdout the request origin
		System.out.println("connection from " + connectionSocket.getInetAddress()
			+ "." + connectionSocket.getPort());  
	
		/* you may wish to factor out the remainder of this
		 * try-block code as a helper method, that could be used
		 * by your multi-threaded solution, since it will require
		 * essentially the same logic for its threads.
		 */

		// create buffered reader for client input
		BufferedReader inFromClient = 
			new BufferedReader(new InputStreamReader(connectionSocket.getInputStream())); // ADD_CODE

		String requestLine = null;	// the HTTP request line
		String headers = null;

		/* Read the HTTP request line and display it on Server stdout.
		 * We will handle the request line below, but first, read and
		 * print to stdout any request headers (which we will ignore).
		 */
		requestLine = inFromClient.readLine(); // ADD_CODE
		System.out.println(requestLine);
		while ((headers = inFromClient.readLine()) != ""){
			if(headers.contains("If-Modified-Since")){
				//If-Modified-Since: Sat, 29 Oct 1994 19:43:31 GMT
				System.out.println(headers);
				SimpleDateFormat format = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss zzz");
				d = format.parse(headers);
				System.out.println(d);
			}
		}

		// now back to the request line; tokenize the request
		StringTokenizer tokenizedLine = new StringTokenizer(requestLine);
		// process the request
		if (tokenizedLine.nextToken().equals("GET")) {
		    String urlName = null;
		    // parse URL to retrieve file name
		    urlName = tokenizedLine.nextToken();
	    
		    if (urlName.startsWith("/") == true )
			urlName  = urlName.substring(1);
		    	System.out.println(urlName);
		    generateResponse(urlName, connectionSocket);

		} 
		else 
		    System.out.println("Bad Request Message");
	    } catch (Exception e) {
		}
	}  // end while true 
	
    } // end main

    private static void generateResponse(String urlName, Socket connectionSocket) throws Exception
    {
	// ADD_CODE: create an output stream
	DataOutputStream  outToClient = 
             new DataOutputStream(connectionSocket.getOutputStream());   

	String fileLoc = http_root_path + "/" + urlName;// ADD_CODE: map urlName to rooted path  ??
	System.out.println ("Request Line: GET " + fileLoc);

	File file = new File( fileLoc );
	if (!file.isFile())
	{
	    // generate 404 File Not Found response header
	    outToClient.writeBytes("HTTP/1.0 404 File Not Found\r\n");
	    // and output a copy to server's stdout
	    System.out.println ("HTTP/1.0 404 File Not Found\r\n");
	} else {
	    // get the requested file content
	    int numOfBytes = (int) file.length();
	    
	    FileInputStream inFile  = new FileInputStream (fileLoc);
	
	    byte[] fileInBytes = new byte[numOfBytes];
	    inFile.read(fileInBytes);

	    FileNameMap fnm = URLConnection.getFileNameMap();
	    String type = fnm.getContentTypeFor(fileLoc);
	    // Source http://stackoverflow.com/questions/51438/getting-a-files-mime-type-in-java //

	    if(d != null){
	    	Date last = new Date(file.lastModied()); 
	    	System.out.println(last);
	    	//Returns the time that the file denoted by this abstract pathname was last modified.
	    	if (d.compareTo(last)>0){
	    		//the value 0 if the argument Date is equal to this Date;
	    		//a value less than 0 if this Date is before the Date argument; 
	        	//and a value greater than 0 if this Date is after the Date argument.
	    		//the server SHOULD return a 304 (NotModified) response.
	    		 outToClient.writeBytes("HTTP/1.0 304 (NotModified)\r\n");
	    		// and output a copy to server's stdout
	    		System.out.println ("HTTP/1.0 304 (NotModified)\r\n");
	    	}
	    	
	    }

	    // ADD_CODE: generate HTTP response line; output to stdout
	    System.out.println("HTTP/1.0 ok\r\n");
	    outToClient.writeBytes("HTTP/1.0 ok\r\n");
	
	    // ADD_CODE: generate HTTP Content-Type response header; output to stdout
	    System.out.println("Content-Type: " + type + " \r\n");
	    outToClient.writeBytes("Content-Type: " + type + " \r\n");

	    // ADD_CODE: generate HTTP Content-Length response header; output to stdout
 		System.out.println("Content-Length: " + numOfBytes + " \r\n");
	    // send file content
	    outToClient.write(fileInBytes, 0, numOfBytes);
	}  // end else (file found case)

	// close connectionSocket
	connectionSocket.close();
    } // end of generateResponse
    
} // end of class HTTPServer
