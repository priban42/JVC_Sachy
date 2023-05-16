# Might need to run these

# pip install speechrecognition
# sudo apt-get install python3-pyaudio
# pip install pyaudio
# pip install pyttsx3

import speech_recognition as sr
import pyttsx3
import time
import threading


class VoiceControl(threading.Thread):

    def __init__(self, debug=False, recordTime=5, info=True, lan="en-US"):
        """
        VoiceControl initialization

        :param debug: default False | enables prints for debug

        :param recordTime: default 5 seconds | how long user input will be recorded each time

        :param info: default True | print info for user

        :param lan: default "en-US" | set "cs-CZ" for czech other languages can be found here
        https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
        """
        threading.Thread.__init__(self)
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.debug = debug
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.data = ()
        self.dataReady = False
        self.runControl = True
        self.recordTime = recordTime
        self.info = info
        self.lan = lan

    def run(self):
        while self.runControl:
            while not self.dataReady and self.runControl:
                temp_data = self.get_coordinates_times(1)
                if temp_data:
                    self.data = temp_data
                    self.dataReady = True
                else:
                    if self.info:
                        if self.lan == "cs-CZ":
                            print("Z vašeho příkazu nebyl rozpoznán tah")
                        else:
                            print("Move not recognised from your command")

    def read_data(self):
        """
        Returns recognised move from user voice command

        :return: returns data or False if function called when data not ready
        """
        if self.dataReady:
            self.dataReady = False
            return self.data
        else:
            if self.debug:
                print("VoiceControl.read_data called when data not ready")
            return False

    def get_coordinates_times(self, max_times=2):
        """
            COORDINATES ARE RETURNED IN ORDER AS THEY WERE SAID

            E.g. move from A1 to A2 is ((0, 0), (0, 1))

            :param max_times: how many times maximum the function tries to __listen() (user will be notifies each time
                                                                                        to speak if info = True)
            :return: tuple ((0, 0), (0, 1)) if found else False
        """
        for i in range(max_times):  # listen for max_times
            text = self.__listen()
            if text:  # User said something
                num_cords = self.__analyze_text(text)
                if num_cords:
                    return num_cords
        return False  # not possible to get coordinates

    def __analyze_text(self, text):
        """
        Gets move coordinates from user text

        :param text: text from user in str format

        :return: tuple E.g. ((0, 0), (0, 1)) if found else False
        """
        coordinates = []
        numeric_coordinates = []
        for l in range(len(self.letters)):  # try to find all combinations of numbers
            for n in range(len(self.numbers)):  # and letters from board
                c = self.letters[l] + self.numbers[n]
                if c in text:
                    coordinates.append(c)
                    tup = (l, n)
                    numeric_coordinates.append(tup)
        if len(coordinates) == 2:  # two coordinates were found, firs said
            if text.find(coordinates[0]) > text.find(coordinates[1]):  # first in tuple
                coordinates[0], coordinates[1] = coordinates[1], coordinates[0]
                numeric_coordinates[0], numeric_coordinates[1] = numeric_coordinates[1], numeric_coordinates[0]
            board_cords = (coordinates[0].upper(), coordinates[1].upper())
            num_cords = ((numeric_coordinates[0][1], numeric_coordinates[0][0]), (numeric_coordinates[1][1], numeric_coordinates[1][0]))
            if self.info:
                if self.lan == "cs-CZ":
                    print("Byl rozpoznán tah {}".format(board_cords))
                else:
                    print("VoiceControl recognised move {}".format(board_cords))
            if self.debug:
                print("VoiceControl recognised move {}".format(num_cords))
            return num_cords
        return False

    def __listen(self):
        """
        Listens for user input once (takes about 5 seconds)

        :return: str format of user spoken input
        """
        try:
            with sr.Microphone() as source:
                if self.info:
                    if self.lan == "cs-CZ":
                        print("Za vteřinu můžete mluvit")
                    else:
                        print("You can speak in a second")
                self.r.adjust_for_ambient_noise(source, duration=0.4)  # Surroundings adjustment
                if self.info:
                    if self.lan == "cs-CZ":
                        print("Můžete mluvit")
                    else:
                        print("You can speak")

                audio = self.r.record(source, duration=self.recordTime)  # Listen for user input

                text = self.r.recognize_google(audio, language=self.lan).lower()  # Google text recognition

                if self.info:
                    if self.lan == "cs-CZ":
                        print("Slyšel jsem ", text)
                        print("Zpracovávám příkaz")
                    else:
                        print("I heard", text)
                        print("Processing yor command")
                time.sleep(1)
                return text

        except sr.RequestError as e:  # Server connection error
            print("ERROR: VoiceControl - request not possible; {0}".format(e))

        except sr.UnknownValueError:  # Anything else
            print("ERROR: VoiceControl - unknown")

    def SpeakText(self, command, speed=150):
        """
        Text to speech

        :param command: String format of text to say
        :param speed: Default 150 | Sets speed of talking
        """
        self.engine.setProperty('rate', speed)
        self.engine.say(command)
        self.engine.runAndWait()


if __name__ == "__main__":
    # commands in english, can be said anything containing the two coordinates FIRST where we start SECOND where we go
    # E.g. move this from A3 to maybe A4, will return ((0, 2), (0, 3))
    voice_control = VoiceControl(debug=True, info=True, recordTime=4, lan="en-US")  # initialize
    voice_control.start()

    # sample code
    cnt = 0
    while True:
        if cnt >= 2:
            print("quiting")
            voice_control.runControl = False
            voice_control.join(1)
            exit()
        if voice_control.dataReady:
            # use voice_control.read_data() to get the loaded data NOT voice_control.data
            move_num = voice_control.read_data()
            print(move_num)
            # voice_control.SpeakText(str(move_num))     # talks to user
            cnt += 1
