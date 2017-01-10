AM_LDFLAGS= -L$(top_srcdir)/lib -lrdkafka -lz -lpthread -lrt

bin_PROGRAMS=tenoc
tenoc_SOURCES=tenoc.c 
tenoc_LDADD=../common/libcommon.a $(top_srcdir)/lib/librdkafka.so.1 -lm \
			/usr/lib/python3.4/config-3.4m-x86_64-linux-gnu/libpython3.4.so 

tenoc_CFLAGS= -I$(top_srcdir)/include/librdkafka -I/usr/include/python3.4