from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pygame import mixer
import os
import datetime
from mutagen.mp3 import MP3
from PIL import ImageTk
import apiclient
import config

# some global variables to make life easier
track = ''
song_len = 0
mixer.init()


# Script to download song, can include bs4 to scrape search results (take care of dynamic JS) and then use youtube-dl
def download_song(song):
    if len(song) < 5:
        messagebox.showinfo("Message", "Please enter something valid ( > 4 chars)")
        return
    api_key = config.api
    youtube = apiclient.discovery.build('youtube', 'v3', developerKey=api_key)
    req = youtube.search().list(q=song, part='snippet', type='video')
    res = req.execute()
    video_id = res['items'][0]['id']['videoId']
    os.system(
        'youtube-dl -x --audio-format mp3 --audio-quality 0 --output "%(title)s.%(ext)s" '
        'https://www.youtube.com/watch?v=' + video_id)
    messagebox.showinfo("Message", "Downloaded song")


def song_path():
    global track
    track = ''
    track = filedialog.askopenfilename()
    if len(track) > 0:
        # set the text according to names you want to display
        song_label = Label(root, text='-' + track[40:67] + "..", background='#b6d696',
                           font=('arial', 15, 'italic bold'))
        song_label.grid(row=3, column=1, padx=20, pady=20)


def play_music():
    global track, song_len
    try:
        mixer.music.load(track)
        mixer.music.play()
        progress_bar.grid()
        pr_track = MP3(track)
        song_len = int(pr_track.info.length)
        progress_slide['maximum'] = song_len
        progress_bar_ed.configure(text='{}'.format(str(datetime.timedelta(seconds=song_len))))

        def current_position_track():
            curr_pos = mixer.music.get_pos() // 1000
            progress_slide['value'] = curr_pos
            progress_bar_st.configure(text='{}'.format(str(datetime.timedelta(seconds=curr_pos))))
            progress_slide.after(2, current_position_track)

        current_position_track()

    except:
        song_label = Label(root, text="Format not supported", background='#b6d696', font=('arial', 15, 'italic bold'))
        song_label.grid(row=3, column=1, padx=20, pady=20)


def pause_music():
    mixer.music.pause()
    root.pause_button.grid_remove()
    root.resume_button.grid()


def resume_music():
    root.pause_button.grid()
    root.resume_button.grid_remove()
    mixer.music.unpause()


def vol_up():
    vol = mixer.music.get_volume()
    mixer.music.set_volume(vol + 0.1)


def vol_down():
    vol = mixer.music.get_volume()
    mixer.music.set_volume(vol - 0.1)


def stop_music():
    mixer.music.stop()
    progress_bar_st.configure(text='{}'.format(str(datetime.timedelta(seconds=0))))


def widget_data():
    global im_vup, im_vdown, progress_bar, progress_slide, progress_bar_st, progress_bar_ed
    # images
    im_vup = PhotoImage(file='icons/up.png')
    im_vdown = PhotoImage(file='icons/down.png')
    im_vup = im_vup.subsample(12, 12)
    im_vdown = im_vdown.subsample(12, 12)

    # Label
    info_label = Label(root, text='Enter artist and song: ', background='#b6d696', font=('arial', 15, 'italic bold'))
    info_label.grid(row=0, column=0, padx=20, pady=20)

    # Enter the song and artist name
    entry_name = Entry(root, font=('arial', 16, 'italic bold'), width=35)
    entry_name.grid(row=0, column=1, padx=20, pady=20)

    # Buttons
    download_button = Button(root, text='Download', bg='#b6d696', font=('arial', 13, 'italic bold'), width=12, bd=5,
                             activebackground='#26400c', command=lambda: download_song(entry_name.get()))
    download_button.grid(row=0, column=2, padx=20, pady=20)

    open_button = Button(root, text='Open', bg='#b6d696', font=('arial', 13, 'italic bold'), width=12, bd=5,
                         activebackground='#26400c', command=song_path)
    open_button.grid(row=0, column=3, padx=20, pady=20)

    play_button = Button(root, text='Play', bg='#b6d696', font=('arial', 13, 'italic bold'), width=12, bd=5,
                         activebackground='#26400c', command=play_music)
    play_button.grid(row=1, column=0, padx=20, pady=20)

    root.pause_button = Button(root, text='Pause', bg='#b6d696', font=('arial', 13, 'italic bold'), width=12, bd=5,
                               activebackground='#26400c', command=pause_music)
    root.pause_button.grid(row=1, column=1, padx=20, pady=20)

    root.resume_button = Button(root, text='Resume', bg='#b6d696', font=('arial', 13, 'italic bold'), width=12, bd=5,
                                activebackground='#26400c', command=resume_music)
    root.resume_button.grid(row=1, column=1, padx=20, pady=20)
    root.resume_button.grid_remove()

    vup_button = Button(root, text='', bg='#b6d696', font=('arial', 13, 'italic bold'), width=55, bd=5,
                        activebackground='#26400c', image=im_vup, compound=RIGHT, command=vol_up)
    vup_button.grid(row=1, column=2, padx=20, pady=20)

    vdown_button = Button(root, text='', bg='#b6d696', font=('arial', 13, 'italic bold'), width=55, bd=5,
                          activebackground='#26400c', image=im_vdown, compound=RIGHT, command=vol_down)
    vdown_button.grid(row=1, column=3, padx=20, pady=20)

    stop_button = Button(root, text='Stop', bg='#b6d696', font=('arial', 13, 'italic bold'), width=12, bd=5,
                         activebackground='#26400c', command=stop_music)
    stop_button.grid(row=2, column=1, padx=20, pady=20)

    # show the progress bar for the song played till now
    progress_bar = Label(root, text='', bg='#b6d696')
    progress_bar.grid(row=4, column=0, columnspan=4, padx=20, pady=20)
    progress_bar_st = Label(progress_bar, text='0:00:0', bg='#b6d696')
    progress_bar_st.grid(row=4, column=0)
    progress_slide = Progressbar(progress_bar, orient=HORIZONTAL, mode='determinate', value=50)
    progress_slide.grid(row=4, column=1, ipadx=335, ipady=2)
    progress_bar_ed = Label(progress_bar, text='0:00:0', bg='#b6d696')
    progress_bar_ed.grid(row=4, column=2)
    progress_bar.grid_remove()

# use when need to fit bg image acc to window size
def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_img.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    bck_label.config(image=photo)
    bck_label.image = photo  # avoid garbage collection


root = Tk()
back_img = PhotoImage(file='icons/dark.png')
back_img = back_img.subsample(1, 1)
# back_img = Image.open('icons/dark.png')
# copy_img = back_img.copy()
# photo = ImageTk.PhotoImage(back_img)
bck_label = Label(root, image=back_img)
# bck_label.bind('<Configure>', resize_image)
# bck_label.pack(fill=BOTH, expand=YES)
bck_label.grid(row=0, column=0, rowspan=6, columnspan=6, padx=20, pady=20)
root.geometry('1080x600+200+50')
root.title('DownPlayer....')
# root.iconbitmap('icon.ico')
root.resizable(False, False)
root.configure(bg='black')
widget_data()
root.mainloop()
