from tkinter import *
from tkinter import filedialog
from tkcalendar import DateEntry
import requests,webbrowser
from PIL import ImageTk,Image
from io import BytesIO
from datetime import datetime
curr=datetime.today()
root=Tk()
root.title('APOD Photo Viewer')
root.iconbitmap('rocket.ico')

#define font and colors
fonts=('Times New Roman',14)
blue='#043c93'
lblue='#7aa5d3'
red='#ff1923'
white='#ffffff'
root.config(bg=blue)

#define functions
def getReq():
    global resp
    global date
    url='https://api.nasa.gov/planetary/apod'
    apiKey='Zg4hDVEKorEybWIZ5kAhZBgg6CpjWsbqli4o5rY3'
    date=calendar.get_date()
    calendar.config(maxdate=curr)
    query={'api_key':apiKey,'date':date}
    resp=requests.request('GET',url,params=query)
    resp=resp.json()
    set_info()

def set_info():
    '''
    {
        'date': '2021-02-05',
        'explanation': "Fifty years ago this Sunday (February 7, 1971), the crew of Apollo 14 left lunar orbit and headed for home.
                        They watched this Earthrise from their command module Kittyhawk.
                        With Earth's sunlit crescent just peeking over the lunar horizon, the cratered terrain in the foreground is along the lunar farside.
                        Of course, while orbiting the Moon, the crew could watch Earth rise and set, but from the lunar surface the Earth hung stationary in the sky over their landing site at Fra Mauro Base.
                        Rock samples returned from Fra Mauro included a 20 pound rock nicknamed Big Bertha, determined to contain a likely fragment of a meteorite from planet Earth.
                        Kept on board the Kittyhawk during the Apollo 14 mission was a cannister of 400-500 seeds that were later grown into Moon Trees.",
        'hdurl': 'https://apod.nasa.gov/apod/image/2102/AS14-71-9845v2wmktwtr4Jerry.jpg',
        'media_type': 'image',
        'service_version': 'v1',
        'title': 'Apollo 14 Heads for Home',
        'url': 'https://apod.nasa.gov/apod/image/2102/AS14-71-9845v2wmktwtr4Jerry.jpg'
    }
    '''
    pic_date.config(text=resp['date'])
    pic_exp.config(text=resp['explanation'])
    
    global img
    global thumb
    global full_img
    url=resp['url']
    if resp['media_type']=='image':
        saveb.config(state=NORMAL)
        full.config(state=NORMAL)
        img_resp=requests.get(url,stream=True)
        img_data=img_resp.content
        img=Image.open(BytesIO(img_data))

        full_img=ImageTk.PhotoImage(img)

        thumb_data=img_resp.content
        thumb=Image.open(BytesIO(thumb_data))
        thumb.thumbnail((200,200))
        thumb=ImageTk.PhotoImage(thumb)

        pic.config(image=thumb)
    elif resp['media_type']=='video':
        saveb.config(state=DISABLED)
        full.config(state=DISABLED)
        pic.config(text=url,image='')
        webbrowser.open(url)

def full_photo():
    top=Toplevel()
    top.title('Full APOD PIC')
    top.iconbitmap('rocket.ico')
    img_lbl=Label(top,image=full_img)
    img_lbl.pack()

def save_photo():
    try:
        save_name=filedialog.asksaveasfilename(initialdir='./',title='Save Image',filetypes=(("JPEG", "*.jpg"), ("All Files", "*.*")))
        img.save(save_name+'.jpg')
    except:
        pass

    
#layout
#frames
inp=Frame(root,bg=blue)
out=Frame(root,bg=white)
inp.pack()
out.pack(padx=50,pady=(0,25))

#inp Frame
calendar=DateEntry(inp,width=10,font=fonts,background=blue,foreground=white)
submit=Button(inp,text='Submit',font=fonts,bg=lblue,command=getReq)
full=Button(inp,text='Full Photo',font=fonts,bg=lblue,command=full_photo)
saveb=Button(inp,text='Save Photo',font=fonts,bg=lblue,command=save_photo)
quitb=Button(inp,text='Exit',font=fonts,bg=red,command=root.destroy)

calendar.grid(row=0,column=0,padx=5,pady=10)
submit.grid(row=0,column=1,padx=5,pady=10,ipadx=35)
full.grid(row=0,column=2,padx=5,pady=10,ipadx=25)
saveb.grid(row=0,column=3,padx=5,pady=10,ipadx=25)
quitb.grid(row=0,column=4,padx=5,pady=10,ipadx=25)

#out frame
pic_date=Label(out,text="LOADING...",font=fonts,bg=white)
pic_exp=Label(out,font=fonts,bg=white,wraplength=600)
pic=Label(out)

pic_date.grid(row=1,column=1,padx=10)
pic_exp.grid(row=0,column=0,padx=10,pady=10,rowspan=2)
pic.grid(row=0,column=1,padx=10,pady=10)

getReq()
root.mainloop()
