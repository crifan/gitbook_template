-include ../../common/config/deploy/deploy_server_info.mk

# Latest: https://github.com/crifan/gitbook_template/blob/master/common/gitbook_makefile.mk

################################################################################
# System Value
################################################################################

CURRENT_USER  := $(shell whoami)
$(info CURRENT_USER=$(CURRENT_USER))

################################################################################
# Global Config
################################################################################

ENABLE_DEPLOY_SERVER = false
ENABLE_COMMIT_GITHUB_IO = false
ENABLE_UPDATE_GITHUB_IO_README = false
ENABLE_RSYNC_PROXY = false

# ENABLE_DEPLOY_SERVER = true
# ENABLE_COMMIT_GITHUB_IO = true
# ENABLE_UPDATE_GITHUB_IO_README = true
# ENABLE_RSYNC_PROXY = true

# default: rsync not use any proxy
RSYNC_PROXY = 
RSYNC_PARAMS = 

################################################################################
# Generated Config
################################################################################

ifeq ($(CURRENT_USER), crifan)
ENABLE_COMMIT_GITHUB_IO = true

# if need commit, enable and change to yours path
GITHUB_IO_PATH=/Users/crifan/dev/dev_root/github/github.io/crifan.github.io

ENABLE_UPDATE_GITHUB_IO_README = true

ENABLE_RSYNC_PROXY = true
else ifeq ($(CURRENT_USER), limao)
ENABLE_COMMIT_GITHUB_IO = true

ENABLE_UPDATE_GITHUB_IO_README = true

# if need commit, enable and change to yours path
GITHUB_IO_PATH=/Users/limao/dev/crifan/crifan.github.io

ENABLE_RSYNC_PROXY = true
endif

ifeq ($(ENABLE_RSYNC_PROXY), true)
# for rsync use sock5 proxy
PROXY_SOCK5 = 127.0.0.1:51837
RSYNC_PROXY = -e "ssh -o 'ProxyCommand nc -X 5 -x $(PROXY_SOCK5) %h %p' -o ServerAliveInterval=30 -o ServerAliveCountMax=5"
endif

ifneq ($(RSYNC_PROXY), )
RSYNC_PARAMS = $(RSYNC_PROXY) -avzh --progress --stats --delete --force
endif

# Gitbook Debug Port and LiveReload Port
GITBOOK_DEBUG_PORT ?= 4000
GITBOOK_DEBUG_LRPORT ?= 35729

### Upload to server ###

ifeq ($(ENABLE_DEPLOY_SERVER), true)
# if need upload/deploy, update content of these file
DEPLOY_SERVER_PASSWORD_FILE=$(GITBOOK_ROOT_COMMON)/config/deploy/deploy_server_password.txt
DEPLOY_IGNORE_FILE=$(GITBOOK_ROOT_COMMON)/config/deploy/deploy_ignore_book_list.txt
endif

COMMON_GITIGNORE_FILE=$(GITBOOK_ROOT_COMMON)/config/common/common_gitignore

ifeq ($(ENABLE_DEPLOY_SERVER), true)

# ifneq ("$(wildcard $(DEPLOY_IGNORE_FILE))", "")
ifneq ($(wildcard $(DEPLOY_IGNORE_FILE)), )
$(info $(DEPLOY_IGNORE_FILE) is exist, not empty)
IGNORE_FILE_CONTENT := $(shell cat $(DEPLOY_IGNORE_FILE))
# IGNORE_FILE_CONTENT := $(file < $(DEPLOY_IGNORE_FILE))

FOUND_BOOK := $(findstring $(BOOK_NAME), $(IGNORE_FILE_CONTENT))
$(info FOUND_BOOK=$(FOUND_BOOK))
endif

ifeq ($(FOUND_BOOK), )
$(info NOT found $(BOOK_NAME) in IGNORE_FILE_CONTENT=$(IGNORE_FILE_CONTENT))
SHOULD_IGNORE_DEPLOY_SERVER = false
else
$(info IS found $(BOOK_NAME) in $(IGNORE_FILE_CONTENT))
SHOULD_IGNORE_DEPLOY_SERVER = true
endif

