README.md: README.ipynb
	jupyter nbconvert \
		README.ipynb \
		--ClearOutputPreprocessor.enabled=True \
		--to markdown \
		--output README.md

upload:
	gsutil cp -r models/* gs://seldon-models/mlserver/mms
	gsutil cp -r models/mnist-svm gs://seldon-models/mlserver/mms-sklearn
	gsutil cp -r models/mushroom-xgboost gs://seldon-models/mlserver/mms-xgboost

