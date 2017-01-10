AUTOMAKE_OPTIONS=foreign 

noinst_LIBRARIES=libcommon.a 

libcommon_a_SOURCES=producer.c producer.h  		\
		job.h job.c 				\
		log.h log.c  				\
		cJSON.h cJSON.c 			\
		tpython.h tpython.c

libcommon_a_CFLAGS=-I../../include/librdkafka -I/usr/include/python3.4