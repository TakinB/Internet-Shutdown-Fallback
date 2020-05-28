import textwrap
maxChar = 140

# define string
sampleString = "Hundreds of thousands of protestors have returned to the streets in Sudan's capital city Khartoum to demand an end to military rule. Security forces have fired tear gas to disperse the crowds. Also on the programme: We speak with a North Korean defector about US President Donald Trump crossing into North Korea and we find out why a Chinese poet has been honoured by a town in England."

textSplitter = textwrap.wrap(sampleString, maxChar)

for i in range(len(textSplitter)):
    ##  send textSplitter[i]
