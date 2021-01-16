# Author: Crifan Li
# Function: Batch make for all gitbooks
# Version: 20190716
# 
# [Note]
# 1. this makefile should be located in
# /Users/crifan/dev/dev_root/gitbook/gitbook_src_root/common

SUB_BOOKS=$(shell ls ../books)
BOOKS_SRC_ROOT=$(shell cd ../books && pwd)

# Batch make for all gitbooks
help debug_dir init sync_content clean_all website pdf epub mobi all upload commit deploy:
	@echo "Current path="`pwd`;
	@echo "LS_OUTPUT="$(SUB_BOOKS);
	@echo "BOOKS_SRC_ROOT="$(BOOKS_SRC_ROOT);
	@for each_item in $(SUB_BOOKS); \
	do \
		if [ -d $(BOOKS_SRC_ROOT)/$$each_item ]; then \
			cd $(BOOKS_SRC_ROOT)/$$each_item; \
			echo `pwd`; \
			if [ -f Makefile ]; then \
				make $@ || exit "$$?"; \
			fi; \
			cd ..; \
		fi; \
	done;