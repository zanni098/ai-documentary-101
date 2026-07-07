import subprocess, json, os, math

ROOT = r"C:\Users\eishm\Downloads\doc_1"
os.chdir(ROOT)

def dur(p):
    return float(subprocess.check_output(
        ["ffprobe","-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1",p]
    ).decode().strip())

CHAR = {n: f"narrator/veo/{n}.mp4" for n in
    ["A3_steps_out_v3","R2_front_medium_v3","R1_closeup_v3","R3_wide_power_v3",
     "R4_turn_v3","R5_low_angle_v3","R7_walk_v3","R8_golden_v3","A9_departure_v3"]}
CHAR["A1_aerial"] = "narrator/hf_20260704_095133_8380756f-8726-47ec-90f5-4fafab6d3a2c.mp4"
CHAR["A2_landing"] = "narrator/veo/A2_heli_landing.mp4"

VOX = {n: f"master/vox_2k/VOX_{n:02d}_{name}_2k.mp4" for n, name in {
    1:"future_of_filmmaking",2:"old_workflow_vs_ai",3:"remotion_higgsfield_flow",
    4:"remotion_deeper",5:"remotion_limits",6:"higgsfield_deeper",
    7:"higgsfield_library",8:"higgsfield_limits",9:"claude_orchestration"}.items()}

VO = {n: f"master/voice_brian/SEG_{n}.mp3" for n in
    ["V2_01","V2_02","V2_03"] + [f"{i:02d}" for i in range(4,22)]}

SFX = {n: f"master/sfx/SFX_{n}.mp3" for n in
    ["rotor_spinup","rotor_spindown","heli_idle","heli_takeoff","footsteps_sand",
     "suit_rustle","wind_desert_bed","desert_ambience","boom_impact2","boom_reveal"]}

OUT = "master/final_scenes"; os.makedirs(OUT, exist_ok=True)

W,H = 1920,1080
LB_CROP_H = 816  # 2.35:1 crop height for letterbox on narrator scenes

def char_vf(scale_dur_target, src_dur, extra=""):
    """scale+crop to 1920x1080 2.35 letterbox, stretch time to fill target."""
    mult = scale_dur_target / src_dur
    return (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"setpts={mult:.4f}*PTS,crop={W}:{LB_CROP_H}:0:{(H-LB_CROP_H)//2},pad={W}:{H}:0:{(H-LB_CROP_H)//2}:black,"
            f"eq=contrast=1.09:saturation=1.08:brightness=-0.02,setsar=1{extra}")

def vox_vf():
    return f"scale={W}:{H}:flags=lanczos,setsar=1"

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG FAIL:", " ".join(cmd[-6:]))
        print(r.stderr[-1500:])
        raise SystemExit(1)

def render_character_beat(name, clip_names, vo_key, sfx_list, no_vo=False, fade_in=0.0, fade_out=0.0):
    """clip_names: list of CHAR keys played back-to-back, stretched to fill vo duration (+lead/tail pad)."""
    lead, tail = 0.6, 0.6
    vo_d = 0.0 if no_vo else dur(VO[vo_key])
    total = (vo_d + lead + tail) if not no_vo else sum(dur(CHAR[c]) for c in clip_names)
    n = len(clip_names)
    share = total / n
    inputs = []; vf_parts = []; labels = []
    for i, cn in enumerate(clip_names):
        src = CHAR[cn]; inputs += ["-i", src]
        sd = dur(src)
        vf_parts.append(f"[{i}:v]{char_vf(share, sd)}[v{i}]")
        labels.append(f"[v{i}]")
    concat_v = "".join(labels) + f"concat=n={n}:v=1:a=0[vcat]"
    fparts = vf_parts + [concat_v]
    fi = f"[vcat]"
    if fade_in > 0: fparts.append(f"{fi}fade=t=in:st=0:d={fade_in}[vfi]"); fi="[vfi]"
    if fade_out > 0: fparts.append(f"{fi}fade=t=out:st={total-fade_out:.2f}:d={fade_out}[vfo]"); fi="[vfo]"
    vf = ";".join(fparts)
    naudio = n
    # audio: VO + sfx list, mixed
    aidx = n
    a_inputs = []
    if not no_vo:
        a_inputs.append(("vo", VO[vo_key], lead, 1.25))
    for sname, off, vol, loopflag in sfx_list:
        a_inputs.append((sname, SFX[sname], off, vol, loopflag) if len(sfx_list[0])==4 else (sname, SFX[sname], off, vol))
    for item in a_inputs:
        inputs += ["-i", item[1]]
    af_parts = []; mix_labels = []
    for k, item in enumerate(a_inputs):
        idx = aidx + k
        name_, path, off = item[0], item[1], item[2]
        vol = item[3]
        loopflag = item[4] if len(item) > 4 else False
        if loopflag:
            af_parts.append(f"[{idx}:a]aloop=loop=-1:size=2000000000,atrim=0:{total:.2f},adelay={int(off*1000)}|{int(off*1000)},volume={vol}[a{k}]")
        else:
            af_parts.append(f"[{idx}:a]adelay={int(off*1000)}|{int(off*1000)},volume={vol}[a{k}]")
        mix_labels.append(f"[a{k}]")
    af = ";".join(af_parts) + ";" + "".join(mix_labels) + f"amix=inputs={len(a_inputs)}:duration=longest:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]"
    cmd = ["ffmpeg","-y"] + inputs + ["-filter_complex", vf + ";" + af,
        "-map","[vfo]" if fade_out>0 else ("[vfi]" if fade_in>0 else "[vcat]"),
        "-map","[a]","-t",f"{total:.2f}",
        "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-r","24",
        "-c:a","aac","-b:a","192k", f"{OUT}/{name}.mp4","-loglevel","error"]
    run(cmd)
    print(name, "OK", round(total,2), "s")