endif

$(info ---Current Config---)
$(info ENABLE_COMMIT_GITHUB_IO=$(ENABLE_COMMIT_GITHUB_IO))
$(info ENABLE_UPDATE_GITHUB_IO_README=$(ENABLE_UPDATE_GITHUB_IO_README))
$(info ENABLE_DEPLOY_SERVER=$(ENABLE_DEPLOY_SERVER))
$(info ENABLE_RSYNC_PROXY=$(ENABLE_RSYNC_PROXY))
$(info RSYNC_PROXY=$(RSYNC_PROXY))
$(info RSYNC_PARAMS=$(RSYNC_PARAMS))

################################################################################
# Global defines
################################################################################

GENERATE_BOOK_JSON_FILE=$(GITBOOK_ROOT_COMMON)/tools/generate_book_json.py
GENERATE_README_MD_FILE=$(GITBOOK_ROOT_COMMON)/tools/generate_readme_md.py
SYNC_README_JSON_TO_BOOK_JSON_FILE=$(GITBOOK_ROOT_COMMON)/tools/sync_ReadmeCurrent_to_bookCurrent.py
UPDATE_GITHUB_IO_README_FILE=$(GITBOOK_ROOT_COMMON)/tools/update_crifan_github_io_readme.py

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

# new line and tab
define NEWLINE


endef

define TAB
	
endef

################################################################################
# Output current makefile info
################################################################################
Author=crifan.org
Version=20210916
Function=Auto use gitbook to generated files: website/pdf/epub/mobi; upload to remote server; commit to your github.io repository
RunHelp = Run 'make help' to see usage
GitRepo = Latest version: https://github.com/crifan/gitbook_template
$(info --------------------------------------------------------------------------------)
$(info ${YELLOW}Author${RESET}  : ${GREEN}$(Author)${RESET})
$(info ${YELLOW}Version${RESET} : ${GREEN}$(Version)${RESET})
$(info ${YELLOW}Function${RESET}: ${GREEN}$(Function)$(NEWLINE)$(TAB)$(TAB)$(RunHelp)$(NEWLINE)$(TAB)$(TAB)$(GitRepo)${RESET})
$(info --------------------------------------------------------------------------------)


define getCurrentDirAndDirName
$(eval MAKEFILE_LIST_LASTWORD = $(lastword $(MAKEFILE_LIST)))
$(eval MAKEFILE_LIST_FIRSTWORD = $(firstword $(MAKEFILE_LIST)))
$(eval MAKEFILE_PATH := $(abspath $(MAKEFILE_LIST_FIRSTWORD)))
$(eval MAKEFILE_DIR := $(dir $(MAKEFILE_PATH)))
$(eval MAKEFILE_DIR_PATSUBST := $(patsubst %/,%,$(MAKEFILE_DIR)))
$(eval MAKEFILE_DIR_NOSLASH = $(MAKEFILE_DIR_PATSUBST))
$(eval CURRENT_DIR_WITH_SLASH = $(MAKEFILE_DIR))
$(eval CURRENT_DIR = $(MAKEFILE_DIR_NOSLASH))
$(eval CURRENT_DIR_NAME := $(notdir $(MAKEFILE_DIR_PATSUBST)))
$(eval GITBOOK_ROOT := $(abspath $(CURRENT_DIR)/../..))
$(eval GITBOOK_ROOT_BOOKS := $(abspath $(GITBOOK_ROOT)/books))
$(eval GITBOOK_ROOT_COMMON := $(abspath $(GITBOOK_ROOT)/common))
$(eval GITBOOK_ROOT_GENERATED := $(abspath $(GITBOOK_ROOT)/generated))

$(info CURRENT_DIR=$(CURRENT_DIR))
endef

$(eval $(call getCurrentDirAndDirName))
# then following can get value for: CURRENT_DIR_NAME, CURRENT_DIR

BOOK_NAME := $(CURRENT_DIR_NAME)
$(info BOOK_NAME=$(BOOK_NAME))

