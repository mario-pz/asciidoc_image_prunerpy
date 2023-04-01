.PHONY: all clean craft

all:
	python3 main.py

craft:
	mkdir -p demo-1/assets demo-2/assets
	touch ./demo-1/assets/yes.png
	touch ./demo-1/assets/should-move-to-unused.png
	touch ./demo-2/assets/should-move-to-unused.png

clean:
	rm -rf unused-images
