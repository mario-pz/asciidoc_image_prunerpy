.PHONY: all clean craft

all:
	python3 main.py

craft:
	mkdir -p demo-1/assets demo-2/assets demo-1/demo-3/assets
	touch ./demo-1/assets/yes.png
	touch ./demo-1/assets/should-move-to-unused-1.png
	touch ./demo-2/assets/should-move-to-unused-2.png
	touch ./demo-1/demo-3/assets/should-move-to-unused-3.png
	cat ./demo.asciidoc > ./demo-1/demo.asciidoc

clean:
	rm -rf unused-images demo-1 demo-2
