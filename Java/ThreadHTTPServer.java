/**
 *   HTTP Server, Multi Threaded
 *   Usage:  java ThreadHTTPServer [port#  [http_root_path]]
 *
 **/

import java.io.*;
import java.net.*;
import java.util.*;

class HTTPThread implements Runnable {
    private Socket connectSocket;
    private String path;

    // constructor to instantiate the HTTPThread object
    public HTTPThread(Socket connectionSocket, String http_root_path) {
    	connectSocket = connectionSocket;
    	path = http_root_path;
    }

    public void run() {
	// invoke processRequest() to process the client request and then generateResponse()
    	try{
    		processRequest(connectSocket);
    	}catch (Exception e){
		}
	// to output the response message
    } 

    private void processRequest(Socket connectionSocket) throws Exception  {
	// same as in single-threaded (this code is inline in the starter code)

		// create buffered reader for client input
		BufferedReader inFromClient = 
			new BufferedReader(new InputStreamReader(connectionSocket.getInputStream())); // ADD_CODE

		String requestLine = null;	// the HTTP request line
		String requestHeader = null;	// HTTP request header line

		/* Read the HTTP request line and display it on Server stdout.
		 * We will handle the request line below, but first, read and
		 * print to stdout any request headers (which we will ignore).
		 */
		requestLine = inFromClient.readLine(); // ADD_CODE
		System.out.println(requestLine);

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
	    } 

    

    private void generateResponse(String urlName, Socket connectionSocket) throws Exception {
	// same as in single-threaded
    	DataOutputStream  outToClient = 
             new DataOutputStream(connectionSocket.getOutputStream());   

	String fileLoc = path + "/" + urlName;// ADD_CODE: map urlName to rooted path  ??
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
}    



public final class ThreadHTTPServer {
	public static int serverPort = 35180;
    	public static String http_root_path = "/cmshome/liangz10";

    	public static void main(String args[]) throws Exception  {
		// process command-line options
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

		// create a listening ServerSocket
		ServerSocket multiSocket = null;
		Socket connectionSocket = null;

		multiSocket = new ServerSocket(serverPort);
		System.out.println("Listening on" + serverPort + http_root_path);	
		while (true) {
	    	// accept a connection
			connectionSocket = multiSocket.accept();
			System.out.println("connection from " + connectionSocket.getInetAddress()
				+ "." + connectionSocket.getPort());  
	    	// Construct an HTTPThread object to process the accepted connection
			HTTPThread http_thread = new HTTPThread(connectionSocket, http_root_path);
	    	// Wrap the HTTPThread in a Thread object
        		Thread thread = new Thread(http_thread);
	    	// Start the thread.
	    		thread.start();
		}
	
    	} 

}