RELEASE_FOLDER_NAME = release
DEBUG_FOLDER_NAME = debug
CURRENT_BOOK_GENERATED=$(GITBOOK_ROOT)/generated/books/$(BOOK_NAME)
RELEASE_PATH = $(CURRENT_BOOK_GENERATED)/$(RELEASE_FOLDER_NAME)/$(BOOK_NAME)
DEBUG_PATH = $(CURRENT_BOOK_GENERATED)/$(DEBUG_FOLDER_NAME)

WEBSITE_PATH = $(RELEASE_PATH)/website
PDF_PATH = $(RELEASE_PATH)/pdf
EPUB_PATH = $(RELEASE_PATH)/epub
MOBI_PATH = $(RELEASE_PATH)/mobi

PDF_NAME = $(BOOK_NAME).pdf
EPUB_NAME = $(BOOK_NAME).epub
MOBI_NAME = $(BOOK_NAME).mobi

# ZIP_NAME = $(BOOK_NAME).zip

WEBSITE_FULLNAME = $(WEBSITE_PATH)
PDF_FULLNAME = $(PDF_PATH)/$(PDF_NAME)
EPUB_FULLNAME = $(EPUB_PATH)/$(EPUB_NAME)
MOBI_FULLNAME = $(MOBI_PATH)/$(MOBI_NAME)

.DEFAULT_GOAL := deploy

.PHONY : debug_makefile debug_nothing
.PHONY : debug_dir debug_python debug debug_inlcude
.PHONY : help
.PHONY : create_folder_all create_folder_website create_folder_pdf create_folder_epub create_folder_mobi
.PHONY : clean_all clean_website clean_pdf clean_epub clean_mobi
.PHONY : all website pdf epub mobi
.PHONY : upload commit deploy

## Debug include file
debug_include:
	@echo DEPLOY_SERVER_USER=$(DEPLOY_SERVER_USER)
	@echo DEPLOY_SERVER_IP=$(DEPLOY_SERVER_IP)
	@echo DEPLOY_SERVER_PATH=$(DEPLOY_SERVER_PATH)
	@echo DEPLOY_SERVER_PASSWORD_FILE=$(DEPLOY_SERVER_PASSWORD_FILE)

## Print current directory related info
debug_dir:
	@echo MAKEFILE_LIST=$(MAKEFILE_LIST)
	@echo MAKEFILE_LIST=$(value MAKEFILE_LIST)
	@echo MAKEFILE_LIST_LASTWORD=$(MAKEFILE_LIST_LASTWORD)
	@echo MAKEFILE_LIST_FIRSTWORD=$(MAKEFILE_LIST_FIRSTWORD)
	@echo MAKEFILE_PATH=$(MAKEFILE_PATH)
	@echo MAKEFILE_DIR=$(MAKEFILE_DIR)
	@echo MAKEFILE_DIR_PATSUBST=$(MAKEFILE_DIR_PATSUBST)
	@echo CURRENT_DIR_WITH_SLASH=$(CURRENT_DIR_WITH_SLASH)
	@echo CURRENT_DIR=$(CURRENT_DIR)
	@echo CURRENT_DIR_NAME=$(CURRENT_DIR_NAME)
	@echo BOOK_NAME=$(BOOK_NAME)
	@echo GITBOOK_ROOT=$(GITBOOK_ROOT)
	@echo GITBOOK_ROOT_BOOKS=$(GITBOOK_ROOT_BOOKS)
	@echo GITBOOK_ROOT_COMMON=$(GITBOOK_ROOT_COMMON)
	@echo GITBOOK_ROOT_GENERATED=$(GITBOOK_ROOT_GENERATED)
	@echo RELEASE_PATH=$(RELEASE_PATH)
	@echo WEBSITE_PATH=$(WEBSITE_PATH)
	@echo WEBSITE_FULLNAME=$(WEBSITE_FULLNAME)
	@echo PDF_PATH=$(PDF_PATH)
	@echo PDF_FULLNAME=$(PDF_FULLNAME)

## Debug for makefile call python
debug_python:
	@python $(GENERATE_BOOK_JSON_FILE)

################################################################################
# Create folder
################################################################################

