.SUFFIXES: .json .pdf

.json.pdf:
	python3 aircraftdatacards.py $*.json

all			:	all.pdf

all.pdf		:	.FORCE

format		:
	python3 format.py

push-descriptions:
	python3 push-descriptions.py

pull-descriptions:
	python3 pull-descriptions.py

clean		:
	rm -f *.pdf

blacken		:
	blacken .

.FORCE		:
