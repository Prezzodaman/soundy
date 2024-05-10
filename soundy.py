import tkinter as tk # seduce me baby, seduce me with your, seduce me baby, seduce me with your
import time
import os
import sys
import simpleaudio
import random

def get_widget_name(widget):
	return str(widget).split(".")[-1]

def toggle_step(event):
	name=get_widget_name(event.widget)
	name_split=name.split("_")
	sound=int(name_split[1])
	step=int(name_split[3])
	steps_states[sound][step]=not steps_states[sound][step]
	if steps_states[sound][step]:
		event.widget.config(bg="black")
	else:
		event.widget.config(bg="white")

def get_widget_by_name(root,name):
	widget_yes=None
	for widget in root.winfo_children():
		if get_widget_name(widget)==name:
			widget_yes=widget
	return widget_yes

def toggle_sound(event):
	name=get_widget_name(event.widget)
	sound=int(name.split("_")[1])
	sound_muted[sound]=not sound_muted[sound]
	if sound_muted[sound]:
		event.widget.config(bg="red")
	else:
		event.widget.config(bg="white")

def kill_sound(event):
	name=get_widget_name(event.widget)
	sound=int(name.split("_")[1])
	for sound_obj in sounds_obj_playing[sound]:
		sound_obj.stop()
	sounds_obj_playing[sound].clear()

def randomize_steps():
	for a in range(0,4):
		sound=random.randint(0,len(sounds)-1)
		step=random.randint(0,steps-1)
		steps_states[sound][step]=True
		get_widget_by_name(steps_frame,f"sound_{sound}_step_{step}").config(bg="black")

def clear_steps():
	for sound in range(0,len(sounds)):
		for step in range(0,steps):
			steps_states[sound][step]=False
			get_widget_by_name(steps_frame,f"sound_{sound}_step_{step}").config(bg="white")