## Create folder for gitbook local debug
create_folder_debug: 
	mkdir -p $(DEBUG_PATH)

## Create folder for gitbook release: website+pdf+epub+mobi
create_folder_release: 
	mkdir -p $(RELEASE_PATH)

## Create folder for gitbook website
create_folder_website: 
	mkdir -p $(WEBSITE_PATH)

## Create folder for pdf
create_folder_pdf: 
	mkdir -p $(PDF_PATH)

## Create folder for epub
create_folder_epub: 
	mkdir -p $(EPUB_PATH)

## Create folder for mobi
create_folder_mobi: 
	mkdir -p $(MOBI_PATH)

## Create folder for all: debug+release(website/pdf/epub/mobi)
create_folder_all: create_folder_debug create_folder_release create_folder_website create_folder_pdf create_folder_epub create_folder_mobi

################################################################################
# Clean
################################################################################

## Clean generated book.json file
clean_generated_book_json:
	-rm -f book.json

## Clean generated README.md file
clean_generated_readme_md:
	-rm -f README.md

## Clean copied .gitignore
clean_gitignore:
	-rm -f .gitignore

## Clean generated all files
clean_generated_all: clean_gitignore clean_generated_readme_md clean_generated_book_json
	@echo Completed clean all generated

# ------------------------------------------------

## Clean gitbook debug
clean_debug:
	-rm -rf $(DEBUG_PATH)

## Clean generated gitbook website whole folder
clean_website:
	-rm -rf $(WEBSITE_PATH)

## Clean generated PDF file and whole folder
clean_pdf:
	-rm -rf $(PDF_PATH)

## Clean generated ePub file and whole folder
clean_epub:
	-rm -rf $(EPUB_PATH)

## Clean generated Mobi file and whole folder
clean_mobi:
	-rm -rf $(MOBI_PATH)

## Clean gitbook release
clean_release: clean_website clean_pdf clean_epub clean_mobi
	-rm -rf $(RELEASE_PATH)

## Clean all generated files
clean_all: clean_generated_all clean_debug clean_release

################################################################################
# Gitbook Init / Preparation
################################################################################

## Generate README.md from ../README_template.md and README_current.json
generate_readme_md: clean_generated_readme_md
	@python $(GENERATE_README_MD_FILE)

## copy README.md to ./src
copy_readme: generate_readme_md
	cp README.md ./src/README.md

## copy common .gitignore
copy_gitignore:
	cp $(COMMON_GITIGNORE_FILE) .gitignore

## Sync README_current.json to book_current.json
sync_readme_to_book:
	@python $(SYNC_README_JSON_TO_BOOK_JSON_FILE)

## Generate book.json from ../book_common.json and book_current.json
generate_book_json: clean_generated_book_json
	@python $(GENERATE_BOOK_JSON_FILE)

## sync content
sync_content: sync_readme_to_book generate_book_json generate_readme_md copy_readme copy_gitignore
	@echo Complete sync content

## gitbook install plugins
install:
	gitbook install

## gitbook init to install plugins
init: sync_content install
	@echo Compelete init all things

################################################################################
# Git Operation
################################################################################

## git pull to update to latest code
pull:
	git pull

## git status
status:
	git status

################################################################################
# Generate Files
################################################################################

GITBOOK_BUILD_FLAGS= --timing
GITBOOK_COMMON_FLAGS= --log debug

## Debug gitbook
debug: sync_content clean_debug create_folder_debug
	gitbook --port $(GITBOOK_DEBUG_PORT) --lrport $(GITBOOK_DEBUG_LRPORT) serve $(CURRENT_DIR) $(DEBUG_PATH) $(GITBOOK_COMMON_FLAGS)

## Generate gitbook website
website: sync_content clean_website create_folder_website
	@echo ================================================================================
	@echo Generate website for $(BOOK_NAME)
	gitbook build $(CURRENT_DIR) $(WEBSITE_FULLNAME) $(GITBOOK_COMMON_FLAGS) $(GITBOOK_BUILD_FLAGS)

