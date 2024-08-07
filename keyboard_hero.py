import os, sys
import random
import pygame as pg
import time

if getattr(sys, 'frozen', False):
    filepy = sys.executable
else:
    filepy = sys.argv[0]
fullpath = os.path.abspath(filepy)

dir_and_name = os.path.split(fullpath)

bass_dir = dir_and_name[0] + '/data/B'
key_dir = dir_and_name[0] + '/data/K'
drum_dir = dir_and_name[0] + '/data/D'

pg.init()
pg.font.init()

bg = pg.image.load(dir_and_name[0] + "/data/background.png")

font = pg.freetype.Font("data/NotoSans-Regular.ttf", 13)

wave_noise = dir_and_name[0] + '/data/noise.wav'
noise_snd = pg.mixer.Sound(wave_noise)

b_items = os.listdir(bass_dir)
bass_sounds = []
for fld_smpl in b_items:
    number = fld_smpl.split('_')[0]
    wave_path = bass_dir + '/' + fld_smpl + '/_.wav'
    snd = pg.mixer.Sound(wave_path)
    snd.set_volume(0.0)
    bass_sounds.append(snd)

k_items = os.listdir(key_dir)
key_sounds = []
for fld_smpl in k_items:
    number = fld_smpl.split('_')[0]
    wave_path = key_dir + '/' + fld_smpl + '/_.wav'
    snd = pg.mixer.Sound(wave_path)
    snd.set_volume(0.0)
    key_sounds.append(snd)

d_items = os.listdir(drum_dir)
drum_sounds = []
for fld_smpl in d_items:
    number = fld_smpl.split('_')[0]
    wave_path = drum_dir + '/' + fld_smpl + '/_.wav'
    snd = pg.mixer.Sound(wave_path)
    snd.set_volume(1)
    drum_sounds.append(snd)
drum_sounds.append(snd)

screen = pg.display.set_mode((599, 281))

glob_volume = 1

mult_vol = 1.0

pg.display.set_caption("Keyboard Hero")
clock = pg.time.Clock()

pg.mixer.pre_init(44100,-16,2, 1024)
pg.mixer.set_num_channels(50)

def to_mute_all_keys(list_keys):
    i = 0
    for k in list_keys:
        list_keys[i] = 1
        i+=1

def tempo_estimate_by_3(time_list):
    if len(time_list) == 3:
        interval_1 =  time_list[1] - time_list[0]
        interval_2 =  time_list[2] - time_list[1]
        interval = (interval_1+interval_2) / 2
        temp = float(int((60/interval)*100))/100
    return temp

def bpm_to_ms(bpm):
    ms = 60000.0/bpm
    return ms

rythm = 68
time_taped = []
metronome_is_play = False
METROEBENT = pg.USEREVENT + 1
pg.time.set_timer(METROEBENT, int(bpm_to_ms(rythm)), -1)

def metroplaymode():
    sleep_h = random.uniform(0.002, 0.006)
    sleep_o = random.uniform(0.002, 0.006)
    rnd_koef = random.uniform(0.05, 0.08)
    drum_sounds[0].set_volume(rnd_koef*mult_vol)
    drum_sounds[0].play() #  BASS
    time.sleep(sleep_h)
    #rnd_koef = random.uniform(0.06, 0.08)
    #drum_sounds[7].set_volume(rnd_koef*mult_vol)
    #drum_sounds[7].play() #  openHiHAT
    #time.sleep(sleep_o)
    rnd_koef = random.uniform(0.09, 0.13)
    drum_sounds[3].set_volume(rnd_koef*mult_vol)
    drum_sounds[3].play() #  RING
    

type_duration = True  # for notes 0 is short 1 standart 2 is long with Enter chenged
capslock = pg.key.get_mods() & pg.KMOD_CAPS
if capslock:
    type_duration_long = False
else:
    type_duration_long = True
octave_shift = 0
octave_bass_shift = 0

def play_bass_note(picth, bass_sounds, bass_to_activate_list):
    picth -= 12
    if octave_bass_shift:
        picth += 12
    i = 0
    noise_snd.stop()
    for b in bass_sounds:
        bass_sounds[i].stop()
        i+=1
    bass_sounds[picth].set_volume(0.82*mult_vol)
    bass_sounds[picth].play()
    bass_to_activate_list[picth] = 2
    rnd_koef = random.uniform(0.1, 0.3)
    noise_snd.set_volume(rnd_koef*mult_vol)
    noise_snd.play()

