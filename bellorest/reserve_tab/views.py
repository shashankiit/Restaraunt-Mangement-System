from django.shortcuts import redirect, render
from userlog.models import User
from .models import *
from django.contrib import messages
from django.db.models import Q
from datetime import time, date

def differlist(li1, li2):
	setA=set(li1)
	setB=set(li2)
	return list(setA.difference(setB))

def overlap(s1, e1, s2, e2):
	return not (e2 < s1 or e1 < s2)

def timeadd(t1,t2):
	t1l = t1.split(':')
	t2l = t2.split(':')
	minute = 0
	hour = 0
	minute = int(t1l[1]) + int(t2l[1])
	while minute > 60:
		hour +=1
		minute -= 60
	hour += int(t1l[0]) + int(t2l[0])
	if minute < 10:
		minute = "0" + str(minute)
	time = str(hour) + ":" + str(minute)
	return time

def reservation(request, pnum):
	user = User.objects.get(phone=int(pnum))
	return render(request, 'reserve_tab/reservation.html', {"user":user})

def confres(request, pnum):
	if request.method == 'POST':
		alldata = request.POST
		pnum = alldata["pnum"]
		lister = alldata.getlist('name')
		diners = lister[0]
		date = lister[1]
		restime = lister[2]
		tdur = lister[3]
		endtime = timeadd(restime, tdur)
		context = {'diners':diners ,'date':date, 'restime':restime, 'duration':tdur, 'endtime':endtime, 'user':pnum}
	return render(request, 'reserve_tab/confres.html', context)

def buttonform(request, pnum):
	if request.POST["action"] == "Confirm":
		# GRAB DATA FROM URL
		diners = int(request.POST["diners"])
		datex = request.POST["date"]
		restime = request.POST["restime"]
		timedur = request.POST["duration"]
		endtime = request.POST["endtime"]
		# FORMAT DATA FOR COMPARISON
		start = restime.split(':')
		timeup=time(hour=int(start[0]),minute=int(start[1]),second=0)
		start = endtime.split(':')
		timedown=time(hour=int(start[0]),minute=int(start[1]),second=0)
		start = datex.split('-')
		datex = date(year=int(start[0]),month=int(start[1]),day=int(start[2]))
		today = date.today()
		# START COMPUTATION
		if datex > today:
			dateres = Reservation.objects.filter(date_for_res=datex)
			print((timeup < timedown))
			occupied_tables=[]
			occupied_objects=[]
			for i in range(dateres.count()):
				current = dateres[i]
				stime = current.time_for_res
				sdur = stime.strftime('%H:%M')
				tdur = current.reservation_duration.strftime('%H:%M')
				etime = timeadd(tdur,sdur)
				start = endtime.split(':')
				etime=time(hour=int(start[0]),minute=int(start[1]),second=0)
				overlapval = overlap(stime,etime,timeup,timedown)
				print(overlapval)
				if overlapval == True:
					occupied_tables.append(int(current.table_id))
					occupied_objects.append(current)
				else:
					continue
			alltables = Dining_table.objects.filter(capacity__gte=diners)
			alltab=[]
			for i in range(alltables.count()):
				alltab.append(int(alltables[i].table_id))
			avaitables = differlist(alltab,occupied_tables)
			blocked_slots_list = []
			for i in range(len(occupied_objects)):
				stime = occupied_objects[i].time_for_res.strftime('%H:%M')
				tdur = current.reservation_duration.strftime('%H:%M')
				etime = timeadd(tdur,sdur)
				stringer = stime + ' - ' + etime
				blocked_slots_list.append(stringer)
			if len(avaitables)==0:
				print(blocked_slots_list)
				messages.info(request, 'No Tables Available at that time')
				return redirect('/reserve_tab/'+str(pnum)+'/reservation')
		elif datex == today:
			# alltables = Dining_table.objects.filter(Q(capacity__gte = diners) & Q(phone_occupied = None))
			# avaitables=[]
			# for i in range(alltables.count()):
			# 	avaitables.append(alltables[i].table_id)
			# if len(avaitables) == 0:
			messages.info(request, 'Cannot reserve on the same day')
			return redirect('/reserve_tab/'+str(pnum)+'/reservation')
		else:#WORKING
			messages.info(request, 'No point reserving in the past')
			return redirect('/reserve_tab/'+str(pnum)+'/reservation')
		# GET TABLE OBJECTS WHICH ARE AVAILABLE
		avaitobj = Dining_table.objects.filter(table_id__in=avaitables)
		avaitsobj = avaitobj.order_by('capacity').first()
		mytableid = avaitsobj.table_id
		Reservation.objects.create(table_id=mytableid,phone = pnum,date_for_res=datex,num_diners=diners,time_for_res=timeup,reservation_duration=timedur)
		messages.info(request, 'Reservation Confirmed')
		return redirect('/ufunc')
	else:
		messages.info(request, 'Ask the nearest manager for help')
		return redirect('/reserve_tab/'+str(pnum)+'/reservation')