## Generate PDF file
pdf: sync_content clean_pdf create_folder_pdf
	@echo ================================================================================
	@echo Generate PDF for $(BOOK_NAME)
	gitbook pdf $(CURRENT_DIR) $(PDF_FULLNAME) $(GITBOOK_COMMON_FLAGS)

## Generate ePub file
epub: sync_content clean_epub create_folder_epub
	@echo ================================================================================
	@echo Generate ePub for $(BOOK_NAME)
	gitbook epub $(CURRENT_DIR) $(EPUB_FULLNAME) $(GITBOOK_COMMON_FLAGS)

## Generate Mobi file
mobi: sync_content clean_mobi create_folder_mobi
	@echo ================================================================================
	@echo Generate Mobi for $(BOOK_NAME)
	gitbook mobi $(CURRENT_DIR) $(MOBI_FULLNAME) $(GITBOOK_COMMON_FLAGS)

## Generate all files: website/pdf/epub/mobi
all: website pdf epub mobi
	@echo ================================================================================
	@echo Generate All for $(BOOK_NAME)

# ################################################################################
# # Compress
# ################################################################################

# ## Compress all generated files to single zip file
# zip:
# 	zip -r $(ZIP_NAME) $(RELEASE_PATH)

# ## Clean compressed file
# clean_zip:
# 	-rm -rf $(ZIP_NAME)

################################################################################
# Upload to server
################################################################################

## Upload all genereted website/pdf/epub/mobi files to remote server using rsync. Create deploy_server_info.mk and deploy_server_password.txt which contain deploy server IP+User+Path and Password before use this
upload: all
	@echo ================================================================================
ifeq ($(ENABLE_DEPLOY_SERVER), true)
	@echo Upload for $(BOOK_NAME)
	sshpass -f $(DEPLOY_SERVER_PASSWORD_FILE) rsync $(RSYNC_PARAMS) $(RELEASE_PATH) $(DEPLOY_SERVER_USER)@$(DEPLOY_SERVER_IP):$(DEPLOY_SERVER_PATH)
else
	@echo Disabled deploy $(BOOK_NAME) to server $(DEPLOY_SERVER_IP)
endif


################################################################################
# Commit to github
################################################################################
COMMIT_COMMENT ?= "1. update book $(BOOK_NAME)"

## Commit generated files to github io
commit: all
	@echo ================================================================================
ifeq ($(ENABLE_COMMIT_GITHUB_IO), true)
	@echo Commit for $(BOOK_NAME)
	@echo pull github.io
	cd $(GITHUB_IO_PATH) && \
	pwd && \
	ls -la && \
	pwd && \
	git pull
	pwd
	@echo update readme.md of local github.io
	if [ $(ENABLE_UPDATE_GITHUB_IO_README) == true ]; then \
		python $(UPDATE_GITHUB_IO_README_FILE) --curBookRepoName $(BOOK_NAME) --localGithubIoPath $(GITHUB_IO_PATH); \
	else \
		echo "Ignored update README.md before commit $(BOOK_NAME) to github.io"; \
	fi;
	@echo copy current book all generated files to local github.io
	rsync $(RSYNC_PARAMS) $(RELEASE_PATH) $(GITHUB_IO_PATH)
	@echo push modifed content to github.io
	cd $(GITHUB_IO_PATH) && \
	pwd && \
	git status && \
	pwd && \
	git add README.md && \
	git add $(BOOK_NAME)/* && \
	pwd && \
	git status && \
	pwd && \
	git commit -m $(COMMIT_COMMENT) && \
	pwd && \
	git status && \
	pwd && \
	git push && \
	pwd && \
	cd $(CURRENT_DIR) && \
	pwd && \
	git remote -v
else
	@echo Ignored commit $(BOOK_NAME) to github.io
endif

################################################################################
# Deploy generated files to remote server and github.io repo
################################################################################

## Deploy = upload and commit for generated files
deploy: upload commit
	@echo ================================================================================
	@echo Deploy for $(BOOK_NAME)

################################################################################
# Help
################################################################################

TARGET_MAX_CHAR_NUM=25
## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Defaul Target: ${GREEN}${.DEFAULT_GOAL}${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)