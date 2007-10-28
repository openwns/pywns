###############################################################################
# This file is part of openWNS (open Wireless Network Simulator)
# _____________________________________________________________________________
#
# Copyright (C) 2004-2007
# Chair of Communication Networks (ComNets)
# Kopernikusstr. 16, D-52074 Aachen, Germany
# phone: ++49-241-80-27910,
# fax: ++49-241-80-22242
# email: info@openwns.org
# www: http://www.openwns.org
# _____________________________________________________________________________
#
# openWNS is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License version 2 as published by the
# Free Software Foundation;
#
# openWNS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
class TableParser:
    fileName = None
    header = None
    lines = None
    firstRowContains = None
    firstRowIdName = None
    secondRowContains = None
    secondRowIdName = None
    description = None
    minimum = None
    maximum = None

    xvalues = None
    yvalues = None
    valueMap = None

    xcol = None
    ycol = None
    zcol = 2

    def __init__(self, fileName, firstRowContains = None, firstRowIdName = None,
                 secondRowContains = None, secondRowIdName = None, description = None,
                 minimum = None, maximum = None, lines = None):
        if firstRowContains is None:
            self.header = ''
            self.lines = []
            self.fileName = fileName
            infile = file(self.fileName)
            for line in infile:
                if line.startswith("%"):
                    self.header += line
                    if line.count("1st row ID"):
                        self.firstRowContains = line.split("(")[1][0]
                        self.firstRowIdName = line.split(":")[1].strip()
                    elif line.count("2nd row ID"):
                        self.secondRowContains = line.split("(")[1][0]
                        self.secondRowIdName = line.split(":")[1].strip()
                    elif line.count("Description"):
                        self.description = line.split(":")[1].strip()
                    elif line.count("Minimum"):
                        self.minimum = float(line.split(":")[1].strip())
                    elif line.count("Maximum"):
                        self.maximum = float(line.split(":")[1].strip())
                    else:
                        raise "Encountered unknown comment line in file: "+self.fileName
                else:
                    lineValues = [ float(col) for col in line.strip().split() ]
                    self.lines.append(lineValues)

            infile.close()
        else:
            self.header = ''
            self.lines = lines
            self.fileName = fileName
            self.firstRowContains = firstRowContains
            self.firstRowIdName = firstRowIdName
            self.secondRowContains = secondRowContains
            self.secondRowIdName = secondRowIdName
            self.description = description
            self.minimum = minimum
            self.maximum = maximum

        if self.firstRowContains == 'r' and self.secondRowContains == 'c':
            self.ycol=0
            self.xcol=1
        elif self.firstRowContains == 'c' and self.secondRowContains == 'r':
            self.ycol=1
            self.xcol=0
        else:
            raise "read Unknown table configuration:\n"+self.header
        # read all x values
        self.xvalues = [ v for v in set([ lineValues[self.xcol] for lineValues in self.lines ])]
        self.yvalues = [ v for v in set([ lineValues[self.ycol] for lineValues in self.lines ])]

        self.xvalues.sort()
        self.yvalues.sort()

        self.valueMap = {}
        # store measured values
        for line in self.lines:
            self.valueMap[(line[self.xcol],line[self.ycol])] = line[self.zcol]


    def getArray(self):
        valueArray = []

        lineNo = 0
        for yv in self.yvalues:
            valueArray.append([]) # create new line
            for xv in self.xvalues:
                valueArray[lineNo].append( self.valueMap[(xv,yv)] )
            lineNo +=1
        return valueArray

    def getXValues(self):
        return self.xvalues

    def getYValues(self):
        return self.yvalues

    def getRowIdName(self):
        if self.ycol==0:
            return self.firstRowIdName
        else:
            return self.secondRowIdName

    def getColumnIdName(self):
        if self.xcol==0:
            return self.firstRowIdName
        else:
            return self.secondRowIdName

    def getDescription(self):
        return self.description
