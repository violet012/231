import stdaudio
import stdarray
import random
import math

def bridge(brown_noise, b0, b1, variance, scale):
    if b0+1==b1: 
        return
    else:
        bm=(b0+b1)//2
        mnumber=(brown_noise[b0]+brown_noise[b1])/2.0
        value=random.gauss(0.0, math.sqrt(variance))
        brown_noise[bm]=value+mnumber
        bridge(brown_noise, b0, bm, variance/scale, scale)
        bridge(brown_noise, bm, b1, variance/scale, scale)

#generate an array of random numbers between -0.25 and 0.25 (white noise)
def white(white_noise, w0, w1, amplitude):
    for i in range(len(white_noise)):
        white_noise[i]=random.uniform(-amplitude, amplitude)

#the final wave, put together array
def final(final_array):
    for index in range(len(brown_noise)):
        time=(1/44100)*index
        sine_function=math.sin(math.pi*frequency*time)**6
        final_array[index]=((1-sine_function)*brown_noise[index])+(sine_function*white_noise[index])

length_of_array=882000
last=length_of_array-1

#time is the sample duration (1/44100) multiplied by the index 
#44100 sample/second

#the final array should have the same length as the white noise and the brown noise

brown_noise=stdarray.create1D(length_of_array, 0.0)
white_noise=stdarray.create1D(length_of_array, 0.0)
final_array=stdarray.create1D(length_of_array, 0.0)

b0=0
b1=last
w0=0
w1=last

hurst_exp=0.5
variance=0.05
scale=2.0**(2.0*hurst_exp)
frequency=0.25
amplitude=0.25

white(white_noise, w0, w1, amplitude)

#separate it into 10 pieces (each one is 88200 length long)
bridge(brown_noise, 0, 88200, variance, scale)
bridge(brown_noise, 88200, 176400, variance, scale)
bridge(brown_noise, 176400, 264600, variance, scale)
bridge(brown_noise, 264600, 352800, variance, scale)
bridge(brown_noise, 352800, 441000, variance, scale)
bridge(brown_noise, 441000, 529200, variance, scale)
bridge(brown_noise, 529200, 617400, variance, scale)
bridge(brown_noise, 617400, 705600, variance, scale)
bridge(brown_noise, 705600, 793800, variance, scale)
bridge(brown_noise, 793800, 881999, variance, scale)
#check and makesure the values are right

final(final_array)


stdaudio.playSamples(final_array)
stdaudio.wait()