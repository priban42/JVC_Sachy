# Might need to run these

# pip install speechrecognition
# sudo apt-get install python3-pyaudio
# pip install pyaudio
# pip install pyttsx3

import speech_recognition as sr
import pyttsx3


class VoiceControl:

    def __init__(self, debug=False):
        """
        VoiceControl initialization

        :param debug: default False | enables prints for debug
        """
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.debug = debug
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]

    def get_coordinates_times(self, max_times=2, info=True):
        """
            COORDINATES ARE RETURNED IN ORDER AS THEY WERE SAID

            E.g. move from A1 to A2 is ((0, 0), (0, 1))

            :param max_times: how many times maximum the function tries to __listen() (user will be notifies each time
                                                                                        to speak if info = True)
            :param info: True to print information for user, default True
            :return: tuple ((0, 0), (0, 1)) if found else False
        """
        for i in range(max_times):                                          # listen for max_times
            text = self.__listen(info)
            if text:                                                        # User said something
                num_cords = self.__analyze_text(text, info)
                if num_cords:
                    return num_cords
        return False                                                        # not possible to get coordinates

    def __analyze_text(self, text, info):
        """
        Gets move coordinates from user text

        :param text: text from user in str format
        :param info: default True, print information for user
        :return: tuple E.g. ((0, 0), (0, 1)) if found else False
        """
        coordinates = []
        numeric_coordinates = []
        for l in range(len(self.letters)):                                  # try to find all combinations of numbers
            for n in range(len(self.numbers)):                              # and letters from board
                c = self.letters[l] + self.numbers[n]
                if c in text:
                    coordinates.append(c)
                    tup = (l, n)
                    numeric_coordinates.append(tup)
        if len(coordinates) == 2:                                           # two coordinates were found, firs said
            if text.find(coordinates[0]) > text.find(coordinates[1]):       # first in tuple
                coordinates[0], coordinates[1] = coordinates[1], coordinates[0]
                numeric_coordinates[0], numeric_coordinates[1] = numeric_coordinates[1], numeric_coordinates[0]
            board_cords = (coordinates[0].upper(), coordinates[1].upper())
            num_cords = (numeric_coordinates[0], numeric_coordinates[1])
            if info:
                print("VoiceControl recognised move {}".format(board_cords))
            if self.debug:
                print("VoiceControl recognised move {}".format(num_cords))
            return num_cords
        return False

    def __listen(self, info=True):
        """
        Listens for user input once (takes about 5 seconds)

        :param info: default True | print info for user
        :return: str format of user spoken input
        """
        try:
            with sr.Microphone() as source:
                if info:
                    print("You can speak in a second")
                self.r.adjust_for_ambient_noise(source, duration=1)         # Surroundings adjustment
                if info:
                    print("You can speak")

                audio = self.r.listen(source)                               # Listen for user input

                text = self.r.recognize_google(audio).lower()               # Google text recognition

                if self.debug:
                    print("Did you say ", text)
                return text

        except sr.RequestError as e:                                        # Server connection error
            print("ERROR: VoiceControl - request not possible; {0}".format(e))

        except sr.UnknownValueError:                                        # Anything else
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
    voice_control = VoiceControl(debug=False)
    # commands in english, can be said anything containing the two coordinates FIRST where we start SECOND where we go
    # E.g. move this from A3 to maybe A4, will return ((0, 2), (0, 3))
    # 
    move_num = voice_control.get_coordinates_times(3, info=True)
    print(move_num)
    voice_control.SpeakText("Text to be said.", speed=150)

