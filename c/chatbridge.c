#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include "chatsvr.h"

struct server{
    int serfd;
    int lines_pending;
    char buf[MAXTRANSMISSION + 3];
    char *nextbuf;
    int bytes_in_buf;
}; 

struct client {
    int fd;
    char name[MAXHANDLE + 1];
    int namecomplete;
    struct client *next;
}*top = NULL;

extern char *memnewline(char *p, int size);  /* finds \r _or_ \n */
extern int isalldigits(char *s);
extern char *read_line_from_server(struct server *ser);
extern void send_another_server(char *message, int serverfd);
static void addclient(int serfd, char *handle);

static char bridge_handle[7] = "bridge";
static struct server **serverlist;
static int nservers = 0;


int main(int argc, char **argv)
{
    int i;
    char *host, *p;
    int port;
    fd_set fdlist;
    int maxfd = 0;
    
    extern void connect_to_server(char *host, int port, int serverindex);

    if (argc < 2) {
	fprintf(stderr, "usage: %s {host port ...} ...\n", argv[0]);
	return(1);
    }
    /* There can't be more than argc servers, so this is enough space: */
    if ((serverlist = malloc(argc * sizeof(struct server))) == NULL) {
	fprintf(stderr, "out of memory!\n");
	exit(1);
    }

    nservers = 0;
    for (i = 1; i < argc; i++) {
	if (isalldigits(argv[i])) {
            if ((port = atoi(argv[i])) <= 0) {
                fprintf(stderr, "%s: port argument must be a positive integer\n", argv[0]);
                return(1);
            }
	    connect_to_server(host, port, nservers++); /* doesn't return if error */
	} else {
	    host = argv[i];
	}
   }
//and the rest of your program goes here, obviously
  while (1) {
      for (i=0; i < nservers; i++){
        if(serverlist[i]->lines_pending){
             if ((p = read_line_from_server(serverlist[i]))){
                   send_another_server(p, serverlist[i]->serfd);
             }
         }
      }
      FD_ZERO(&fdlist);
      for (i=0; i < nservers; i++){
           FD_SET(serverlist[i]->serfd, &fdlist);
           if (serverlist[i]->serfd > maxfd){
                 maxfd = serverlist[i]->serfd;
           }
      }
      FD_SET(0, &fdlist);
      if (select(maxfd + 1, &fdlist, NULL, NULL, NULL) < 0) {
           perror("select");
           exit(1);
      }
      for (i=0; i < nservers; i++){
           if (FD_ISSET(serverlist[i]->serfd, &fdlist)) {
               if ((p = read_line_from_server(serverlist[i]))){
                     send_another_server(p, serverlist[i]->serfd);
               }
           }
      }
  }
return(0);
}


