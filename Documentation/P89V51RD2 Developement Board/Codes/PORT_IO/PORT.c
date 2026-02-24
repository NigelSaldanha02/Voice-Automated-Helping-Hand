							   /**************************************************************************************************
		Platform:P89V51RD2 Development Board.
		IO Operations
		Written by: Kunal Joshi, NEX Robotics Pvt. Ltd.
		Edited By: Sachitanand Malewar, NEX Robotics Pvt. Ltd.
		Last Modification: 2010-23-04
		This program turns the 'Port 1' and 'Port 2 pin 0' ON and OFF with a delay in between
    	Compiled with: uVision3 V4.02; C Compiler: C51.Exe, V9.01
**************************************************************************************************/

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
  connect PORT 1 To LED BAR Graph to check O/p.
  connect  P2.0  to LED tocheck O/P.
  add your delay in delay_ms call function.

  Software released under Creative Commence cc by-nc-sa licence.
  For legal information refer to: 
  http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode

********************************************************************************/

#include <intrins.h>
#include "p89v51rx2.h"

sbit Port2_0=P2^0;

// function for giving a delay of ms milliseconds
void delay_ms(unsigned int ms)
{
 unsigned int i,j;
 
 for(i=0;i<ms;i++)
 for(j=0;j<55;j++);
}

void main (void)
{
 while(1)
 {
  P1=0x00; 	  // Active low to port 1
  Port2_0=0;	  // Active low to Port 2 Pin 0
  delay_ms(100);  //  delay of 100 miliseconds
  P1=0xFF;	  // Active high to port 1
  Port2_0=1;	  // Active high to Port 2 Pin 0
  delay_ms(100);  //delay of 100 miliseconds
 }
}