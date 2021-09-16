# Function: Batch make for all gitbooks
# Author: Crifan Li
# Update: 20210916
# Latest: https://github.com/crifan/gitbook_template/blob/master/common/batchProcess/Makefile
# 
# [Note]
# 1. this makefile should be located common batchProcess folder:
# 	/Users/crifan/dev/dev_root/gitbook/GitbookTemplate/gitbook_template/common/batchProcess
# 	should goto above folder to run:
# 	make xxx

BATCH_PROCESS_IGNORE_FILE=batch_process_ignore_books.txt
$(info BATCH_PROCESS_IGNORE_FILE=$(BATCH_PROCESS_IGNORE_FILE))
$(info ----------------------------------------)

BATCH_PROCESS_IGNORE_BOOKS := $(shell cat $(BATCH_PROCESS_IGNORE_FILE))
$(info BATCH_PROCESS_IGNORE_BOOKS=$(BATCH_PROCESS_IGNORE_BOOKS))
$(info ----------------------------------------)

SUB_BOOKS=$(shell ls ../../books)
$(info SUB_BOOKS=$(SUB_BOOKS))
$(info ----------------------------------------)

BOOKS_SRC_ROOT=$(shell cd ../../books && pwd)
$(info BOOKS_SRC_ROOT=$(BOOKS_SRC_ROOT))
$(info ----------------------------------------)

# # REAL_ALL_BOOKS = $(foreach singleBook,$(SUB_BOOKS),$(if [-d $(BOOKS_SRC_ROOT)/$(singleBook)],$(singleBook),))
# # REAL_ALL_BOOKS = $(foreach singleBook,$(SUB_BOOKS),$(if [-f $(BOOKS_SRC_ROOT)/$(singleBook)],,$(singleBook)))
# REAL_ALL_BOOKS = $(foreach singleBook,$(SUB_BOOKS),$(if [test -d $(BOOKS_SRC_ROOT)/$(singleBook)],$(singleBook),))
# $(info REAL_ALL_BOOKS=$(REAL_ALL_BOOKS))
# $(info ----------------------------------------)

TO_PROCESS_BOOKS := $(filter-out $(BATCH_PROCESS_IGNORE_BOOKS), $(SUB_BOOKS))
$(info TO_PROCESS_BOOKS=$(TO_PROCESS_BOOKS))
$(info ----------------------------------------)

# help:
# 	@# echo help;
# 	@for each_item in $(TO_PROCESS_BOOKS); \
# 	do \
# 		if [ -d $(BOOKS_SRC_ROOT)/$$each_item ]; then \
# 			echo $$each_item; \
# 		fi; \
# 	done;


# echo `pwd`; \
# echo $$each_item; \

# Batch make for all gitbooks
help debug_nothing debug_dir init sync_content pull status clean_all website pdf epub mobi all upload commit deploy:
	@echo "Current path="`pwd`;
	@echo "LS_OUTPUT="$(TO_PROCESS_BOOKS);
	@echo "BOOKS_SRC_ROOT="$(BOOKS_SRC_ROOT);
	@for each_item in $(TO_PROCESS_BOOKS); \
	do \
		if [ -f $(BOOKS_SRC_ROOT)/$$each_item/README.md ]; then \
			cd $(BOOKS_SRC_ROOT)/$$each_item; \
			if [ -f Makefile ]; then \
				make $@ || exit "$$?"; \
			fi; \
			cd ..; \
		else \
			echo Omit not-existed book src or non-folder: $$each_item; \
		fi; \
	done;