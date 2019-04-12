# 比较不通数据库的字段
# 同表同名，长度不通，需要测试

import cx_Oracle

#定义获取数据库结构函数
def getTableStructure(location, owner) :
    sql = """SELECT
a.table_name 表名,
a.column_name 字段名,
a.data_type 字段类型,
a.字段长度,
a.字段精度
from
(select a.owner,a.table_name,b.column_name,b.data_type,case when b.data_precision is null then b.data_length else data_precision end 字段长度,data_scale 字段精度,
decode(nullable,'Y','√','N','×') 是否为空,c.created 创建日期,c.last_ddl_time 最后修改日期 
from all_tables a,all_tab_columns b,all_objects c 
where a.table_name=b.table_name and a.owner=b.owner
and a.owner=c.owner
and a.table_name=c.object_name
and a.owner='"""+ owner +"""' 
and c.object_type='TABLE') a
left join 
(select a.owner,a.table_name,a.column_name,a.constraint_name from user_cons_columns a, user_constraints b 
where a.constraint_name = b.constraint_name and b.constraint_type = 'P') d
on a.owner=d.owner and a.table_name=d.table_name and a.column_name=d.column_name
order by a.table_name,a.column_name, a.data_type"""


    conn = cx_Oracle.connect(location)
    cursor = conn.cursor()
    result = cursor.execute(sql)
    list = []
    for ele in result:
        list.append(ele)
    cursor.close()
    conn.close()
    return list

#比较数据库结构函数
def compareTowDatabase() :
    list2 = getTableStructure("dtbl_dev2/dtbl_dev2@10.97.85.109/orcl", 'DTBL_DEV2')
    list1 = getTableStructure("DTBL_PRD/dTbL@10.160.1.46:1521/dtbl", 'DTBL_PRD')

    count = 0
    for i in range(0, len(list2)):

        list1Index = -1;
        isCompleteExist = False
        isPartExist = False
        for j in range(0, len(list1)):
            if (list1[j][0] == list2[i][0] and list1[j][1] == list2[i][1]):
                if list1[j][2] == list2[i][2]:
                    isCompleteExist = True
                else:
                    isPartExist = True
                list1Index = j
                break
        if (isCompleteExist or isPartExist):
            list1.pop(list1Index)

        else:
            print(list2[i])
            print(list1[list1Index])
            print('*************')
            count += 1

    print(count)

#执行函数
compareTowDatabase()