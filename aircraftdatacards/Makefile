.SUFFIXES: .json .pdf

.json.pdf:
	python3 aircraftdatacards.py $*.json

all						:	\
	sandbox.pdf				\
	australian.pdf			\
	british.pdf				\
	canadian.pdf			\
	chinese.pdf				\
	european.pdf			\
	french.pdf				\
	italian.pdf				\
	bombers.pdf 			\
	bomber-fighters.pdf		\
	all.pdf

# We force these since in most cases the aircraft data files will have changed.
sandbox.pdf				:	.FORCE
all.pdf					:	.FORCE
australian.pdf			:	.FORCE
british.pdf				:	.FORCE
canadian.pdf			:	.FORCE
chinese.pdf				:	.FORCE
european.pdf			:	.FORCE
french.pdf				:	.FORCE
italian.pdf				:	.FORCE
bombers.pdf				:	.FORCE
bomber-fighters.pdf		:	.FORCE

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
