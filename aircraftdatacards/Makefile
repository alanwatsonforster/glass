.SUFFIXES: .json .pdf

.json.pdf:
	python3 aircraftdatacards.py $*.json

all			:	all.pdf

all.pdf		:	.FORCE

working.pdf	:	.FORCE

format		:
	python3 format.py

push-descriptions:
	python3 push-descriptions.py

pull-descriptions:
	python3 pull-descriptions.py

clean		:
	rm -f *.pdf *.aux *.log *.synctex.gz *.fls *.toc *.out

blacken		:
	blacken .

.FORCE		:
