import json
import time
from GoogleTranslator import GoogleTranslator
def main():
    translator = GoogleTranslator()
    count = 0

    with open("input.txt","r", encoding="utf-8") as fo:
        lines = fo.readlines()

    with open('output.txt', 'w', encoding='utf-8') as df:
        for line in lines:
            if len(line) > 1:
                count += 1
                print('\r' + str(count), end = '', flush = True)
                df.write(line.strip() + "\n")
                result = translator.translate(line)
                df.write(result.strip() + "\n\n")

if __name__ == "__main__":
	startTime = time.time()
	main()
	print()
	print('%.2f seconds' % (time.time() - startTime))