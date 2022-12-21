#include <stdio.h>
#include <stdlib.h>
#include <ncurses.h>
#include "csv.h"
#include "socket_quit.h"
#include "app.h"
#include "gpio.h"
#include "menu.h"




#define WIDTH 105
#define HEIGHT 40

WINDOW *window;

char *choices[] = {
    "Lampada 01 da Sala:",
    "Lampada 02 da Sala:",
    "Ar-Condicionado:",
    "Ativar o Alarme:",
    "Sair",
};

int optionX = 0;
int optionY = 0;
int choices_length = sizeof(choices) / sizeof(char *);

void printMenu(WINDOW *window, int highlight) {
	int x = 2, y = 4, i;
	box(window, 0, 0);

	for(i = 0; i < choices_length; i++) {
		if (i == choices_length - 1) {
			wattron(window, COLOR_PAIR(2));
		}

		if (highlight == i + 1) {
			wattron(window, A_REVERSE);
			mvwprintw(window, y, x, "%s", choices[i]);
			wattroff(window, A_REVERSE);
		} else {
			mvwprintw(window, y, x, "%s", choices[i]);
		}

		if (i == choices_length - 1) {
			wattroff(window, COLOR_PAIR(2));
		}

		++y;
	}

	wrefresh(window);
}

void clearMenu(WINDOW *window_param) {
	wclear(window_param);
	wborder(window_param, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ');  
	wrefresh(window_param);
	delwin(window_param); 
}

void printData(Data data) {
  wattron(window, COLOR_PAIR(data.devOut.l01 == 1 ? 3 : 2));
	mvwprintw(window, 4, 41, data.devOut.l01 == 1 ? "ON " : "OFF");
	wattroff(window, COLOR_PAIR(data.devOut.l01 == 1 ? 3 : 2));

  wattron(window, COLOR_PAIR(data.devOut.l02 == 1 ? 3 : 2));
	mvwprintw(window, 5, 41, data.devOut.l02 ? "ON " : "OFF");
	wattroff(window, COLOR_PAIR(data.devOut.l02 == 1 ? 3 : 2));
  
  wattron(window, COLOR_PAIR(data.devOut.pr == 1 ? 3 : 2));
	mvwprintw(window, 5, 41, data.devOut.pr ? "ON " : "OFF");
	wattroff(window, COLOR_PAIR(data.devOut.pr == 1 ? 3 : 2));

  wattron(window, COLOR_PAIR(data.devOut.ac == 1 ? 3 : 2));
	mvwprintw(window, 7, 41, data.devOut.ac == 1 ? "ON " : "OFF");
	wattroff(window, COLOR_PAIR(data.devOut.ac == 1 ? 3 : 2));

  wattron(window, COLOR_PAIR(data.devOut.alarm == 1 ? 3 : 2));
	mvwprintw(window, 13, 41, data.devOut.alarm == 1 ? "ON " : "OFF");
	wattroff(window, COLOR_PAIR(data.devOut.alarm == 1 ? 3 : 2));

  mvwprintw(window, 19, 2, "Temperatura - sala1: ");
  wattron(window, COLOR_PAIR(1));
  mvwprintw(window, 19, 25, "%4.2f", data.dht22Class1.temperature);
	wattroff(window, COLOR_PAIR(1));
  mvwprintw(window, 20, 2, "Umidade - sala1: ");
	wattron(window, COLOR_PAIR(1));
  mvwprintw(window, 20, 25, "%4.2f", data.dht22Class1.humidity);
	wattroff(window, COLOR_PAIR(1));

	mvwprintw(window, 25, 2, "Alarme Tocando: ");
  wattron(window, COLOR_PAIR(data.devOut.alarmPlaying == 1 ? 3 : 2));
	mvwprintw(window, 25, 18, data.devOut.alarmPlaying == 1 ? "SIM" : "NAO");
	wattroff(window, COLOR_PAIR(data.devOut.alarmPlaying == 1 ? 3 : 2));

  wrefresh(window);
}

void printDevicesIn(DevicesIn devIn) {
  mvwprintw(window, 4, 50, "sala 01 - Sensor de Presenca:");
	wattron(window, COLOR_PAIR(devIn.spres == 1 ? 3 : 2));
	mvwprintw(window, 4, 89, devIn.spres == 1 ? "ON " : "OFF");
	wattroff(window, COLOR_PAIR(devIn.spres == 1 ? 3 : 2));

  mvwprintw(window, 5, 50, "Sala 01 - Sensor de Fumaca:");
	wattron(window, COLOR_PAIR(devIn.sfum == 1 ? 3 : 2));
	mvwprintw(window, 5, 89, devIn.sfum == 1 ? "ON " : "OFF");
	wattroff(window, COLOR_PAIR(devIn.sfum == 1 ? 3 : 2));

  mvwprintw(window, 6, 50, "Sala 01 - Sensor de Janela 01:");
	wattron(window, COLOR_PAIR(devIn.sjan == 1 ? 3 : 2));
	mvwprintw(window, 6, 89, devIn.sjan == 1 ? "ON " : "OFF");
	wattroff(window, COLOR_PAIR(devIn.sjan == 1 ? 3 : 2));



  mvwprintw(window, 8, 50, "Sala 01 - Sensor de Porta:");
	wattron(window, COLOR_PAIR(devIn.spor == 1 ? 3 : 2));
	mvwprintw(window, 8, 89, devIn.spor == 1 ? "ON " : "OFF");
	wattroff(window, COLOR_PAIR(devIn.spor == 1 ? 3 : 2));
	mvwprintw(window, 25, 50, "Pessoas: ");
  wattron(window, COLOR_PAIR(1));
	mvwprintw(window, 25, 59, devIn.peopleQuantity >= 10 ? "%d" : "0%d", devIn.peopleQuantity);
	wattroff(window, COLOR_PAIR(1));

  wrefresh(window);
}

void printHeader() {
	wattron(window, COLOR_PAIR(4));
	mvwprintw(window, 2, 15, "DISPOSITIVOS DE SAIDA");
	wattroff(window, COLOR_PAIR(4));

	wattron(window, COLOR_PAIR(4));
	mvwprintw(window, 2, 61, "DISPOSITIVOS DE ENTRADA");
	wattroff(window, COLOR_PAIR(4));

	wattron(window, COLOR_PAIR(4));
	mvwprintw(window, 17, 37, "TEMPERATURA E UMIDADE");
	wattroff(window, COLOR_PAIR(4));

	wattron(window, COLOR_PAIR(4));
	mvwprintw(window, 23, 13, "ALARME");
	wattroff(window, COLOR_PAIR(4));

	wattron(window, COLOR_PAIR(4));
	mvwprintw(window, 23, 57, "QUANTIDADE DE PESSOAS");
	wattroff(window, COLOR_PAIR(4));
}

void* menuHandler() {
	int highlight = 1;
	int choice = 0;
	int c;

	initscr();
	start_color(); 
	clear();
	noecho();
	cbreak();
	curs_set(0);
	init_pair(1, COLOR_CYAN, COLOR_BLACK);
	init_pair(2, COLOR_RED, COLOR_BLACK);
	init_pair(3, COLOR_GREEN, COLOR_BLACK);
	init_pair(4, COLOR_MAGENTA, COLOR_BLACK);
     
	window = newwin(HEIGHT, WIDTH, optionY, optionX);
	keypad(window, TRUE);
	refresh();

	dataInit();

	do {
		printHeader();
		printMenu(window, highlight);
		c = wgetch(window);

		switch(c) {
			case KEY_UP:
				if(highlight == 1)
					highlight = choices_length;
				else
					--highlight;
				break;
			case KEY_DOWN:
				if(highlight == choices_length)
					highlight = 1;
				else
					++highlight;
				break;
			case 6:    
				choice = highlight;

				DevicesOut devOut = recoverDevicesOutData();

                switch(choice) {
                    case 1:
                        if(devOut.l01){
                            devOut.l01 = 0;
                        }
                        else {
                            devOut.l01 = 1;
                        }
                        char *device1 = "Lâmpada 01 da Sala";
                        Command command1;
                        command1.device = device1;
                        command1.state = devOut.l01;
                        writeData(command1);
                        break;
                    case 2:
                        if(devOut.l02){
                            devOut.l02 = 0;
                        }
                        else {
                            devOut.l02 = 1;
                        }
                        char *device2 = "Lâmpada 02 da Sala";
                        Command command2;
                        command2.device = device2;
                        command2.state = devOut.l02;
                        writeData(command2);
                        break;
                    
                    case 3:
                        if(devOut.ac) {
                            devOut.ac = 0;
                        }
                        else {
                            devOut.ac = 1;
                        }
                        char *device3 = "Ar-Condicionado sala 01";
                        Command command3;
                        command3.device = device3;
                        command3.state = devOut.ac;
                        writeData(command3);
                        break;
                   
    
                    case 4:
                        if(devOut.pr){
                            devOut.pr = 0;
                        }
                        else {
                            devOut.pr = 1;
                        }
                        char *device4 = "Ativar o Projetor Multimídia";
                        Command command4;
                        command4.device = device4;
                        command4.state = devOut.pr;
                        writeData(command4);
                        break;

                 case 5:
                        if(devOut.alarm){
                            devOut.alarm = 0;
                        }
                        else {
                            devOut.alarm = 1;
                        }
                        char *device5 = "Ativar o Alarme";
                        Command command5;
                        command5.device = device5;
                        command5.state = devOut.alarm;
                        writeData(command5);
                        break;
                }
				storeDevicesOutUpdate(devOut);
				if (choice == 11) {
					char *message = "Finalizando. . .";
					quitHandler(message);
				}
				break;
			default:
				refresh();
				break;
		}
	} while(1);

	return NULL;
}