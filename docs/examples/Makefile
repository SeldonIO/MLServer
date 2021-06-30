.SUFFIXES: .ipynb .md

EXAMPLES := $(wildcard */*.ipynb)
EXAMPLES_MD=$(patsubst %.ipynb, %.md, $(EXAMPLES))

all: $(EXAMPLES_MD)

.ipynb.md:
	jupyter nbconvert \
		$< \
		--ClearOutputPreprocessor.enabled=True \
		--to markdown \
		--output $(notdir $@)


.PHONY: all
