import xlrd

# Excel to CSV converter
# simplified from: http://juno-devel.ovh.org/Public/Code/Python/xls2csv.0.4.py
def readXLS(wSheet):
    for numRow in xrange(wSheet.nrows):
        outlist = []
        for numCol in xrange(wSheet.ncols):
            cellType = wSheet.cell_type(numRow,numCol)
            cellValue = wSheet.cell_value(numRow,numCol)

            if((cellType == xlrd.XL_CELL_BOOLEAN) or (cellType == xlrd.XL_CELL_NUMBER)):
                try:
                    outlist.append(str(int(cellValue)))
                except: 
                    try:
                        outlist.append(str(float(cellValue)))
                    except:
                        outlist.append(str(cellValue))
            elif(cellType == xlrd.XL_CELL_NUMBER ):
                outlist.append(cellValue)
            elif(cellType == xlrd.XL_CELL_DATE ):
                # trying to handle dates - maybe buggy at this time !
                # by default, datemode is 1900-based
                datemode = 0 # 1900-based
                # datemode = 1 # 1904-based
                tp = xlrd.xldate_as_tuple(cellValue,0)
                mydate = datetime.datetime( tp[0], tp[1], tp[2], tp[3], tp[4], tp[5] )
                # return isoformat (may be improved in the future)
                outlist.append(mydate.isoformat())
            else:
                outlist.append(cellValue)
        yield outlist
            
            
def getXLSdata(infile,numsheet=0):
    separator = "|"
    
    # Open input file
    book = xlrd.open_workbook(filename=infile)

    nSheets = book.nsheets
    if(numsheet >= nSheets or numsheet < 0):
        raise ValueError

    # Select working sheet
    wSheet = book.sheet_by_index(numsheet)

    # Handle negative indexes for removing rows and colums

    for data in readXLS(wSheet):
        yield data
        # result_file.write((separator).join(data))
        # result_file.write("\n")

    # result_file.close()
