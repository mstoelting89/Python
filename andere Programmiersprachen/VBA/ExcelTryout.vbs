Option Explicit

ExcelTryout


Sub ExcelTryout()
    Dim objExcelApp 'As Object
    Dim objWorkbook 'As Workbook
    Dim objWorksheet 'As Worksheet
    
    Dim strFilePath 'As String
    Dim strSheetName 'As String
    
    ' ======================================================================================
    ' Init
    ' ======================================================================================
    strFilePath = "C:\Users\mstoelting\Documents\Corlies.xlsx"
    strSheetName = "CorliesWS"
        
    ' ======================================================================================
    ' Open the Excel-File (the Workbook) and set the Worksheet
    ' ======================================================================================
    Set objExcelApp = CreateObject("Excel.Application")
    objExcelApp.Visible = False
    Set objWorkbook = objExcelApp.Workbooks.Open(strFilePath)
    Set objWorksheet = objExcelApp.Sheets(strSheetName)
    
    ' ======================================================================================
    ' Lesen und ausgeben
    ' ======================================================================================
    MsgBox objWorksheet.Cells(3, 2), , "Effe zien"
    MsgBox "Last row is: " & GetLastRow(objWorksheet) & vbCrlf & _
		   "Last column of row 7 is: " & GetLastColumn(objWorksheet, 7)
       
    ' ======================================================================================
    ' Close
    ' ======================================================================================
    objWorkbook.Close
    objExcelApp.Quit
    
    ' ======================================================================================
    ' Clean up objects
    ' ======================================================================================
    If Not (objWorksheet Is Nothing) Then Set objWorksheet = Nothing
    If Not (objWorkbook Is Nothing) Then Set objWorkbook = Nothing
    If Not (objExcelApp Is Nothing) Then Set objExcelApp = Nothing
End Sub
Function GetLastRow(ByRef pobjSheet) 'As Long
    Dim ColNbr 'As Integer
    Dim LastRowInCol, Highest 'As Long
    
    Highest = 0
    ' ======================================================================================
    '
    '
    ' REMARK: Still based on older Excel versions, which can contain only 256 columns
    '
    '
    ' ======================================================================================
    For ColNbr = 1 To 256
'        LastRowInCol = pobjSheet.Range(Cells(65536, ColNbr), Cells(65536, ColNbr)).End(xlUp).Row
        LastRowInCol = pobjSheet.Cells(65536, ColNbr).End(-4162).Row
        If LastRowInCol > Highest Then
            Highest = LastRowInCol
        End If
    Next

    GetLastRow = Highest
End Function
Function GetLastColumn(ByRef pobjSheet, plngRow) 'As Integer
    Dim strFileExtension 'As String
    
    ' ======================================================================================
    ' Init
    ' ======================================================================================
    strFileExtension = UCase(Mid(pobjSheet.Parent.Name, InStrRev(pobjSheet.Parent.Name, ".") + 1))
    
    ' ======================================================================================
    ' Depending on the Excel version, .....
    ' ======================================================================================
    If Len(strFileExtension) = 3 Then ' "XLS", "XLM", "XLA" etc.; old Ecxel version
        GetLastColumn = pobjSheet.Cells(plngRow, 256).End(-4159).Column
    Else
        GetLastColumn = pobjSheet.Cells(plngRow, pobjSheet.Columns.Count).End(-4159).Column
    End If
End Function
