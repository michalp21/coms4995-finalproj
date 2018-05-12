CC = gcc

LIB_NAME = player
SOURCES = player.c
EXTERNAL_SOURCES_NAMES = rng.c net.c game.c
EXTERNAL_SOURCES_DIR = ../../acpc_infrastructure/
EXTERNAL_SOURCES = $(addprefix $(EXTERNAL_SOURCES_DIR), $(EXTERNAL_SOURCES_NAMES))

OBJECTS = $(SOURCES:.c=.o)
EXTERNAL_OBJECTS = $(EXTERNAL_SOURCES_NAMES:.c=.o)

$(LIB_NAME).so: objects
	$(CC) -shared -o lib$(LIB_NAME).so $(OBJECTS) $(EXTERNAL_OBJECTS)

objects: $(SOURCES)
	$(CC) -c -Wall -Werror -fpic $(SOURCES) $(EXTERNAL_SOURCES)

clean:
	rm $(OBJECTS)
	rm $(EXTERNAL_OBJECTS)
	rm lib$(LIB_NAME).so
