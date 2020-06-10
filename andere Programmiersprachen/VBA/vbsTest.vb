Option Explicit

Sub testProgramm()
	dim objExcelApp 
	dim objWorkbook 
	dim objWorksheet
	
	dim strCurrentPath
	dim strSheetName
	
	strCurrentPath = "C:\Users\mstoelting\Documents\VBA"
	strSheetName = "Tabelle1"
	
	Set objExcelApp = CreateObject("Excel.Application")
    objExcelApp.Visible = False
    Set objWorkbook = objExcelApp.Workbooks.Open(strFilePath)
    Set objWorksheet = objExcelApp.Sheets(strSheetName)
	
	
End Sub

testProgramm