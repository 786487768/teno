AUTOMAKE_OPTIONS=foreign 

noinst_LIBRARIES=libcommon.a 

libcommon_a_SOURCES=producer.c producer.h  		\
		task.h task.c 				\
		log.h log.c  				\
		cJSON.h cJSON.c 			\
		tpython.h tpython.c         \
		teno_db.h teno_db.c         \
		tools.h tools.c

libcommon_a_CFLAGS= -I../../include/librdkafka -I/usr/include/python3.4 -I/usr/include/mysql