void connect_to_server(char *host, int port, int serverindex)
{
    struct hostent *hp;
    struct sockaddr_in r;
    char *p;
    int serverfd;
    int len;
    if ((hp = gethostbyname(host)) == NULL) {
	fprintf(stderr, "%s: no such host\n", host);
	exit(1);
    }
    if (hp->h_addr_list[0] == NULL || hp->h_addrtype != AF_INET) {
	fprintf(stderr, "%s: not an internet protocol host name\n", host);
	exit(1);
    }

    if ((serverfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket");
        exit(1);
    }

    r.sin_family = AF_INET;
    memcpy(&r.sin_addr, hp->h_addr_list[0], hp->h_length);
    r.sin_port = htons(port);

    if (connect(serverfd, (struct sockaddr *)&r, sizeof r) < 0) {
        perror("connect");
        exit(1);
    }
    if((serverlist[serverindex] = malloc(sizeof(struct server)))==NULL){
            fprintf(stderr, "out of memory!\n");
            exit(1);
    }
    serverlist[serverindex]->serfd = serverfd;
    serverlist[serverindex]->lines_pending = 0;
    serverlist[serverindex]->nextbuf = NULL;
    serverlist[serverindex]->bytes_in_buf = 0;
    while ((p = read_line_from_server(serverlist[serverindex])) == NULL)
	; /* i.e. loop until we get an entire line */
    if (strcmp(p, CHATSVR_ID_STRING)) {
	fprintf(stderr, "That is not a 'chatsvr'\n");
	exit(1);
    }
    strcat(bridge_handle, "\r\n");
    len = strlen(bridge_handle);
    if (write(serverfd, bridge_handle, len) != len) {
            perror("write");
            exit(1);
    }
}


/* This function is guaranteed to do at most one read(). */
char *read_line_from_server(struct server *s)
{
    int len;
    char *p;

    /*
     * If we returned a line last time, that's at the beginning of buf --
     * move the rest of the string over it.  The bytes_in_buf value has
     * already been adjusted.
     */
    if (s->nextbuf) {
	memmove(s->buf, s->nextbuf, s->bytes_in_buf);
	s->nextbuf = NULL;
    }

    /* Do a read(), unless we already have a whole line. */
    if (!memnewline(s->buf, s->bytes_in_buf)) {
	if ((len = read(s->serfd, s->buf + s->bytes_in_buf,
		    sizeof s->buf - s->bytes_in_buf - 1)) < 0) {
	    perror("read");
	    exit(1);
	}
	if (len == 0) {
	    printf("Server shut down.\n");
	    exit(0);
	}
	s->bytes_in_buf += len;
    }

    /* Now do we have a whole line? */
    if ((p = memnewline(s->buf, s->bytes_in_buf))) {
	s->nextbuf = p + 1;  /* the next line if the newline is one byte */
	/* but if the newline is \r\n... */
	if (s->nextbuf < s->buf + s->bytes_in_buf && *p == '\r' && *(p+1) == '\n')
	    s->nextbuf++;  /* then skip the \n too */
	/*
	 * adjust bytes_in_buf for next time.  Data moved down at the
	 * beginning of the next read_line_from_server() call.
	 */
	s->bytes_in_buf -= s->nextbuf - s->buf;
	*p = '\0';  /* we return a nice string */

	/* Is there a subsequent line already waiting? */
	s->lines_pending = !!memnewline(s->nextbuf, s->bytes_in_buf);

	return(s->buf);
    }

    /*
     * Is the buffer full even though we don't yet have a whole line?
     * This shouldn't happen if the server is following the protocol, but
     * still we don't want to infinite-loop over this.
     */
    if (s->bytes_in_buf == sizeof s->buf - 1) {
	s->buf[sizeof s->buf - 1] = '\0';
	s->bytes_in_buf = 0;
	s->lines_pending = 0;
	return(s->buf);  /* needn't set nextbuf because there's nothing to move */
    }

    /* No line yet.  Please try again later. */
    return(NULL);
}



char *memnewline(char *p, int size)  /* finds \r _or_ \n */
	/* This is like min(memchr(p, '\r'), memchr(p, '\n')) */
	/* It is named after memchr().  There's no memcspn(). */
{
    for (; size > 0; p++, size--)
	if (*p == '\r' || *p == '\n')
	    return(p);
    return(NULL);
}


int isalldigits(char *s)
{
    for (; *s; s++)
	if (!isdigit(*s))
	    return(0);
    return(1);
}

void send_another_server(char *message, int serverfd)
{
  //message now, char *message = "bert: ryan, hello"; from read_line_server
  char say[5] = "says";
  // output "bert says: ryan, hello"
  int len;
  len = strlen(message);
  char *p;
  char *q;
  char copy[len+5];
  message[len] = '\0';
  p = strchr(message, ':');
  *p = '\0';
  bridge_handle[7] = '\0';
  if (strcmp(message, bridge_handle) != 0){
  // get name "bert", first handle putinto linkedlist
       addclient(serverfd, message);
       strcpy(copy, message);
       strcat(copy, " ");
       strcat(copy,say);
       strcat(copy, ": "); // make copy now "bert says:"

       *p = ':';         // message change it back to original
       if((q = strchr(message, ','))){
             char pointer[MAXHANDLE + 1]; // another handle
             int i=0;
             p+=2;
             while(p!=q){
                 pointer[i] = *p;
                 i++;
                 p++;
             }
             int len2;
             //len2 = strlen(pointer);
             pointer[i] = '\0';
   // get another name "ryan", check if it in linked list, get the end of message after ":"
             strcat(copy, pointer);
             i=0;
             char copy2[len];
             while(*p!='\0'){
                  copy2[i] = *p;
                  p++;
                  i++;
             }
             len2 = strlen(copy2); 
             copy2[len2] = '\0';
             strcat(copy,copy2);
             copy[len+5] = '\0';
             struct client *pp;
             for (pp = top; pp; pp = pp->next){
                 if((pp->fd != serverfd)&&(strcmp(pp->name, pointer)==0)){
                       strcat(copy, "\r\n");
                       len = strlen(copy);
                       if(write((pp->fd), copy, len) != len)
                             perror("write");
                  }
             }
       }
  }
}



static void addclient(int serfd, char *handle)
{
    struct client **pp;
    for (pp = &top; *pp; pp = &(*pp)->next){
           if(((*pp)->fd == serfd)&&(strcmp((*pp)->name, handle)==0))
                 break;
    }
    if (*pp){;}else{
         struct client *p = malloc(sizeof(struct client));
         if (!p) {
             fprintf(stderr, "out of memory!\n");  /* highly unlikely to happen */
             exit(1);
         }
         p->fd = serfd;
         strcpy(p->name, handle);
         p->namecomplete = 1;
         p->next = top;
         top = p;
    }
}