to_print = ''
keys_to_activate_list = [0] * 41
keys_type_sustain_list = [0] * 41
keys_volumes_list = [0] * 41
key_max_vol =  [0.8] * 41

def play_key_note(pitch_note, keys_to_activate_list, keys_type_sustain_list, key_sounds ):
    if octave_shift == -1: pitch_note -= 12
    if octave_shift == 1: pitch_note += 12
    keys_to_activate_list[pitch_note] = 2
    keys_type_sustain_list[pitch_note] = type_duration_long
    key_sounds[pitch_note].stop()
    key_sounds[pitch_note].play(loops=-1)
    rnd_koef = random.uniform(0.26, 0.6)
    key_max_vol[pitch_note] = rnd_koef*mult_vol

def realize_key_note(pitch_note, keys_to_activate_list):
    if octave_shift == -1: pitch_note -= 12
    if octave_shift == 1: pitch_note += 12
    keys_to_activate_list[pitch_note] = 1

# when key add to this tuple (picth, tick_life)
bass_to_activate_list = [0] * 28
bass_volumes_list = [0] * 28
long_sustein = 0
r_koef_volume = 1
bass_mode = False
ecs_pressed_mute = False
clock.tick(2000)
first_tic = True
i = 0
n = 0
m = 0
update_metro = 0
metro_int = 1



run = True

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == METROEBENT:
            if update_metro:
                pg.time.set_timer(METROEBENT, int(bpm_to_ms(rythm)), -1)
            n +=1
            if n > 5:
                to_print = ''
                n = 0
            i += 1
            if m == 0:
                m += 1
            else:
                m = 0
            if i > 10:
                time_taped = []
                i = 0
            if metronome_is_play:
                metroplaymode()
                if metro_int:
                    to_print = '####################              ' + to_print
                    metro_int = 0
                else:
                    to_print = '.              ' + to_print
                    metro_int = 1
            else:
                pass
 
        if event.type == pg.KEYDOWN and event.key == pg.K_CAPSLOCK:
            capslock = pg.key.get_mods() & pg.KMOD_CAPS
            # ?SET TO CAPS LOCK for use bass or not
            if capslock:
                type_duration_long = False
                to_print = 'LONG sustain notes [0]              ' + to_print
            else:
                type_duration_long = True
                to_print = 'SHORT sustain notes [1]              ' + to_print

        if event.type == pg.KEYDOWN and event.key == pg.K_LALT:
            ecs_pressed_mute = True
            i = 0
            noise_snd.stop()
            drum_sounds[3].stop()
            drum_sounds[7].stop()
            for b in bass_sounds:
                bass_sounds[i].stop()
                i+=1

        if event.type == pg.KEYDOWN and event.key == pg.K_PAGEUP:
            mult_vol = 1.0
            to_print = 'VOL_NORMAL              ' + to_print
        if event.type == pg.KEYDOWN and event.key == pg.K_PAGEDOWN:
            mult_vol = 0.55555
            to_print = 'VOL_SILENT              ' + to_print
        
        if event.type == pg.KEYUP and event.key == pg.K_LALT:
            ecs_pressed_mute = False

        if event.type == pg.KEYDOWN and event.key == pg.K_LCTRL:
            to_mute_all_keys(keys_to_activate_list)
            bass_mode = True
            to_print = 'BASS_LINE_NORMAL              ' + to_print
            octave_bass_shift = 0
        if event.type == pg.KEYDOWN and event.key == pg.K_LSHIFT:
            to_mute_all_keys(keys_to_activate_list)
            bass_mode = True
            to_print = 'BASS_LINE_ON_HIGH              ' + to_print
            octave_bass_shift = 1

        if event.type == pg.KEYDOWN and event.key == pg.K_RALT:
            bass_mode = False
            to_print = 'BASSLINE_OFF              ' + to_print
            octave_shift = -1
            to_mute_all_keys(keys_to_activate_list)
            bass_mode = False
            to_print = 'octave +LOW              ' + to_print

        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            bass_mode = False
            to_print = 'BASSLINE_OFF              ' + to_print
            octave_shift = 1
            to_mute_all_keys(keys_to_activate_list)
            to_print = 'octave +HIGHT              ' + to_print

        if event.type == pg.KEYDOWN and event.key == pg.K_TAB:
            bass_mode = False
            to_print = 'BASSLINE_OFF              ' + to_print
            octave_shift = 0
            to_mute_all_keys(keys_to_activate_list)
            to_print = 'octave NORMAL              ' + to_print

        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: #: # HIHAT CLOSED
            rnd_koef = random.uniform(0.25, 0.45)
            drum_sounds[1].set_volume(rnd_koef*mult_vol)
            drum_sounds[7].stop()
            drum_sounds[1].play()
            
        if event.type == pg.KEYDOWN and event.key == pg.K_DOWN: #pg.K_BACKSPACE: # HIHAT OPEN
            #rnd_koef = random.uniform(0.78, 0.86)
            drum_sounds[7].set_volume(0.16*mult_vol)
            drum_sounds[7].play()

        if  event.type == pg.KEYDOWN and (event.key  == pg.K_LEFT or event.key == pg.K_END): # BASS
            rnd_koef = random.uniform(0.22, 0.43)
            drum_sounds[0].set_volume(rnd_koef*mult_vol)
            drum_sounds[0].play()

        if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE: # START STOP BASS
            if metronome_is_play:
                metronome_is_play = False
                to_print = 'BASS RYTHM STOP tempo '+str(rythm)+'    ms:'+ str(bpm_to_ms(rythm)) +'              ' + to_print
                pg.time.set_timer(METROEBENT, 0)
            else:
                metronome_is_play = True
                pg.time.set_timer(METROEBENT, 0)
                to_print = 'BASS RYTHM PLAY tempo '+str(rythm)+'    ms:'+ str(bpm_to_ms(rythm)) +'              ' + to_print
                pg.time.set_timer(METROEBENT, int(bpm_to_ms(rythm)), -1)
                metroplaymode()

        if event.type == pg.KEYDOWN and (event.key == pg.K_DELETE):
            lll = len(time_taped)
            if lll < 3:
                to_print = str(lll+1)+' <- 4 TAPs (for tempo)...              ' + to_print
                dt = time.time()
                time_taped.append(dt)
            else:
                r = tempo_estimate_by_3(time_taped)
                rythm = r
                to_print = 'tempo '+str(rythm)+'    ms:'+ str(bpm_to_ms(rythm)) +'              ' + to_print
                pg.time.set_timer(METROEBENT, int(bpm_to_ms(rythm)), -1)
                time_taped = []
        
        if event.type == pg.KEYDOWN and (event.key == pg.K_RIGHT or event.key == pg.K_UP): # SNARE
            rnd_koef = random.uniform(0.14, 0.24)
            drum_sounds[2].set_volume(rnd_koef*mult_vol)
            drum_sounds[2].play()

        if event.type == pg.KEYDOWN and event.key == pg.K_BACKSLASH: # RING to Shift
            rnd_koef = random.uniform(0.09, 0.3)
            drum_sounds[3].set_volume(rnd_koef*mult_vol)
            drum_sounds[3].play()

        # Latin_precusia  K_RETURN
        if event.type == pg.KEYDOWN and event.key == pg.K_RCTRL: # hi Perc
            rnd_koef = random.uniform(0.17, 0.47)
            drum_sounds[6].set_volume(rnd_koef*mult_vol)
            drum_sounds[6].play()
        if event.type == pg.KEYDOWN and event.key == pg.K_RSHIFT: # click perc
            rnd_koef = random.uniform(0.17, 0.47)
            drum_sounds[5].set_volume(rnd_koef*mult_vol)
            drum_sounds[5].play()
        #if event.type == pg.KEYDOWN and event.key == pg.K_RCTRL:
        #    rnd_koef = random.uniform(0.55, 0.85)
        #    drum_sounds[5].set_volume(rnd_koef)
        #    drum_sounds[5].play()
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN: # low perc
            rnd_koef = random.uniform(0.17, 0.47)
            drum_sounds[4].set_volume(rnd_koef*mult_vol)
            drum_sounds[4].play()    
        
        # BASS buttons :   ZXCBNM<>?ASDFGHJKL:""
        if event.type == pg.KEYDOWN and event.key == pg.K_z:
            play_bass_note(12, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_x:
            play_bass_note(13, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_c:
            play_bass_note(14, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_v:
            play_bass_note(15, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_b:
            play_bass_note(16, bass_sounds, bass_to_activate_list)
        
        if event.type == pg.KEYDOWN and event.key == pg.K_n:
            play_bass_note(17, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_m:
            play_bass_note(18, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_COMMA:
            play_bass_note(19, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_PERIOD:
            play_bass_note(20, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_SLASH:
            play_bass_note(21, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_a:
            play_bass_note(17, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_s:
            play_bass_note(18, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_d:
            play_bass_note(19, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_f:
            play_bass_note(20, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_g:
            play_bass_note(21, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_h:
            play_bass_note(22, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_j:
            play_bass_note(23, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_k:
            play_bass_note(24, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_l:
            play_bass_note(25, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_SEMICOLON:
            play_bass_note(26, bass_sounds, bass_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_QUOTE:
            play_bass_note(27, bass_sounds, bass_to_activate_list)

        # Organs
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            play_key_note(12, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_q:
            realize_key_note(12, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_w:
            play_key_note(13, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_w:
            realize_key_note(13, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_e:
            play_key_note(14, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_e:
            realize_key_note(14, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_r:
            play_key_note(15, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_r:
            realize_key_note(15, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_t:
            play_key_note(16, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_t:
            realize_key_note(16, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_y:
            play_key_note(17, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_y:
            realize_key_note(17, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_u:
            play_key_note(18, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_u:
            realize_key_note(18, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_i:
            play_key_note(19, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_i:
            realize_key_note(19, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_o:
            play_key_note(20, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_o:
            realize_key_note(20, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_p:
            play_key_note(21, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_p:
            realize_key_note(21, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_LEFTBRACKET:
            play_key_note(22, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_LEFTBRACKET:
            realize_key_note(22, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_RIGHTBRACKET:
            play_key_note(23, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_RIGHTBRACKET:
            realize_key_note(23, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_1:
            play_key_note(17, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_1:
            realize_key_note(17, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_2:
            play_key_note(18, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_2:
            realize_key_note(18, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_3:
            play_key_note(19, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_3:
            realize_key_note(19, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_4:
            play_key_note(20, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_4:
            realize_key_note(20, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_5:
            play_key_note(21, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_5:
            realize_key_note(21, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_6:
            play_key_note(22, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_6:
            realize_key_note(22, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_7:
            play_key_note(23, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_7:
            realize_key_note(23, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_8:
            play_key_note(24, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_8:
            realize_key_note(24, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_9:
            play_key_note(25, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_9:
            realize_key_note(25, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_0:
            play_key_note(26, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_0:
            realize_key_note(26, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_MINUS:
            play_key_note(27, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_MINUS:
            realize_key_note(27, keys_to_activate_list)

        if event.type == pg.KEYDOWN and event.key == pg.K_EQUALS:
            play_key_note(28, keys_to_activate_list, keys_type_sustain_list, key_sounds )
        if event.type == pg.KEYUP and event.key == pg.K_EQUALS:
            realize_key_note(28, keys_to_activate_list)

    # each tic check activates list
    index = -1
    for k in keys_to_activate_list:
        index += 1
        if k == 2:
            if keys_volumes_list[index] < key_max_vol[index]:
                keys_volumes_list[index] += 0.03
                key_sounds[index].set_volume(keys_volumes_list[index])
        if k == 1:
            if keys_volumes_list[index] > 0:
                sustain = 0.008
                if  keys_type_sustain_list[index]:
                    sustain = 0.00003
                if ecs_pressed_mute:
                    sustain = 0.004
                keys_volumes_list[index] -= sustain
                key_sounds[index].set_volume(keys_volumes_list[index])
        if keys_volumes_list[index] <= 0:
            key_sounds[index].stop()
    index = -1

    if first_tic:
        first_tic = False
        screen.fill((155, 155, 155))
        screen.blit(bg, (0, 0))
        pg.display.flip()
    
    if '              ' in to_print:
        screen.fill((155, 155, 155))
        screen.blit(bg, (0, 0))
        to_print = to_print.split('             ')[0]

        font.render_to(screen, (80, 20), to_print, (255, 255, 255))
        pg.display.flip()
pg.quit()
