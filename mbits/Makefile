image:
	docker build -t organisynth-yt .

all_services:
	docker run -it --rm -v $(pwd)/all_services:/opt organisynth-yt bash -c "yt build"