def render_vox_beat(name, vox_key, dim_audio=0.35):
    src = VOX[vox_key]
    d = dur(src)
    vf = f"[0:v]{vox_vf()}[v]"
    af = f"[0:a]volume={dim_audio}[a]"
    cmd = ["ffmpeg","-y","-i",src,"-filter_complex", vf+";"+af,
        "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","19",
        "-pix_fmt","yuv420p","-r","24","-c:a","aac","-b:a","192k", f"{OUT}/{name}.mp4","-loglevel","error"]
    run(cmd)
    print(name, "OK", round(d,2), "s")

def render_title(name, seconds=4.0):
    vf = (f"color=c=black:s={W}x{H}:d={seconds}[bg];"
          f"[bg]drawtext=text='AI DOCUMENTARY MAKING 101':fontcolor=white:fontsize=90:"
          f"font=Arial:fontfile='C\\:/Windows/Fonts/arialbd.ttf':x=(w-text_w)/2:y=(h-text_h)/2:"
          f"alpha='if(lt(t,0.4),t/0.4,if(gt(t,{seconds-0.6}),({seconds}-t)/0.6,1))'[v]")
    af = f"anullsrc=channel_layout=stereo:sample_rate=44100"
    cmd = ["ffmpeg","-y","-f","lavfi","-i",vf.split("[v]")[0].split("drawtext")[0].strip(";")+"", ]
    # simpler: build via filter_complex with color source directly
    cmd = ["ffmpeg","-y","-f","lavfi","-i", f"color=c=black:s={W}x{H}:d={seconds}:r=24",
           "-f","lavfi","-i", f"anullsrc=channel_layout=stereo:sample_rate=44100",
           "-vf", (f"drawtext=text='AI DOCUMENTARY MAKING 101':fontcolor=white:fontsize=84:"
                   f"fontfile='C\\:/Windows/Fonts/arialbd.ttf':x=(w-text_w)/2:y=(h-text_h)/2:"
                   f"alpha='if(lt(t\\,0.4)\\,t/0.4\\,if(gt(t\\,{seconds-0.6})\\,({seconds}-t)/0.6\\,1))'"),
           "-t", f"{seconds}", "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p",
           "-c:a","aac","-b:a","192k","-shortest", f"{OUT}/{name}.mp4","-loglevel","error"]
    run(cmd)
    print(name, "OK")

print("=== Building all beats ===")

# SCENE 1: ARRIVAL (silent)
render_character_beat("S1a_aerial", ["A1_aerial"], None, [
    ("wind_desert_bed",0.0,0.30,True),("heli_idle",0.0,0.35,True)], no_vo=True, fade_in=0.8)
render_title("S1b_title", 3.2)
render_character_beat("S1c_landing", ["A2_landing"], None, [
    ("wind_desert_bed",0.0,0.28,True),("rotor_spindown",0.0,0.55,False)], no_vo=True)
