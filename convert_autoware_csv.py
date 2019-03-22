import csv

columns = ['LINKID', 'LANETYPE', 'LANECODE', 'BARRIER', 'LNO', 'CODE', 'DATE', 'REMARK', 'HDUFID', 'POINT_X', 'POINT_Y', 'POINT_Z', 'POINT_M']
linkids = []
lanetypes = []
lanecodes = []
barriers = []
lnos = []
codes = []
dates = []
hdufids = []
point_xyzms = []
point_sizes = []

with open('UTM52N.csv', newline='', encoding='utf-8', errors='ignore') as csvfile:
    csvreader = csv.reader(csvfile)
    csvreader.__next__()
    for row in csvreader:
        #POINT_XYZM section
        row0 = row[0].split('(')[0]
        if row0 == "LINESTRING ZM ":
            wkt = row[0].split('(')[1].split(')')[0].split(',')
        else:
            wkt = row[0].split('((')[1].split('))')[0].split('),(')
            wkt =  " ".join(wkt).replace('0 ', '0,').split(',')

        point_xyzms.append(wkt)
        point_sizes.append(len(wkt))

        #other sections
        if row[1]:
            linkids.append(row[1])
        elif row[2]:
            linkids.append(row[2])
        else:
            linkids.append('')
        lanetypes.append(row[3])
        lanecodes.append(row[4])
        barriers.append(row[5])
        lnos.append(row[6])
        codes.append(row[7])
        dates.append(row[8])
        hdufids.append(row[10])

with open('UTM52N_converted.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(columns)
    
    for lno in lnos:
        linkid = linkids.pop(0)
        lanetype = lanetypes.pop(0)
        lanecode = lanecodes.pop(0)
        barrier = barriers.pop(0)
        code = codes.pop(0)
        date = dates.pop(0)
        hdufid = hdufids.pop(0)

        for point_xyzm in point_xyzms.pop(0):
            xyzm = point_xyzm.split(' ')
            point_x = xyzm[0]
            point_y = xyzm[1]
            point_z = xyzm[2]
            point_m = ''
            newrows = [linkid, lanetype, lanecode, barrier, lno, code, date, '', hdufid, point_x, point_y, point_z, point_m]
            csvwriter.writerow(newrows)

