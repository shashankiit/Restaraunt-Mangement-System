from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
from datetime import time, date, datetime, timedelta

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
	while minute >= 60:
		hour +=1
		minute -= 60
	hour += int(t1l[0]) + int(t2l[0])
	if minute < 10:
		minute = "0" + str(minute)
	time = str(hour) + ":" + str(minute)
	return time

def get_slots(hours, appointments, duration):
	slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
	freeslots = []
	for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
		# assert start <= end, "Cannot attend all appointments"
		while start + duration <= end:
			x = "{:%H:%M} - {:%H:%M}".format(start, start + duration)
			freeslots.append(x)
			start += duration
	return freeslots

def reservation(request, pnum):
	user = User.objects.get(phone=int(pnum))
	return render(request, 'reserve_tab/reservation.html', {"user":user})

def confres(request, pnum):
	if request.method == 'POST':
		alldata = request.POST
		phnum = alldata["pnum"]
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
		datesplit = datex.split('-')
		datex = date(year=int(datesplit[0]),month=int(datesplit[1]),day=int(datesplit[2]))
		start = restime.split(':')
		timeup=datetime(year=int(datesplit[0]),month=int(datesplit[1]),day=int(datesplit[2]),hour=int(start[0]),minute=int(start[1]))
		start = endtime.split(':')
		timedown=datetime(year=int(datesplit[0]),month=int(datesplit[1]),day=int(datesplit[2]),hour=int(start[0]),minute=int(start[1]))
		start = timedur.split(':')
		td = timedelta(hours=int(start[0]),minutes=int(start[1]))
		workinghours = (datetime(year=int(datesplit[0]),month=int(datesplit[1]),day=int(datesplit[2]),hour=8), datetime(year=int(datesplit[0]),month=int(datesplit[1]),day=int(datesplit[2]),hour=23))
		today = date.today()
		# START COMPUTATION
		if datex > today:
			dateres = Reservation.objects.filter(date_for_res=datex)
			occupied_tables=[]
			occupied_objects=[]
			freeslotscomputation=[]
			for i in range(dateres.count()):
				current = dateres[i]
				stime = current.time_for_res
				sdur = stime.strftime('%H:%M')
				start = sdur.split(':')
				stime=datetime(year=int(datesplit[0]),month=int(datesplit[1]),day=int(datesplit[2]),hour=int(start[0]),minute=int(start[1]))
				tdur = current.reservation_duration.strftime('%H:%M')
				etime = timeadd(tdur,sdur)
				start = etime.split(':')
				etime=datetime(year=int(datesplit[0]),month=int(datesplit[1]),day=int(datesplit[2]),hour=int(start[0]),minute=int(start[1]))
				overlapval = overlap(stime,etime,timeup,timedown)
				if overlapval == True:
					x=(stime,etime)
					freeslotscomputation.append(x)
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
				tdur = occupied_objects[i].reservation_duration.strftime('%H:%M')
				etime = timeadd(tdur,sdur)
				stringer = stime + ' - ' + etime
				blocked_slots_list.append(stringer)
			if len(avaitables)==0:
				freeslots = get_slots(workinghours,freeslotscomputation,td)
				messages.info(request, 'No Tables Available at that time')
				messages.info(request, 'Free slots are:')
				for i in freeslots:
					messages.info(request, i)
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