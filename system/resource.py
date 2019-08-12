import os
import time
import dbModule
import psutil


def getSystemResource():
    cpu_usage = psutil.cpu_percent()

    mem_usage = psutil.virtual_memory()

    disk_usage = psutil.disk_usage('/')

    print(cpu_usage)
    print(mem_usage.percent)
    print(disk_usage.percent)

    db_class = dbModule.Mysql()
    remove_sql = """delete from system_info order by rdate limit 1"""
    db_class.cursor.execute(remove_sql)

    sql = """INSERT INTO system_info (cpu_usage, memory_usage, disk_usage, rdate)
                VALUES (%s, %s, %s, now())
                ON DUPLICATE KEY UPDATE cpu_usage = values(cpu_usage), 
                memory_usage = values(memory_usage),
                disk_usage = values(disk_usage)"""

    db_class.cursor.execute(sql, (cpu_usage, mem_usage.percent, disk_usage.percent))
    db_class.commit()



getSystemResource()