if len(sys.argv)==3:
	path=sys.argv[1]
	sounds=[]
	sounds_obj=[]
	for filename in os.listdir(path):
		if filename.split(".")[-1].lower()=="wav":
			sound=os.path.basename(filename)
			try:
				obj=simpleaudio.WaveObject.from_wave_file(f"{path}/{filename}")
				if obj.sample_rate%8000==0 or obj.sample_rate%11025==0:
					sounds_obj.append(obj)
					sounds.append(filename)
				else:
					print(f"Warning: \"{sound}\" has an invalid sample rate, excluding")
			except:
				print(f"Warning: \"{sound}\" is an invalid wave file, excluding")

	sounds_limit=16
	if len(sounds)>sounds_limit:
		indices=[] # professional coding
		for a in range(0,len(sounds)):
			indices.append(a)
		random.shuffle(indices)
		indices=indices[:sounds_limit]
		sounds_temp=[]
		sounds_obj_temp=[]
		for index in indices:
			sounds_temp.append(sounds[index])
			sounds_obj_temp.append(sounds_obj[index])
		sounds=sounds_temp
		sounds_obj=sounds_obj_temp

	if len(sounds)==0:
		print("Error: no sounds with a valid sample rate!")
	else:
		kint=tk.Tk()
		kint.resizable(width=False,height=False)
		kint.title("Soundy")

		steps_frame=tk.Frame(kint)

		steps=int(sys.argv[2])
		if steps<8:
			steps=8
		if steps>64:
			steps=64
		steps_states=[]
		sounds_obj_playing=[]
		temp=[False]*steps
		for sound in range(0,len(sounds)):
			steps_states.append(temp.copy())
			sounds_obj_playing.append([])
		current_step=0
		bpm=120
		sound_muted=[False]*len(sounds)
		sound_mono=[]
		sound_phase=[]
		for sound in range(0,len(sounds)):
			sound_mono.append(tk.BooleanVar(value=False))
			sound_phase.append(tk.StringVar(value="1"))
		sound_options=3

		limit=40

		pos_label=tk.Label(steps_frame,text="v")

		for sound in range(0,len(sounds)):
			for step in range(0,steps):
				if step%4==0:
					thing="*"
				else:
					thing="."
				label=tk.Label(steps_frame,text=thing,width=4,height=2,borderwidth=1,relief="solid",bg="white",name=f"sound_{sound}_step_{step}",cursor="cross")
				label.bind("<Button-1>",toggle_step)
				label.grid(row=sound+1,column=step+sound_options+2)

			mute_label=tk.Label(steps_frame,text="X",width=4,height=2,borderwidth=1,relief="solid",bg="white",name=f"sound_{sound}_mute",cursor="cross")
			mute_label.grid(row=sound+1,column=0)
			mute_label.bind("<Button-1>",toggle_sound)

			name_label=tk.Label(steps_frame,text=os.path.basename(sounds[sound]),height=2,name=f"label_{sound}")
			name_label.grid(row=sound+1,column=1)

			mono_check=tk.Checkbutton(steps_frame,text="Mono",variable=sound_mono[sound])
			mono_check.grid(row=sound+1,column=2)

			phase_entry=tk.Entry(steps_frame,width=2,textvariable=sound_phase[sound])
			phase_entry.grid(row=sound+1,column=3)

			kill_button=tk.Button(steps_frame,text="Kill",name=f"kill_{sound}")
			kill_button.grid(row=sound+1,column=4)
			kill_button.bind("<Button-1>",kill_sound)

		steps_frame.pack()

		tk.Label(kint,text="BPM:").pack()
		bpm_slider=tk.Scale(kint,from_=20,to=200,orient="horizontal")
		bpm_slider.pack()
		bpm_slider.set(120)

		prefs_frame=tk.Frame(kint)
		playing_label=tk.Label(prefs_frame,text="")
		playing_label.pack(side="left")

		actual_bpm_label=tk.Label(prefs_frame,text="")
		actual_bpm_label.pack(side="left")

		randomize_button=tk.Button(prefs_frame,text="Randomize",command=randomize_steps)
		randomize_button.pack(side="left")

		clear_button=tk.Button(prefs_frame,text="Clear",command=clear_steps)
		clear_button.pack(side="left")

		prefs_frame.pack()

		overflow_label=tk.Label(kint,text="")
		overflow_label.pack()

		sounds_playing=0
		average_bpm=0

		while True:
			last_time=time.perf_counter()
			bpm_duration=(((60000/bpm_slider.get())/4))/1000
			time.sleep(bpm_duration)
			if current_step>=steps:
				current_step=0
			for number,sound in enumerate(steps_states):
				if sound[current_step] and not sound_muted[number]:
					if sound_mono[number].get():
						for sound_obj in sounds_obj_playing[number]:
							sound_obj.stop()
						sounds_obj_playing[number].clear()
					if sound_phase[number].get().isdigit():
						phase=int(sound_phase[number].get())
					else:
						phase=1
					if sounds_playing<limit:
						for a in range(0,phase):
							sounds_obj_playing[number].append(sounds_obj[number].play())
					else:
						print("refused")

			if sounds_playing>=limit:
				overflow_label.configure(text="OVERFLOW!!!")
			else:
				overflow_label.configure(text="")

			pos_label.grid(row=0,column=current_step+sound_options+2)
			current_step+=1

			temp=[]
			sounds_to_pop=[]

			for number,sound in enumerate(sounds_obj_playing):
				for number_obj,obj in enumerate(sound):
					if not obj.is_playing():
						sounds_to_pop.append([number,number_obj])

			for thing in sounds_to_pop:
				if thing[1]<len(sounds_obj_playing[thing[0]]):
					sounds_obj_playing[thing[0]].pop(thing[1])

			sounds_playing=0
			for sound in sounds_obj_playing:
				sounds_playing+=len(sound)
			playing_label.configure(text=f"Sounds currently playing: {sounds_playing} | ")

			time_diff=time.perf_counter()-last_time
			actual_bpm=15/time_diff
			average_bpm+=actual_bpm
			average_bpm/=2

			actual_bpm_label.configure(text=f"Actual BPM: {actual_bpm:.2f} | ")
			kint.update()
else:
	print("Parameters: sound path, sequence length")