render_character_beat("S1d_stepsout", ["A3_steps_out_v3"], None, [
    ("wind_desert_bed",0.0,0.25,True),("footsteps_sand",1.0,0.5,False),("suit_rustle",0.3,0.4,False)], no_vo=True)

# SCENE 2: THE ADDRESS
render_character_beat("S2a_vo1", ["R2_front_medium_v3"], "V2_01",
    [("wind_desert_bed",0,0.22,True),("boom_impact2",0.0,0.7,False)])
render_character_beat("S2b_vo2", ["R1_closeup_v3","R4_turn_v3"], "V2_02",
    [("wind_desert_bed",0,0.22,True)])
render_character_beat("S2c_vo3", ["R3_wide_power_v3"], "V2_03",
    [("wind_desert_bed",0,0.24,True)], fade_out=0.0)

# SCENE 3: OLD WORLD -> exhibits 1,2
render_character_beat("S3a_vo04", ["R7_walk_v3"], "04", [("wind_desert_bed",0,0.2,True)])
render_vox_beat("S3b_vox1", 1)
render_character_beat("S3c_vo05", ["R2_front_medium_v3"], "05", [("wind_desert_bed",0,0.2,True)])
render_vox_beat("S3d_vox2", 2)
render_character_beat("S3e_vo06", ["R4_turn_v3","R1_closeup_v3"], "06", [("wind_desert_bed",0,0.2,True)])

# SCENE 4: TWO TOOLS -> exhibits 3-7
render_character_beat("S4a_vo07", ["R1_closeup_v3"], "07", [("wind_desert_bed",0,0.2,True)])
render_vox_beat("S4b_vox3", 3)
render_character_beat("S4c_vo08", ["R2_front_medium_v3","R7_walk_v3"], "08", [("wind_desert_bed",0,0.2,True)])
render_vox_beat("S4d_vox4", 4)
render_vox_beat("S4e_vox5", 5)
render_character_beat("S4f_vo09", ["R4_turn_v3"], "09", [("wind_desert_bed",0,0.2,True)])
render_vox_beat("S4g_vox6", 6)
render_character_beat("S4h_vo10", ["R2_front_medium_v3","R5_low_angle_v3"], "10", [("wind_desert_bed",0,0.2,True)])
render_vox_beat("S4i_vox7", 7)

# SCENE 5: COST -> exhibit 8
render_character_beat("S5a_vo11", ["R1_closeup_v3","R3_wide_power_v3"], "11",
    [("wind_desert_bed",0,0.22,True),("boom_reveal",0.0,0.5,False)])
render_vox_beat("S5b_vox8", 8)

# SCENE 6: ORCHESTRATOR REVEAL -> exhibit 9
render_character_beat("S6a_vo12", ["R2_front_medium_v3","R4_turn_v3"], "12", [("wind_desert_bed",0,0.2,True)])
render_character_beat("S6b_vo13", ["R5_low_angle_v3"], "13",
    [("wind_desert_bed",0,0.2,True),("boom_impact2",0.0,0.75,False)])
render_vox_beat("S6c_vox9", 9)
render_character_beat("S6d_vo14", ["R5_low_angle_v3","R2_front_medium_v3"], "14", [("wind_desert_bed",0,0.2,True)])

# SCENE 7: REFLECTION (golden hour)
render_character_beat("S7a_vo15", ["R8_golden_v3"], "15", [("wind_desert_bed",0,0.24,True)])
render_character_beat("S7b_vo16", ["R1_closeup_v3"], "16", [("wind_desert_bed",0,0.2,True)])
render_character_beat("S7c_vo17", ["R8_golden_v3"], "17", [("wind_desert_bed",0,0.26,True)])

# SCENE 8: DEPARTURE / SIGN-OFF
render_character_beat("S8a_vo18", ["R3_wide_power_v3","R4_turn_v3"], "18", [("wind_desert_bed",0,0.2,True)])
render_character_beat("S8b_vo19", ["R2_front_medium_v3"], "19",
    [("wind_desert_bed",0,0.2,True),("rotor_spinup",3.0,0.4,False)])
render_character_beat("S8c_departure", ["A9_departure_v3"], None,
    [("rotor_spinup",0.0,0.55,False),("heli_takeoff",3.5,0.5,False),("wind_desert_bed",0,0.2,True)],
    no_vo=True, fade_out=1.2)

print("=== ALL BEATS RENDERED ===")
