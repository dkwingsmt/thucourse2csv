#!/usr/bin/env python
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

import time

class StructTime(object):
	def __init__(self, year, month, day, hour, minute):
		self.year = year
		self.month = month
		self.day = day
		self.hour = hour
		self.minute = minute
	def __repr__(self):
		return '<StructTime object %s>' % repr(self.__dict__)

def CalcWday(year, month, mday):
	'''Calculate day of week
month: 1~12
mday: 1~31
return: range [0, 6], Monday is 0 (same as time.localtime())
Will NOT test if it's a valid date.'''
    #Zeller formula, see http://www.blogjava.net/realsmy/archive/2007/05/10/116475.html
	if month < 3:
		year = year - 1
		month = month + 12
	c = (year // 100) - 1
	y = year % 100
	m = month
	d = mday
	return (y+y//4+c//4-2*c+26*(m+1)//10+d-3)%7

def MaxDayOfMonth(year, month):
	#  month      1  2  3  4  5  6  7  8  9  10 11 12
	dayofmonth = (31,28,31,30,31,30,31,31,30,31,30,31)
	maxmday = dayofmonth[month - 1]
	if month == 2 and IsLeapYear(year):
		maxmday = 29
	return maxmday

def IsLeapYear(year):
	'''Returns if this year is a leap year'''
	return ((year%4 == 0) and (not (year%100 == 0))) or (year%400 == 0)

def IsValidMonth(month):
	'''Returns if this month is a valid month.'''
	if month < 1 or month > 12:
		return False
	return True

def IsValidMDay(year, month, mday):
	'''Returns if this day of month is valid.'''
	if mday < 1 or mday > MaxDayOfMonth(year, month):
		return False
	return True

def IsValidDate(year, month, mday):
	'''Returns if this date is a valid date.'''
	return IsValidMonth(month) and IsValidMDay(year, month, mday)

def SimpleTimeToInt(time_struct):
	'''Convert time (in StructTime) to a int,
If failed for any of the keys, return 0
Guarantee that SimpleTimeToInt(a_later_time) > SimpleTimeToInt(an_earlier_time),
plus one time correspond to one int, vise versa,
but int might not be continuous as time increase.'''
	weights = (
		('minute', 60),
		('hour', 60*60),
		('day', 60*60*24),
		('month', 60*60*24*31),
		('year', 60*60*24*31*12),
		)
	val = 0
	time_dic = time_struct.__dict__
	try:
		for key, weight in weights:
			offset = -1900 if key == 'year' else 0
			val = val + (time_dic[key] + offset) * weight
	except KeyError:
		val = 0
	return val

def CarryMonth(year, month):
	'''If the month is out of range, modify year to last/next year
Return (new_year, new_month)'''
	ret_year = year
	ret_month = month
	processed = False
	while ret_month < 1:	
		ret_month = ret_month + 12
		ret_year = ret_year - 1
		processed = True	
	if not processed:
		while ret_month > 12:
			ret_month = ret_month - 12
			ret_year = ret_year + 1
	return (ret_year, ret_month)

def CarryDate(year, month, mday):
	'''If the month and day is out of range, modify year and month to fit them
Return (new_year, new_month, new_mday)'''
	(ret_year, ret_month) = CarryMonth(year, month)
	ret_mday = mday
	processed = False
	while ret_mday < 1:
		ret_month = ret_month - 1
		(ret_year, ret_month) = CarryMonth(ret_year, ret_month)	
		ret_mday = ret_mday + MaxDayOfMonth(ret_year, ret_month)
		processed = True		
	if not processed:
		this_max_day_of_month = MaxDayOfMonth(ret_year, ret_month)
		while ret_mday > this_max_day_of_month:
			ret_mday = ret_mday - this_max_day_of_month
			ret_month = ret_month + 1
			(ret_year, ret_month) = CarryMonth(ret_year, ret_month)
			this_max_day_of_month = MaxDayOfMonth(ret_year, ret_month)
	return (ret_year, ret_month, ret_mday)

def CarryMinute(hour, minute):
	'''If minute is out of range([0, 60) ), change hour to suit it.
Return (new_hour, new_minute)'''
	while minute < 0:
		minute = minute + 60
		hour = hour - 1
	while minute > 59:
		minute = minute - 60
		hour = hour + 1
	return (hour, minute)

def CarryHour(day, hour):
	'''If hour is out of range([0, 23) ), change dayt to suit it.
Return (new_day, new_hour)'''
	while hour < 0:
		hour = hour + 24
		day = day - 1
	while hour > 59:
		hour = hour - 24
		day = day + 1
	return (day, hour)

def GenerateNowTime():
	'''返回值：StructTime时间值'''
	nowtm = time.localtime()
	return StructTime(
		year=nowtm.tm_year,
		month=nowtm.tm_mon,
		day=nowtm.tm_mday,
		hour=nowtm.tm_hour,
		minute=nowtm.tm_min
		)

def GenerateTimeStr(target_time, now_time = None):
	'''通过target_time构建字符串u'x年x月x日x点x分'返回。
如果显式给出了now_time，将会把target_time与now_time从前至后相同的部分省略'''
	
	timepattern = ((u'%d年', 'year'),
		   (u'%d月', 'month'),
		   (u'%d日', 'day'),
		   (u'%d点', 'hour'),
		   (u'%d分', 'minute'))

        replace_table = (
                (u'0分', u'整'),
                (u'0点0分', u''),
                )

	ret_str_lst = []
	tgt_dic = target_time.__dict__
	now_dic = now_time.__dict__ if now_time else None
	# 因为从前至后的连续相同的部分省略，
	# 一旦遇见不同的部分MetDiffrent置True，之后不再可能省略
	MetDiffrent = False        
	try:
		for pattern, name in timepattern:
			number = tgt_dic[name]
			if (not MetDiffrent) and now_time:
				now_number = now_dic[name]
				if now_number == number:
					continue
				else:
					MetDiffrent = True
			ret_str_lst.append(pattern % number)
	except KeyError:
		ret_str_lst = [u'错误时间']

	ret_str = u''.join(ret_str_lst)
	if ret_str == u'':
		ret_str = u'现在'
        for before, after in replace_table:               
                ret_str = ret_str.replace(before, after)
                

	return ret_str
