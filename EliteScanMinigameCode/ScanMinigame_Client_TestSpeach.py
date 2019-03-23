import win32com.client as wincl
tts = wincl.Dispatch("SAPI.SpVoice") #Will crash here for nonwindows users
while True :
    tts.speak( input( 'What do you want to hear? - ' ) )
    print('If youve heard nothing tts isnt working' + '\n')
    