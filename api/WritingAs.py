import time


class WritingAs:
    def play(self, line, console):
        pass


class WritingAsTypewriter(WritingAs):
    def play(self, buffer, line, bufferreplace_func):
        rendered = ""
        for char in line:
            rendered += char
            bufferreplace_func(f"{buffer} {rendered}\n")
            time.sleep(0.05)
        return line
