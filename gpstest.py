import time
import serial
import pynmea2



while 1:
	port = serial.Serial('COM3', 4800, timeout=0.01)
	try:
		pynmea2.parse(port.readline())
		break
	except ValueError:
		port.close()
		print 'Error! reconnecting'

# now connected
class RF103(pynmea2.NMEASentence):
    fields = (
        ('Sentence type', 'sentence'),
			# 00=GGA
			# 01=GLL
			# 02=GSA
			# 03=GSV
			# 04=RMC
			# 05=VTG
        ('Command', 'command'),
        	# 0=set
       		# 1=query 
        ('Rate', 'rate'),
        ('Checksum', 'checksum'),
        	# 0=no
        	# 1=yes
    )

msgs = []
msgs.append(RF103('PS', 'RF103', '00', '0', '1', '1')) # set GGA=1
msgs.append(RF103('PS', 'RF103', '01', '0', '0', '1')) # set GLL=0
msgs.append(RF103('PS', 'RF103', '02', '0', '1', '1')) # set GSA=1
msgs.append(RF103('PS', 'RF103', '03', '0', '5', '1')) # set GSV=5
msgs.append(RF103('PS', 'RF103', '04', '0', '0', '1')) # set RMC=0
msgs.append(RF103('PS', 'RF103', '05', '0', '1', '1')) # set VTG=1

for msg in msgs:
	data = msg.render(checksum=True, dollar=True, newline=True)
	print data
	port.write(data)

stream = pynmea2.NMEAStreamReader()

while 1:
	data = port.readline()
	if not data:
		time.sleep(0.1)
		continue
	msg = pynmea2.parse(data)
	print '%.3f %s' % (time.time(), msg)
