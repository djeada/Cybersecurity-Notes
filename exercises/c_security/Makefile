CC ?= cc
PYTHON ?= python3
CFLAGS ?= -std=c11 -O0 -g -Wall -Wextra -Wpedantic
# Keep deliberate invalid accesses visible even when their results are unused.
ASANFLAGS ?= -std=c11 -O0 -g -Wall -Wextra -Wpedantic -fsanitize=address,undefined -fno-omit-frame-pointer

EXERCISES := $(patsubst %/,%,$(wildcard [0-9][0-9]_*/))
PLAIN := $(foreach e,$(EXERCISES),build/$(e)/vulnerable build/$(e)/fixed)
SANITIZED := $(foreach e,$(EXERCISES),build-asan/$(e)/vulnerable build-asan/$(e)/fixed)

.PHONY: all asan test test-asan clean

all: $(PLAIN)
asan: $(SANITIZED)

build/%/vulnerable: %/vulnerable.c
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(CFLAGS) $< -o $@ $(LDFLAGS)

build/%/fixed: %/fixed.c
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(CFLAGS) $< -o $@ $(LDFLAGS)

build-asan/%/vulnerable: %/vulnerable.c
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(ASANFLAGS) $< -o $@ $(LDFLAGS)

build-asan/%/fixed: %/fixed.c
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(ASANFLAGS) $< -o $@ $(LDFLAGS)

test: all
	$(PYTHON) -m unittest discover -s tests -v

test-asan: asan
	C_SECURITY_BUILD=build-asan C_SECURITY_SANITIZED=1 $(PYTHON) -m unittest discover -s tests -v

clean:
	rm -rf build build-asan
