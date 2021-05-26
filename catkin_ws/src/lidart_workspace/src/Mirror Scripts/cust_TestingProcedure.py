#     Software Version: 1.0.0
#      
#     Copyright 2017 Optotune Switzerland AG. All Rights Reserved. Permission to use,
#     copy, modify, and distribute this software and its documentation for educational, 
#     research, and not-for-profit purposes, without fee and without a signed licensing
#     agreement, is hereby granted, provided that the above copyright notice, this paragraph 
#     and the following two paragraphs appear in all copies, modifications, and distributions.
#     Contact Optotune Switzerland AG, Bernstrasse 388, 8953 Dietikon, Switzerland for
#     commercial licensing opportunities.
#      
#     IN NO EVENT SHALL OPTOTUNE BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, 
#     OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE 
#     AND ITS DOCUMENTATION, EVEN IF OPTOTUNE HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#      
#     OPTOTUNE SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#     WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING 
#     DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". OPTOTUNE HAS NO OBLIGATION TO
#     PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#      
# =======================================================================================================



from cust_MR_FPGA.cust_boards import Scuti
import cust_MR_FPGA.cust_commands as commands

PORT = '/dev/ttyUSB0'
Scuti = Scuti(port=PORT,timeout = 0.1)
 
input("Press Enter to execute \"Start\" command ...")
Scuti.ser.write("start\r\n".encode())
print(Scuti.ser.read(4))
input("Press Enter to reset mirror ...")
Scuti.ser.write('reset\r\n'.encode())
print(Scuti.ser.read(4))
 
 
''' Test the angle commands for A and B channel individually'''
input("Press Enter set an angle of -5 degrees of channel A ...")
Scuti.ser.write('angleA = -5.0 deg\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter set an angle of +5 degrees of channel B ...")
Scuti.ser.write("angleB = +5.0 deg\r\n".encode())
print(Scuti.ser.read(4))
input("Press Enter set an angle of +5 degrees of channel A ...")
Scuti.ser.write('angleA = +5.0 deg\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter set an angle of -5 degrees of channel B ...")
Scuti.ser.write("angleB = -5.0 deg\r\n".encode())
print(Scuti.ser.read(4))
input("Press Enter to reset mirror ...")
Scuti.ser.write('reset\r\n'.encode())
print(Scuti.ser.read(4))
 
''' Test the angle commands for A and B channel simultaneously '''
input("Press Enter set an angle of -5 and +5 degrees of channel A and B ...")
Scuti.ser.write('2changle = -5deg;5deg\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter set an angle of +5 and -5 degrees of channel A and B ...")
Scuti.ser.write('2changle = +5deg;-5deg\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter to reset mirror ...")
Scuti.ser.write('reset\r\n'.encode())
print(Scuti.ser.read(4))
 
''' Test the current commands for A and B channel individually'''
input("Press Enter set a current of -70 mA channel A ...")
Scuti.ser.write('currenta = -70.0 mA\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter set a current of +70 mA channel B ...")
Scuti.ser.write('currentb = +70.0 mA\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter set a current of +70 mA channel A ...")
Scuti.ser.write('currenta = +70.0 mA\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter set a current of -70 mA channel B ...")
Scuti.ser.write('currentb = -70.0 mA\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter to reset mirror ...")
Scuti.ser.write('reset\r\n'.encode())
print(Scuti.ser.read(4))
 
''' Test the PIDOF commands for A and B channel'''
input("Press Enter set a PID value of -0.3 in channel A ...")
Scuti.ser.write('pidofa=-0.3\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter set a PID value of 0.3 in channel B ...")
Scuti.ser.write('pidofb=+0.3\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter set a PID value of 0.3 in channel A ...")
Scuti.ser.write('pidofa=0.3\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter set a PID value of -0.3 in channel B ...")
Scuti.ser.write('pidofb=-0.3\r\n'.encode())
print(Scuti.ser.read(4))
input("Press Enter to reset mirror ...")
Scuti.ser.write('reset\r\n'.encode())
print(Scuti.ser.read(4))
 
 
'''Test Pro Mode
Drive the mirror with a waveform'''
Scuti.initialize(set_factory_defaults = False)
Scuti.getPIDvals()
Scuti.sendCmd(commands.ControlMode(Mode = 'PIDOF'))
Scuti.sendCmd(commands.SetOF(Channel = 'A', Value = -0.08,reply_enabled=True))
Scuti.sendCmd(commands.SetOF(Channel = 'B', Value = -0.08,reply_enabled=True))
Scuti.sendCmd(commands.EnableUnit(Enable = True,Unit = 'Scaling'))
Scuti.sendCmd(commands.SetScaling(Channel = 'A', Value = 0.4))
Scuti.sendCmd(commands.SetScaling(Channel = 'B', Value = 0.4))
Scuti.sendCmd(commands.SetWaveform(Channel = 'A',Waveform = 'Sine'))
Scuti.sendCmd(commands.SetWaveform(Channel = 'B',Waveform = 'Sine'))
Scuti.sendCmd(commands.SetWFFrequency(Channel = 'A',Value = 1))    
Scuti.sendCmd(commands.SetWFFrequency(Channel = 'B',Value = 1))
Scuti.sendCmd(commands.SetRelativePhase(Value = 90))
Scuti.sendCmd(commands.SignalManager(Unit = 'WF'))
  
input("Press Enter to exit communication and reset the mirror position...")
Scuti.close()
