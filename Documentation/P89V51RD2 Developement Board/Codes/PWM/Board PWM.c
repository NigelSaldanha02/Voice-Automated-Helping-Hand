/**************************************************************************************************************
		Platform: P89V51RD2 Development Board.
		PWM using PCA (Timers and Counters)
		Written by: Kunal Joshi, NEX Robotics Pvt. Ltd.
		Edited By: Sachitanand Malewar, NEX Robotics Pvt. Ltd.
		Last Modification: 2010-23-04
		This programme is used to generate Pulse Width Modulation (PWM) using PCA
        Note: Only PWM 0 and PWM 1 channels are used 
        Compiled with: uVision3 V4.02; C Compiler: C51.Exe, V9.01
**************************************************************************************************************/			  

/********************************************************************************

   Copyright (c) 2010, NEX Robotics Pvt. Ltd.                       -*- c -*-
   All rights reserved.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:

   * Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.

   * Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in
     the documentation and/or other materials provided with the
     distribution.

   * Neither the name of the copyright holders nor the names of
     contributors may be used to endorse or promote products derived
     from this software without specific prior written permission.

   * Source code can be used for academic purpose. 
	 For commercial use permission form the author needs to be taken.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
  POSSIBILITY OF SUCH DAMAGE. 

  Pin Configuration:-
  Load count in PWM_0 and PWM_1.
  check O/P on PORT PIN 1.3 and PORT PIN 1.4
  
  Software released under Creative Commence cc by-nc-sa licence.
  For legal information refer to: 
  http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode

********************************************************************************/

#include <intrins.h>
#include "p89v51rx2.h"

void PWM_0(unsigned char cnt0)
{
CCAP0H=cnt0;
}

/*********************************************************************************

void PWM_n(unsigned char cntn)
{
CCAPnH=cntn;     //n=0,1
}

*********************************************************************************/

void PWM_1(unsigned char cnt1)
{
CCAP1H=cnt1;
}

//initialise programmable counter array module to generate pwm
//The CCAPnH register holds the reload value. CCAPnL register increments,and is loaded with this value everytime it overflows
void pca_init(void)
{
 CMOD=0x80;    //80 sets PCA counter to run at Fosc/6; 
 CCON=0x40;    //start PCA counter
 						
 CCAP0L=0x00;   
 CCAP0H=0xFF;  //Left motor duty cycle register
  
 CCAP1L=0x00;				  
 CCAP1H=0xFF;  //Right motor duty cycle register

 CCAPM0=0x42;  //enable PWM mode and ECOM bits for PWM_0
 CCAPM1=0x42;  //enable PWM mode and ECOM bits for PWM_1
}

void main()
{
pca_init();
PWM_0(0x40);   //0x00 will give full (100% duty cycle) , while 0xFF will give zero (0% duty cycle). 		
PWM_1(0x60);   //0x00 will give full (100% duty cycle) , while 0xFF will give zero (0% duty cycle). 
while(1);
}

