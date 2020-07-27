from django.shortcuts import render
import numpy as np
import sounddevice as sd

def filter1(power,data) :
	fs = 44100
	print("playing")
	sd.playrec(data , samplerate = fs * power ,channels = 1 )
	sd.wait()


def filter2(power, data) :
	fs = 44100
	output_WAV = np.zeros(len(data))
	circular_buffer_length = 256
	circ_buf = np.zeros(circular_buffer_length)
	write_index = 0
	read_index = 0
	write_period = 1.0 / fs
	read_period = write_period * power
	for i in range(0, len(data)):
		# Write to the circular buffer.
		# To reduce the audible clicks when the two pointers cross we average the
		# existing value with the new value.
		circ_buf[write_index] = (circ_buf[write_index] + data[i]) / 2
		# circ_buf[write_index] = input_WAV[i]
		if write_index == circular_buffer_length - 1:
			write_index = 0
		else:
			write_index += 1

		# Calc the next read index on the circular buffer.
		t = i * write_period
		ri = t / read_period
		read_index = int(ri % circular_buffer_length)

		# Read from the circular buffer with different pitch.
		output_WAV[i] = circ_buf[read_index]
	sd.playrec(output_WAV, samplerate=fs, channels=1)
	sd.wait()



def index(request):
    if request.method == 'POST':
        duration = int(request.POST.get('duration'))
        if request.POST.get('filter'):
            fs = 44100
            myRec = sd.rec(duration * fs, samplerate=fs, channels=1)
            sd.wait()

            power = float(request.POST.get('freq'))

            if request.POST.get('filter') == 'treble':
                filter1(power, myRec)
            if request.POST.get('filter') == 'bass':
                filter2(power, myRec)

    return render(request, 'main.html')
