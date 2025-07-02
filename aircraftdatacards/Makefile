.SUFFIXES: .json .pdf

.json.pdf:
	python3 aircraftdatacards.py $*.json

all			:	all.pdf

all.pdf		:	.FORCE

sandbox.pdf	:	.FORCE

format		:
	python3 format.py

example-adcs:
	version=1 make example-adc.pdf && mv example-adc.pdf example-adc-v1.pdf
	version=2 make example-adc.pdf && mv example-adc.pdf example-adc-v2.pdf
	version=3 make example-adc.pdf && mv example-adc.pdf example-adc-v3.pdf

push-descriptions:
	python3 push-descriptions.py

pull-descriptions:
	python3 pull-descriptions.py

clean		:
	rm -f *.pdf *.aux *.log *.synctex.gz *.fls *.toc *.out

blacken		:
	blacken .

.FORCE		:
