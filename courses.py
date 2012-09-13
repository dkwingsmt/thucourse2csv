#!/usr/bin/python2
# -*- coding: utf-8 -*-

#    © Copyright 2012 MOU Tong (DKWings).
#
#    This file is part of thucourse2csv.
#
#    Thucourse2csv is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Thucourse2csv is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with thucourse2csv.  If not, see <http://www.gnu.org/licenses/>.

import xlrd
import re
import timebasic

tgt_file = '/home/dkwings/thu-2-2/courses.xls'

def GetNormalClassTime(cls_num):
    '''Turn [1,6] to ((Start_Hr, Start_Min), (End_Hr, End_Min))'''
    norm_cls_time_tst = (
        ((8,  00), (9,  35)),
        ((9,  50), (11, 25)),
        ((13, 30), (15, 05)),
        ((15, 20), (16, 55)),
        ((17, 10), (18, 45)),
        ((19, 20), (20, 55)),
        )
    return norm_cls_time_tst[cls_num - 1]

class Course(object):
    '''One set of course_info, and has the data of detail lists
Contains:
    name        - A string, the name of the course
    teacher     - A string 
    catagory    - A string, mandatory or not
    wday        - A int of 1,...,7, indicating Monday to Sunday
    time        - A CourseTime instance, indicating the time of a day
    week        - A list of int in [1, 16], indicating the actual week
    place       - A string, the real place'''
    def __init__(self):
        self.name = u''
        self.teacher = u''
        self.catagory = u''
        self.wday = 0
        self.time = None
        self.week = ()
        self.place = u''

    def Assign(self, item, content):
        '''Equals to self.item = content.
If item doesn't exist, will raise KeyError'''
        if item in self.__dict__:
            self.__dict__[item] = content
        else:
            # raise KeyError
            if self.__dict__[item]:
                pass

    def ToStr(self):
        wday_name = (u'周一', u'周二', u'周三', 
                u'周四', u'周五', u'周六', u'周日')
        str_lst = []
        if self.name:
            str_lst.append(self.name)
        if self.teacher:
            str_lst.append(u'(%s)' % self.teacher)
        if self.catagory:
            str_lst.append(u'[%s]' % self.catagory)
        str_lst.append(u' ')
        if self.wday:
            str_lst.append(u'每%s' % wday_name[self.wday - 1])
        if self.time:
            t = self.time
            str_lst.append(u'%d:%02d-%d:%02d' % (t[0][0], t[0][1], t[1][0], t[1][1]))
        if self.place:
            str_lst.append(u'在%s' % self.place)
        if self.week:
            str_lst.append(u' 第')
            wk_str_lst = []
            for wk in self.week:
                wk_str_lst.append(unicode(wk))
            str_lst.append(u','.join(wk_str_lst))
            str_lst.append(u'周')
        return u''.join(str_lst)            


def TryTime(src_str):
    '''Try to recognize as time, return time((Start_Hr, Start_Min), (End_Hr, End_Min))'''
    pattern = u'时间(\d+):(\d+)-(\d+):(\d+)'
    regex_res = re.match(pattern, src_str)
    if regex_res:
        gr = regex_res.groups()
        return ( (int(gr[0]), int(gr[1]) ), ( int(gr[2]), int(gr[3]) )  )

def TryWeek(src_str):
    '''Try to recognize as week info'''
    alias_lst = (
        (u'全周', range(1, 17)),
        (u'前八周', range(1, 9)),
        (u'后八周', range(9, 17)),
        (u'单周', range(1, 17, 2)),
        (u'双周', range(2, 17, 2)),
        )
    for alias, ans in alias_lst:
        if alias == src_str:
            return ans
    # now try to recognize u'第1, 3-4, 5周'
    # the '?' avoid error in str like u'第1周周'(sometimes happens)
    pattern = u'^(第)?(.*?)周'
    regex_res = re.match(pattern, src_str)
    if not regex_res:
        return

    detail_str = regex_res.groups()[1]
    week_str_lst = detail_str.split(u',')
    week_lst = []
    for week_str in week_str_lst:
        # like u'第1周'
        try:
            week_lst.append(int(week_str))
            continue
        except ValueError:
            pass
        # like u'第1-2周'
        week_split_lst = week_str.split(u'-')
        if len(week_split_lst) == 2:
            try:
                start_week = int(week_split_lst[0])
                end_week = int(week_split_lst[1])
            except ValueError:
                pass
            else:
                week_lst.extend(range(start_week, end_week + 1))
                continue
        print u'### What\'s this? "%s"' % week_str
    return week_lst

def TryCatagory(src_str):
    alias_lst = (u'必修', u'限选', u'任选')
    for alias in alias_lst:
        if alias in src_str:
            return alias

def TryPlace(src_str):
    place_lst = (
            u'一教', u'二教', u'三教', u'四教', u'五教', u'六教',
            u'中央主楼', u'西主楼', u'东主楼', u'艺教中心', u'综合体育馆', 
            u'游泳馆', u'明理楼', u'技科楼', u'工物馆', u'东区体育活动中心', 
            u'主楼报告厅', u'美院', u'建筑馆报告厅', u'综合馆', u'伟伦楼',
            u'精仪系馆', u'FIT大楼', u'FIT楼', u'东区棒垒球场'
            )
    for place in place_lst:
        if place in src_str:
            return src_str

def TryPlaceIcon(src_str):
    place_icon_lst = (
            u'楼', u'教', u'中心', u'馆', u'中心',
            )
    for place_icon in place_icon_lst:
        if place_icon in src_str:
            return src_str

def AnalyseCrsInfo(name, wday, cls_num, crs_info_str):
    '''return Course instance'''
    crs = Course()
    # Apply default settings
    crs.Assign('name', name)
    crs.Assign('wday', wday)
    if cls_num > 0 and cls_num < 7:
        crs.Assign('time', GetNormalClassTime(cls_num))
        
    str_lst = crs_info_str.split(u'；')
    # It's somewhere to put suspect place and teacher name.
    undefined_str = []
    methods_items = (
            (TryCatagory, 'catagory'),
            (TryTime, 'time'),
            (TryWeek, 'week'),
            )
    for info_str in str_lst:
        found = False
        for TryMethod, item in methods_items:
            try_res = TryMethod(info_str)
            if try_res != None:
                crs.Assign(item, try_res)
                found = True
                break
        if not found:
            undefined_str.append(info_str)
    if not undefined_str:
        return crs

    # Time to recognize places and teacher name
    # 1) If the place matches any of the aliases, it is a place; the rest is teacher name
    # 2) If len(undefined_str), the former is a teacher, the latter is a place
    # 3) If the place has some of the icons, it is a place
    # The best status is all choosing 1), so for the others I'll ask the user to tell me

    # 1)
    possible_teacher_name = None
    has_place = False
    for info_str in undefined_str:
        try_res = TryPlace(info_str)
        if try_res:
            crs.Assign('place', try_res)
            has_place = True
        else:
            possible_teacher_name = info_str
        if has_place and possible_teacher_name:
            crs.Assign('teacher', possible_teacher_name)    
            break
    if has_place:
        return crs

    # 2)        
    if len(undefined_str) == 2:
        crs.Assign('teacher', undefined_str[0])
        crs.Assign('place', undefined_str[1])
        print u'###Though not in the record, I guess "%s" is a place. Please tell me anyway :)' % undefined_str[1]
        return crs

    # 3)
    possible_teacher_name = None
    has_place = False
    for info_str in undefined_str:
        try_res = TryPlaceIcon(info_str)
        if try_res:
            print u'###Though not in the record, I guess "%s" is a place. Please tell me anyway :)' % info_str
            crs.Assign('place', try_res)
            has_place = True
        else:
            possible_teacher_name = info_str
        if has_place and possible_teacher_name:
            crs.Assign('teacher', possible_teacher_name)            
            break
        
    return crs

def AnalyseCellStr(wday, cls_num, crs_str, already_crs_str):
    '''Analyse the string in a cell, and returns the list of the courses of the cell
parameter
    wday    - the day of week analysed roughly by the table
    cls_num - the number of class time analysed roughly by the table
    crs_str - the main string in the cell of the table
    already_crs_str   - list of (cls_name, info_str) ever met. Avoid same class 
                                    appears again (happens a lot for long exp classes)
Return 
    [Courses(, ...)]'''
    crs_str_lst = crs_str.strip(u' \n\t\r').split(u'\n')
    crs_lst = []
    # matches the string that has a pair of brackets with a Chinese semicolon in it
    #   like u'...(...；...)...'
    # only choose the first bracket pair. 
    # and pick out the string before, between the brackets
    pattern = u'^(.*)\((.*?；.*?)\)$'

    for crs_str_raw in crs_str_lst:
        crs_str = crs_str_raw.strip(u' \n\t\r')
        regex_res = re.match(pattern, crs_str)
        if not regex_res:
            print u'### What\'s this? "%s"' % crs_str
            break
        crs_name, crs_info_str = regex_res.groups()

        # test if same as a course once met
        same_as_history_flag = False
        for old_str in already_crs_str:
            if (crs_name, crs_info_str) == old_str:
                same_as_history_flag = True
                break
        if same_as_history_flag:
            continue
        already_crs_str.append((crs_name, crs_info_str))

        crs = AnalyseCrsInfo(crs_name, wday, cls_num, crs_info_str)
        crs_lst.append(crs)

    return crs_lst

def CSVTitle():
    return u'主题,开始日期**,开始时间,结束日期,结束时间,全天事件,提醒开/关,提醒日期,提醒时间,会议组织者,必需的与会者,可选的与会者,会议资源,地点**,记帐信息,类别,里程,忙闲状态,敏感度,说明,私有,优先级'

def CSVEvent(content, place, startdate, starttime, enddate, endtime, remarks = u'', reminddate = (), remindtime = (), fullday = False):
    '''date: (year, month, day)
time(hour, minute)'''
    pattern = u'%s,%d/%d/%d,%d:%02d:%02d,%d/%d/%d,%d:%02d:%02d,%s,%s,%d/%d/%d,%02d:%02d:%02d,,,,,%s,,,,2,普通,"%s",FALSE,中'
    if (not reminddate) or (not remindtime):
        reminddate = startdate
        remindtime = starttime
        bool_remind = u'FALSE'
    else:
        bool_remind = u'TRUE'
    final_str = pattern % (
            content,
            startdate[0], startdate[1], startdate[2],
            starttime[0], starttime[1], 0,
            enddate[0], enddate[1], enddate[2],
            endtime[0], endtime[1], 0,
            'TRUE' if fullday else 'FALSE',
            bool_remind,
            reminddate[0], reminddate[1], reminddate[2],
            remindtime[0], remindtime[1], 0,
            place, remarks)
    return final_str

def GetDateByWeek(week_num, wday, first_week_date):
    addition_day = (week_num - 1) * 7 + (wday - 1)
    return timebasic.CarryDate(first_week_date[0], first_week_date[1],
            first_week_date[2] + addition_day)

def CourseLstToCSVFormat(crs_lst, first_week_date, week_info = False):
    csv_str_lst = [CSVTitle()]
    for crs in crs_lst:
        for week in crs.week:
            date = GetDateByWeek(week, crs.wday, first_week_date)
            csv_str_lst.append(CSVEvent(crs.name, crs.place, 
                date, crs.time[0], date, crs.time[1], crs.teacher + u' ' + crs.catagory))
    if week_info:
        for week in range(1, 19):
            date = GetDateByWeek(week, 1, first_week_date)
            csv_str_lst.append(CSVEvent(u'第%d周'%week, u'', 
                date, (0, 0), date, (23, 59), u'',
                fullday=True))
    return csv_str_lst

def translateXlsToCourses(bk):
    # May raise IndexError
    sh = bk.sheet_by_index(0)

    # In case there are more than 6 classes a day (it really happens!)
    # Check the first column, which is '第1节'(row2)... '第6节'
    tmp_row = 2
    try:
        while sh.cell_value(tmp_row, 0).strip():
            tmp_row += 1
    except IndexError:
        pass
    
    # max of the course table is max_row - 1
    max_row = tmp_row
    
    crs_lst = []
    for col in range(1, 8):
        already_crs_str = []
        for row in range(2, max_row):
            str_get = sh.cell_value(row, col).strip()
            if str_get:
                crs_lst.extend(AnalyseCellStr(col, row - 1, str_get, already_crs_str))

    return crs_lst

def writeCvs(crs_lst, tgt_file, start_date, add_week_info = False):
    
    csv_str_lst = CourseLstToCSVFormat(crs_lst, start_date, week_info = add_week_info)
    
    for csv_str in csv_str_lst:
        tgt_file.write(csv_str.encode('gb2312'))
        tgt_file.write('\n')

class CoursesException(Exception):
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

def translate(srcfilename, tgtfilename, start_date, add_week_info = False):
    # May raise IOError 
    try:
        bk = xlrd.open_workbook(srcfilename)
    except IOError:
        raise CoursesException('Can\' find file %s' % srcfilename)
    except xlrd.biffh.XLRDError:
        raise CoursesException('Invalid xls file %s' % srcfilename)
    
    crs_lst = translateXlsToCourses(bk)

    open_tgt_suc = True
    try:
        tgt_file = open(tgtfilename, 'w')
    except IOError:
        open_tgt_suc = False
        
    if not open_tgt_suc or not tgt_file:
        raise CoursesException('Can\' create file %s' % tgtfilename)

    if not timebasic.IsValidDate(*start_date):
        raise CoursesException('Invalid start date.')
        
    writeCvs(crs_lst, tgt_file, start_date = start_date, add_week_info = add_week_info)
    tgt_file.close()

    return True


__all__ = ["translate", "CoursesException"]
