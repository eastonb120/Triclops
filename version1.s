//Define initial data for program
.section		.data
		.balign 4
Intro:		.asciz "Triclops Version 1\n\n\n"
Rotate:		.asciz "Rotating Motor.....\n\n"
ErrMsg:		.asciz "Setup didn't work... Aborting...\n"
CwMsg:		.asciz "Rotating Counter Clockwise\n"
CcwMsg:		.asciz "Rotating Clockwise\n"
EnabMsg:	.asciz "Motion Detectors Enabled\n\n\n"
//Pin that is sampled by the driver when pin goes from LOW to HIGH, motor takes one step
StepPin:	.int	3
//Pin that is sampled by the driver to determine rotation direction. When HIGH, CounterClockWise
DirPin:		.int	2
//PIR input that will cause motor to rotate CCW. When Pin is HIGH, then the DirPin is HIGH
CcwPIR:		.int	28
//PIR input that will cause motor to rotate CW. When Pin is HIGH, then the DirPin is LOW
CwPIR:		.int	29
//PIR input that will cause motor to stop rotating.
CentPIR:	.int	26
//Delay for each step of motor, if too little delay, driver won't recognize value change
delayStep_Ms:	.int	1
//Delay to account for PIR inactivity period after detecting motion
delayPIR_Ms:	.int	5000

//Code Section. Below is all of the code for Triclops logic
.section	.text
	.global main
//Imported functions from the wiringPi library and the C printf function
	.extern printf
	.extern wiringPiSetup 	@wiringPi setup memory addressing for GPIO
	.extern delay		@wiringPi delay function
	.extern digitalWrite	@wiringPi allows to change output pin value
	.extern pinMode		@wiringPi allows to change the pin from input to output
	.extern digitalRead	@wiringPi allows to read value of pin
//Branch that will be stepped into first
main:
	push	{ip,lr}		@push return address + dummy register for alignment
//Section for displaying intro
	ldr	r0, =Intro 	@Assigns asci string to r0
	bl	printf		@reads r0 then displays string
//Setup memory for wiringPi
	bl	wiringPiSetup	@Calls wiringPiSetup
	mov	r1,#-1		@Assigns failure value to compare to r1
	cmp	r0,r1		@Compare return of wiringPiSetup to Fail
	bne	pinSetup	@If r0 != r1, jump to initialization branch
	ldr	r0, =ErrMsg	@Else, load error message to r0 prior to printing asci string
	bl	printf		@Output the string
	b	done

//Setup pins for output
pinSetup:
	ldr	r0, =StepPin 	@Assign the memory address of StepPin
	ldr	r0, [r0]	@Load the contents of the StepPin to r0
	mov	r1, #1		@Assign constant to r1
	bl	pinMode		@PinMode(StepPin,OUTPUT)
	ldr	r0, =DirPin 	@Do the same for DirPin
	ldr	r0, [r0]
	mov	r1, #1
	bl	pinMode		@Setup DirPin as output

	b	testMotor	@Branching to label CW so we can make the motor rotate

//Motor will rotate on revolution in clockwise direction
//For loop that goes to 800 steps
testMotor:
	ldr	r0, =Rotate
	bl	printf
	ldr	r0, =DirPin
	ldr	r0,[r0]
	mov	r1, #1		@Prepare r1 with LOW prior to writing to DirPin
	bl 	digitalWrite	@Write to LOW to DirPin

	ldr	r0, =CwMsg	@Output Message that we are going to go counter clockwise
	bl	printf
	mov	r4, #0
	mov	r5, #800

	bl	loopHelper


	ldr	r0, =DirPin
	ldr	r0,[r0]
	mov	r1, #0
	bl	digitalWrite

	ldr	r0, =CcwMsg
	bl	printf
	mov	r4, #0
	mov	r5, #800

	bl	loopHelper
//branch to actual motion detection
	ldr	r0, =EnabMsg
	bl	printf
	b	motionSense
//Part of code where motion CW and CCW motion detectors trigger motor. This is an inifite loop.
motionSense:

	ldr	r0, =CwPIR
	ldr	r0, [r0]
	bl	digitalRead
	mov	r4, r0

	ldr	r0, =CcwPIR
	ldr	r0, [r0]
	bl	digitalRead
	mov	r5, r0

	cmp	r4,r5
	bllt	CCWMot
	blgt	CWMot
	b	motionSense

CCWMot:


	mov	r4, #0
	mov	r5, #800
	ldr	r0, =CcwMsg
	bl	printf
	ldr	r0, =DirPin
	ldr	r0, [r0]
	mov	r1, #0
	bl	digitalWrite

	bl	loopHelper

	b	motionSense

CWMot:


	mov	r4, #0
	mov	r5, #800
	ldr	r0, =CwMsg
	bl	printf
	ldr	r0, =DirPin
	ldr	r0, [r0]
	mov	r1, #1
	bl	digitalWrite

	bl	loopHelper

	b	motionSense
//LoopHelper was added to ensure that program counter didn't return to a point would cause a segfault
loopHelper:
	push	{r5, r6, fp, lr}
	sub	sp, sp, #8
	mov	fp, sp
	bl	countLoop
	mov	sp, fp
	pop	{r5, r6, fp, lr}
	bx	lr
//for(int r4 = 0; r4 < r5; r4++)
countLoop:
	cmp 	r4,r5		@Is r4 > r5 ?
	bxgt 	lr		@If so, then return to done... !!!FIX

	ldr	r0, =StepPin	@Assign the memory address of StepPin
	ldr	r0, [r0]	@Load the contents of the StepPin to r0
	mov	r1, #1		@Make r1 HIGH
	bl	digitalWrite	@Write HIGH to StepPin

	ldr	r0, =delayStep_Ms @Assign the delay to r0
	ldr	r0, [r0]
	bl	delay

	ldr	r0, =StepPin
	ldr	r0, [r0]
	mov	r1, #0
	bl	digitalWrite	@Write low

	ldr	r0, =delayStep_Ms
	ldr	r0, [r0]
	bl	delay

	add	r4,#1
	b	countLoop

done:
	pop {ip, pc}
