;By: CMDR AweBob at https://github.com/AweBob/EliteDangerous_Tools
;Lines to change: line8 for hotkey , line12 for opengalaxymap

SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
SetTitleMatchMode 2



$o:: ;Leave the percent sign and change to whatever you want your hotkey to be
IfWinExist, Elite - Dangerous (CLIENT)
{
	WinActivate
	Send, k ;change to whatever key it is set to in .binds file, I assume this works with joystick buttons
	Loop, 50 {
		try {
			ImageSearch, OutputVarX, OutputVarY, X1, Y1, X2, Y2, menuBar.png
			break
		} catch e {
			return
		}
	}
	if ErrorLevel != 0 {
		return	
	} 
	MouseClick, 
	
}
return



Numpad8::
ExitApp
