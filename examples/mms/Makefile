README.md: README.ipynb
	jupyter nbconvert \
		README.ipynb \
		--ClearOutputPreprocessor.enabled=True \
		--to markdown \
		--output README.md

upload:
	gsutil cp -r models/* gs://seldon-models/mlserver

