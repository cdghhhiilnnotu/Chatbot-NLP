from tkinter import *
import speech_recognition
import pyttsx3
from chatbot import get_response

# Các biến mặc định sử dụng trong thiết kế giao diện
APP_WIDTH = 375
APP_HEIGHT = 512
BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
BOT_NAME = 'TTwo'


# Tạo lớp đối tượng sử dụng giao điện chatbot
class ChatBotApplication:
    # Initialize App
    # Khởi tạo đối tượng
    def __init__(self):
        # Tạo đối tượng Tkinter để thiết kế GUI App
        self.app = Tk()
        # Thiết lập các thông số, thành phần cho App
        self._setup_win_app()

    # Hàm thiết lập thông số, thành phần của app
    def _setup_win_app(self):
        # Tạo cửa sổ và điều chỉnh vị trí
        # Tính toán vị trí cho cửa số app
        ws = self.app.winfo_screenwidth()
        hs = self.app.winfo_screenheight()
        x = (ws / 2) - (APP_WIDTH / 2)
        y = (hs / 2) - (APP_HEIGHT / 2) - 30
        # Cài đặt icon cho app
        self.app.iconbitmap('Assets/app.ico')
        # Cài đặt tên của app
        self.app.title('Chat Bot Application')
        # Cài đặt kích thước và vị trí của cửa sổ app
        self.app.geometry('%dx%d+%d+%d' % (APP_WIDTH, APP_HEIGHT, x, y))

        # Tạo phần GUI nhận diện giọng nói
        self.talk = Canvas(self.app, height=200, bg='black')
        self.talk.pack()
        # Tạo nút bật tính năng năng nhận diện giọng nói
        micimg = PhotoImage(file=r'Assets/mic.png')
        self.speakbtn = Button(self.talk, width=35, height=35, image=micimg, bd=1, command=self._onmic)
        self.speakbtn.image = micimg
        self.speakbtn.place(x=170, y=83)

        # Tạo phần GUI chat với chatbot
        self.chat = Canvas(self.app, bg=BG_GRAY)
        self.chat.pack()
        # -Tạo phần hiển thị cuộc trò chuyện với chatbot
        self.outtext = Text(self.chat, height=12, bg=BG_COLOR, fg=TEXT_COLOR,
                            font=('Courier', 13, 'bold'), state=DISABLED, pady=10, padx=20, wrap=WORD)
        self.outtext.pack()
        # -Tạo thanh cuộn để cho phần hiển thị cuộc trò chuyện
        outpscr = Scrollbar(self.outtext)
        outpscr.place(height=257, relx=1.0045, y=-9)
        outpscr.configure(command=self.outtext.yview, cursor='arrow')

        # Tạo phần nhập câu hỏi trò chuyện
        self.inputarea = Canvas(self.app, bg='gray')
        self.inputarea.pack()
        # -Tạo ô nhập
        self.intext = Text(self.inputarea, width=32, height=2,
                           fg='black', font=('Courier', 12, 'bold'), wrap=WORD)
        self.intext.place(x=3, y=2)
        self.intext.bind('<Return>', self._sendmsg)
        # -Tạo nút gửi tin nhắn
        sendimg = PhotoImage(file=r'Assets/send.png')
        self.sendbtn = Button(self.inputarea, width=35, height=35, image=sendimg, command=lambda: self._sendmsg(None))
        self.sendbtn.image = sendimg
        self.sendbtn.place(x=330, y=2)

    # Hàm chạy app
    def run(self):
        # Tạo vòng lặp hiển thị app
        self.app.mainloop()

    # Hàm gửi tin nhắn
    def _sendmsg(self, event):
        # Lấy tin nhắn từ inputtextbox
        message = self.intext.get('1.0', 'end-1c').strip().replace("\n", "")
        # Nếu inputtext trống thì không nhận tin nhắn
        if message != '':
            self._getmsg(message)
        # Xóa dấu \n sau khi enter
        return "break"

    # Hàm nhận tin nhắn người dùng từ inputtextbox
    def _getmsg(self, msg):
        # Xóa chữ trong inputextbox
        self.intext.delete('1.0', 'end-1c')
        # In tin nhắn ra outputtextbox
        msg1 = f'You: {msg}\n'
        self.outtext.configure(state=NORMAL)
        self.outtext.insert(END, msg1)
        self.outtext.configure(state=DISABLED)
        # Sau khi in tin nhắn thì tìm và in câu trả lời
        self.app.after(1, lambda: self._prinresponses(msg))

    # Hàm hiển thị câu trả lời của chatbot
    def _prinresponses(self, msg):
        # Tìm kiếm câu trả lời của chatbot
        res = get_response(msg)
        # Tạo giọng nói cho cho chatbot
        engine = pyttsx3.init()
        voice = engine.getProperty('voices')
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')

        # In ra câu trả lời
        msg2 = f'{BOT_NAME}: {res}\n'
        self.outtext.configure(state=NORMAL)
        self.outtext.insert(END, msg2)
        self.outtext.configure(state=DISABLED)
        self.outtext.see('end')

        # Đọc câu trả lời
        engine.say(res)
        engine.runAndWait()

    # Hàm mở mic nhận diện giọng nói
    def _onmic(self):
        # Tạo đối tượng nhận diện giọng nói và nhận diện giọng nói
        engine = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as mic:
            print(f'{BOT_NAME} is listening')
            audio = engine.listen(mic)
        # Cố gắng nhận diện giọng nói, nếu ko được thì trả msg = ''
        try:
            msg = engine.recognize_google(audio)
        except:
            msg = ''
        # Nếu nhận được giọng nói thì nhận tin nhắn
        if msg != '':
            self._getmsg(msg)


# if __name__ == '__main__':
app = ChatBotApplication()
app.run()
