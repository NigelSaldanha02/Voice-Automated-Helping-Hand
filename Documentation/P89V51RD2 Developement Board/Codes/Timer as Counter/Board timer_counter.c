/**************************************************************************************************************
		Platform: P89V51RD2 Development Board.
	    Timer as external event counter.
		Written by: Kunal Joshi, NEX Robotics Pvt. Ltd.
		Edited By: Sachitanand Malewar, NEX Robotics Pvt. Ltd.
		Last Modification: 2010-23-04
		In this program Timer 0 is used as counter.
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

  Pin Function:-
  connect  P3.4 (T0) to pulse generated circuit(555 in Astable mode).
  connect Bar graph to Port 1 for checking O/p.
  Note:- you can used timer 1 also as counter.

  Software released under Creative Commence cc by-nc-sa licence.
  For legal information refer to: 
  http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode

********************************************************************************/

#include <intrins.h>
#include "p89v51rx2.H"

//initializing timer/counter0 as counter in mode 2
void  timer0_setup(void)   
{
 TMOD=0x06; // Timer 1 in 8 bit external counter mode
 TH0=0x00;  // reset counter value to 0       
 TL0=0x00;  // reset counter value to 0  
}

void main(void)
{
 unsigned char count;
 unsigned char A=0;
 timer0_setup();		     //initializing timer/counter0
 P1=0x00;
 while(1)			         //loop continuously
 {
 TR0=1;
 if(A!=TL0)		            //TL0 contain count 
 {                
  count=TL0;        		 //count 
  P1=count;					//count on PORT 1
 }
  A=TL0;
 }
}

