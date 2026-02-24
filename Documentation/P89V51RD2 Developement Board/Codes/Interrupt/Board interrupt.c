/**************************************************************************************************************
		Platform:P89V51RD2 Development Board.
		Use of External hardware 
		Written by: Kunal Joshi, NEX Robotics Pvt. Ltd.
		Edited By: Sachitanand Malewar, NEX Robotics Pvt. Ltd.
		Last Modification: 2010-23-04
		This program demonstrates the use of external hardware interrupt
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
  connect PORT1 To LED BAR Graph to check O/p.
  connect  P3.3 (INT 1) to interrupt generated circuit.


  Software released under Creative Commence cc by-nc-sa licence.
  For legal information refer to: 
  http://creativecommons.org/licenses/by-nc-sa/3.0/legalcode

********************************************************************************/


#include <intrins.h>
#include "p89v51rx2.H"

//initialization routine for Interrupt 1 setup.

void int1_setup() //Initalisation of the Int 1 should be done in the same sequence as given in this function.
{
 IEN0 = 0x84;      //External Interrupt 1 Enable and Global Interrupt Enable. 
 P3 = 0x08;        //set P3.3 (INT 1) as input port.
}


//ISR for external Interrupt 1

void int1_isr(void)interrupt 2     //ISR Routine for External Interrupt 1(INT 1).
{
 P1=0xF0; 	                      // Active low to port 1
 IE1=0;                           // Clearing IE1 flag to 0.
}                   
 		            	
void main()
{ 
 int1_setup();      //external linterrupt 1 initialization setup.
 while(1)
 {
  P1=0x0F;          // Active High to port 1
 }
}//main ends                

