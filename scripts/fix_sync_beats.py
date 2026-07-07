import subprocess, os

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

VO = {n: f"master/voice_brian/SEG_{n}.mp3" for n in
    ["V2_01","V2_02","V2_03"] + [f"{i:02d}" for i in range(4,22)]}

SFX = {n: f"master/sfx/SFX_{n}.mp3" for n in
    ["rotor_spinup","rotor_spindown","heli_idle","heli_takeoff","footsteps_sand",
     "suit_rustle","wind_desert_bed","desert_ambience","boom_impact2","boom_reveal"]}

OUT = "master/final_scenes"
W,H = 1920,1080
LB_CROP_H = 816

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG FAIL:", " ".join(cmd[-8:]))
        print(r.stderr[-1500:])
        raise SystemExit(1)

def char_vf_natural(share, src_dur, extra=""):
    """Trim a natural-speed window of length `share` from the middle of the source (no speed change)."""
    start = max(0.0, (src_dur - share) / 2.0)
    return (f"trim=start={start:.3f}:duration={share:.3f},setpts=PTS-STARTPTS,"
            f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"crop={W}:{LB_CROP_H}:0:{(H-LB_CROP_H)//2},pad={W}:{H}:0:{(H-LB_CROP_H)//2}:black,"
            f"eq=contrast=1.09:saturation=1.08:brightness=-0.02,setsar=1{extra}")

def char_vf_stretch(share, src_dur, extra=""):
    """Slow-motion stretch for when the VO beat needs MORE time than the clip naturally has."""
    mult = share / src_dur
    return (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"setpts={mult:.4f}*PTS,crop={W}:{LB_CROP_H}:0:{(H-LB_CROP_H)//2},pad={W}:{H}:0:{(H-LB_CROP_H)//2}:black,"
            f"eq=contrast=1.09:saturation=1.08:brightness=-0.02,setsar=1{extra}")

def render_character_beat(name, clip_names, vo_key, sfx_list, fade_in=0.0, fade_out=0.0):
    lead, tail = 0.6, 0.6
    vo_d = dur(VO[vo_key])
    total = vo_d + lead + tail
    n = len(clip_names)
    share = total / n
    inputs = []; vf_parts = []; labels = []
    for i, cn in enumerate(clip_names):
        src = CHAR[cn]; inputs += ["-i", src]
        sd = dur(src)
        mult = share / sd
        if mult < 1.0:
            vf_parts.append(f"[{i}:v]{char_vf_natural(share, sd)}[v{i}]")
        else:
            vf_parts.append(f"[{i}:v]{char_vf_stretch(share, sd)}[v{i}]")
        labels.append(f"[v{i}]")
    concat_v = "".join(labels) + f"concat=n={n}:v=1:a=0[vcat]"
    fparts = vf_parts + [concat_v]
    fi = "[vcat]"
    if fade_in > 0: fparts.append(f"{fi}fade=t=in:st=0:d={fade_in}[vfi]"); fi="[vfi]"
    if fade_out > 0: fparts.append(f"{fi}fade=t=out:st={total-fade_out:.2f}:d={fade_out}[vfo]"); fi="[vfo]"
    vf = ";".join(fparts)
    aidx = n
    a_inputs = [("vo", VO[vo_key], lead, 1.25)]
    for sname, off, vol, loopflag in sfx_list:
        a_inputs.append((sname, SFX[sname], off, vol, loopflag))
    for item in a_inputs:
        inputs += ["-i", item[1]]
    af_parts = []; mix_labels = []
    for k, item in enumerate(a_inputs):
        idx = aidx + k
        path, off, vol = item[1], item[2], item[3]
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
    print(name, "OK", round(total,2), "s (re-synced)")

# Beats needing re-sync: any beat whose share/src_dur < 1.0 was previously sped up unnaturally.
# Rebuild ALL dialogue beats with the corrected natural-trim-or-slowmo logic (keeps everything consistent).
render_character_beat("S2a_vo1", ["R2_front_medium_v3"], "V2_01",
    [("wind_desert_bed",0,0.22,True),("boom_impact2",0.0,0.7,False)])
render_character_beat("S2b_vo2", ["R1_closeup_v3","R4_turn_v3"], "V2_02",
    [("wind_desert_bed",0,0.22,True)])
render_character_beat("S2c_vo3", ["R3_wide_power_v3"], "V2_03",
    [("wind_desert_bed",0,0.24,True)])

render_character_beat("S3a_vo04", ["R7_walk_v3"], "04", [("wind_desert_bed",0,0.2,True)])
render_character_beat("S3c_vo05", ["R2_front_medium_v3"], "05", [("wind_desert_bed",0,0.2,True)])
render_character_beat("S3e_vo06", ["R4_turn_v3","R1_closeup_v3"], "06", [("wind_desert_bed",0,0.2,True)])

render_character_beat("S4a_vo07", ["R1_closeup_v3"], "07", [("wind_desert_bed",0,0.2,True)])
render_character_beat("S4c_vo08", ["R2_front_medium_v3","R7_walk_v3"], "08", [("wind_desert_bed",0,0.2,True)])
render_character_beat("S4f_vo09", ["R4_turn_v3"], "09", [("wind_desert_bed",0,0.2,True)])
render_character_beat("S4h_vo10", ["R2_front_medium_v3","R5_low_angle_v3"], "10", [("wind_desert_bed",0,0.2,True)])

render_character_beat("S5a_vo11", ["R1_closeup_v3","R3_wide_power_v3"], "11",
    [("wind_desert_bed",0,0.22,True),("boom_reveal",0.0,0.5,False)])

render_character_beat("S6a_vo12", ["R2_front_medium_v3","R4_turn_v3"], "12", [("wind_desert_bed",0,0.2,True)])
render_character_beat("S6b_vo13", ["R5_low_angle_v3"], "13",
    [("wind_desert_bed",0,0.2,True),("boom_impact2",0.0,0.75,False)])
render_character_beat("S6d_vo14", ["R5_low_angle_v3","R2_front_medium_v3"], "14", [("wind_desert_bed",0,0.2,True)])

render_character_beat("S7a_vo15", ["R8_golden_v3"], "15", [("wind_desert_bed",0,0.24,True)])
render_character_beat("S7b_vo16", ["R1_closeup_v3"], "16", [("wind_desert_bed",0,0.2,True)])
render_character_beat("S7c_vo17", ["R8_golden_v3"], "17", [("wind_desert_bed",0,0.26,True)])

render_character_beat("S8a_vo18", ["R3_wide_power_v3","R4_turn_v3"], "18", [("wind_desert_bed",0,0.2,True)])
render_character_beat("S8b_vo19", ["R2_front_medium_v3"], "19",
    [("wind_desert_bed",0,0.2,True),("rotor_spinup",3.0,0.4,False)])

print("=== RE-SYNC COMPLETE ===")
