import os
import cx_Oracle
import xml.dom.minidom
import re


src_sql = "SELECT NODE_ID, NODE_NAME, FUN_PATH  FROM ST_TREE_E_CSPAFUNM WHERE PARENT_NODE_ID = "

def findChildredNodes(connect, parentNodeId, resultList):
    cursor = connect.cursor()
    sql = src_sql + "'" + parentNodeId + "'"
    # sql = "SELECT NODE_ID, NODE_NAME, FUN_PATH  FROM ST_TREE_E_CSPAFUNM WHERE PARENT_NODE_ID = 'JYFX'"
    res = cursor.execute(sql)
    # print(sql)
    rows = res.fetchall()
    if res.rowcount == 0:
        return
    for ele in rows:
        resultList.append(ele)
        findChildredNodes(connect, ele[0], resultList)
    cursor.close()


def findAllReportPath(nodeId):

    connect = cx_Oracle.connect('dtbl_dev2/dtbl_dev2@10.97.85.109/orcl')
    reslist = []
    findChildredNodes(connect, nodeId, reslist)

    filteredList = []
    pathlist = []
    filteredJsList = []

    jsmap = {}
    for ele in reslist:
        if ele[2] != None:
            filteredList.append([ele[1], ele[2][ele[2].rindex('/') + 1: -5] + '.js'])
            filteredJsList.append(ele[2][ele[2].rindex('/') + 1: -5] + '.js')
            jsmap[ele[2][ele[2].rindex('/') + 1: -5] + '.js'] = ele[1]
            if not ele[2].startswith('/report') and not ele[2].startswith('/business'):
             pathlist.append(ele[2])
    # print(filteredList)
    # print(pathlist)
    return {'all':filteredList, 'js':filteredJsList, 'map':jsmap}
    # return filteredList
# print(dir(res))



# print ('a/b/c'.startswith('/'))
startdir = 'F:\\dev-vteam\\dev-code\\dtbl-code3\\com.vteam.scfs.report.resource\\META-INF\\rptdesign'

def searchJsContent():
    reportdir = 'F:\\dev-vteam\\dev-code\\dtbl-code3\\com.vteam.scfs.report.web\\WebContent'
    bussnessdir = 'F:\\dev-vteam\\dev-code\\dtbl-code3\\com.vteam.scfs.general.business.web\\WebContent'
    reportdirs = [reportdir, bussnessdir]

    cnt_map = findAllReportPath('JYFX')
    rptnamelist = {}
    for rptdir in reportdirs:
        for dir, dirnames, filenames in os.walk(rptdir):
            for filename in filenames:
                if filename in cnt_map['map']:
                    searchRptdesign(os.path.join(dir, filename), rptnamelist, cnt_map['map'][filename])


    for dir, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            if filename in rptnamelist:
                # print(os.path.join(dir, filename))
                searchEventInXml(os.path.join(dir, filename), rptnamelist[filename])



def searchRptdesign(path, rptlist, fun_path):
    strfile = open(path, 'r', 10240, 'UTF-8')
    str = strfile.read()
    for ele in re.findall('ReportName=(.+)\.rptdesign', str):
        rptlist[ele + '.rptdesign'] = fun_path


#查找XML里的历程
def searchEventInXml(filePath, fun_path):
    dom = xml.dom.minidom.parse(filePath)
    root = dom.documentElement
    file = open(filePath, 'r', 10240, 'UTF-8')
    str = file.read()
    res = re.search('VLOA\w{1,20}E|VBTX\w{1,20}E|VPRI\w{1,20}E', str, re.IGNORECASE)
    if res != None:
        print(res)
        print(filePath)
        print(fun_path)
        print('------------------------------')



searchJsContent()


# findAllReportPath('JYFX')

# for dir, dirnames, filenames in os.walk(startdir):
#     for filename in filenames:
#         print(filename)


