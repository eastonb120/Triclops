/********************************************************************
*Filename	:	rotate.c
*Description	:	make a pin active then inactive
*Date		:	4/14/2018
********************************************************************/
#include <wiringPi.h>
#include <stdio.h>
//Reference by GPIO Number not by actual pin
#define StepPin		3

int main(void)
{
	if(wiringPiSetup() == -1){
		printf("setup wiringPi failed!");
	}
	printf("Linker LedPin   :   GPIO %d(wiringPi pin)\n", StepPin);

	pinMode(StepPin, OUTPUT);

	while(1){
		digitalWrite(StepPin, LOW);
		delay(2);
		digitalWrite(StepPin, HIGH);
		delay(2);
	}

	return(0);
}

