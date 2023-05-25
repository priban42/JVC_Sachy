from pocketsphinx import LiveSpeech
import threading
import queue


class SpeechToMoves():
    LETTERS = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "eight":0}
    NUMBERS = {"one": 0, "two": 1, "three": 2, "four": 3, "five": 4, "six": 5, "seven": 6, "eight": 7}
    def __init__(self, dict_path="coordinates.dict"):
        self.speech = LiveSpeech(dict=dict_path)
        self.buffer = queue.Queue()
        self.coord_assembly = queue.Queue()
        self.last_time = 0
        self.running = False
        self.thread = None
        self._lock = threading.Lock()


    def phrase_to_command(self, phrase):
        splited = str(phrase).split(" ")
        if len(splited) != 4:
            return None
        if splited[0] not in SpeechToMoves.LETTERS or splited[1] not in SpeechToMoves.NUMBERS:
            return None
        if splited[2] not in SpeechToMoves.LETTERS or splited[3] not in SpeechToMoves.NUMBERS:
            return None
        print(splited)
        command = ((SpeechToMoves.LETTERS[splited[0]], SpeechToMoves.NUMBERS[splited[1]]),
                   (SpeechToMoves.LETTERS[splited[2]], SpeechToMoves.NUMBERS[splited[3]]))
        return command
    def available(self):
        return not self.buffer.empty()
    def get_next_coordinate(self):
            return self.buffer.get()
    def check_phrase(self):
        for phrase in self.speech:
            print(phrase)
            self.buffer.put(self.phrase_to_command(phrase))
            if not self.running:
                return

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.check_phrase)
            self.thread.start()

    def close(self):
        if self.running:
            self.running = False
            self.thread.join()

def main():
    spt = SpeechToMoves()
    spt.start()
    while(1):
        if spt.available():
            print(spt.get_next_coordinate())

if __name__ == "__main__":
    main()