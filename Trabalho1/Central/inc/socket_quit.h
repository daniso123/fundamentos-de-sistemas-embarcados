#ifndef SOCKET_QUIT_H_
#define SOCKET_QUIT_H_

void finish(int signal);
void finishWithError(int signal);
void quitSetup();
void quitHandler(char *message);

#endif