AM_LDFLAGS= -L$(top_srcdir)/lib -lrdkafka -lz -lpthread -lrt

bin_PROGRAMS=submit
submit_SOURCES=submit.c 
submit_LDADD=../common/libcommon.a $(top_srcdir)/lib/librdkafka.so.1
submit_CFLAGS= -I$(top_srcdir)/include/librdkafka
