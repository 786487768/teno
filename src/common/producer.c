/*
 * producer - x system common tools
 *
 * Connect with kafka and produce command messages to kafka
 */

 #include "src/common/producer.h"

 static int run = 1;
 static rd_kafka_t *rk;
 static int exit_eof = 0;
 static int quiet = 0;
 static enum{
     OUTPUT_HEXDUMP,
     OUTPUT_RAW,
 } output = OUTPUT_HEXDUMP;

 static void 
 stop(int sig){
     run = 0;
     fclose(stdin);
 }

 static void 
 hexdump(FILE *fp, const char *name, const void *ptr, size_t len){
     
 }

/**
 * Kafka logger callback (optional)
 */
 static void 
 logger(const rd_kafka_t *rt, int level, 
                 const char *fac, const char *buf){
     struct timeval tv;
     gettimeofday(&tv, NULL);
     fprintf(stderr, "%u.%03u RDKAFKA-%i-%s: %s: %s\n", 
         (int)tv.tv_sec, (int)(tv.tv_usec / 1000),
         level, fac, rk? rd_kafka_name(rk) : NULL, buf);
 }

 /**
 * Message delivery report callback.
 * Called once for each message.
 * See rdkafka.h for more information.
 */
static void 
msg_delivered (rd_kafka_t *rk,
               void *payload, size_t len,
               int error_code,
               void *opaque, void *msg_opaque) {

    if (error_code)
        fprintf(stderr, "%% Message delivery failed: %s\n",
            rd_kafka_err2str(error_code));
    else if (!quiet)
        fprintf(stderr, "%% Message delivered (%zd bytes): %.*s\n", len,
            (int)len, (const char *)payload);
}

/**
 * Message delivery report callback using the richer rd_kafka_message_t object.
 */
static void 
msg_delivered2 (rd_kafka_t *rk,
                            const rd_kafka_message_t *rkmessage, void *opaque) {
    printf("del: %s: offset %"PRId64"\n",
           rd_kafka_err2str(rkmessage->err), rkmessage->offset);
        if (rkmessage->err)
        fprintf(stderr, "%% Message delivery failed: %s\n",
                        rd_kafka_message_errstr(rkmessage));
    else if (!quiet)
        fprintf(stderr,
                        "%% Message delivered (%zd bytes, offset %"PRId64", "
                        "partition %"PRId32"): %.*s\n",
                        rkmessage->len, rkmessage->offset,
            rkmessage->partition,
            (int)rkmessage->len, (const char *)rkmessage->payload);
}

static void 
sig_usr1(int sig){
    rd_kafka_dump(stdout, rk);
}

extern void 
produce_message(char *buf, MYSQL *mysql){
    rd_kafka_topic_t *rkt;
    rd_kafka_conf_t *conf;
    rd_kafka_topic_conf_t *topic_conf;
    /* Kafka configure, will be a struct in later */
    char *brokers = "localhost:9092";
    char *topic = "test";
    int partition = 0;

    int task_id = -1;
    cJSON *message;
    if(buf){
        message = cJSON_Parse(buf);
        task_id = cJSON_GetObjectItem(message, "task_id")->valueint;
    }
        
    char errstr[512];
    // int64_t start_offset = 0;
    // int report_offsets = 0;
    // int do_conf_dump = 0;
    char tmp[16];
    // int64_t seek_offset = 0;
    // int64_t tmp_offset = 0;
    // int get_wmarks = 0;

    /* Kafka configuration */
    conf = rd_kafka_conf_new();
    /* Set looger */
    rd_kafka_conf_set_log_cb(conf, logger);
    /* Quick termination */
    snprintf(tmp, sizeof(tmp), "%i", SIGIO);
    rd_kafka_conf_set(conf, "internal.termination.signal", tmp, NULL, 0);

    /* Topic configuration */
    topic_conf = rd_kafka_topic_conf_new();

    signal(SIGINT, stop);
    signal(SIGUSR1, sig_usr1);

    int sendcnt = 0;

    /* Set up a message delivery report callback */
    rd_kafka_conf_set_dr_cb(conf, msg_delivered);

    /* Create Kafka handle */
    if(!(rk = rd_kafka_new(RD_KAFKA_PRODUCER, conf,
                errstr, sizeof(errstr)))){
        fprintf(stderr, 
            "%% Failed to create new producer: %s\n", 
            errstr);
        update_state(mysql, task_id, TASK_FAIL);
        exit(1);
    }

    rd_kafka_set_log_level(rk, LOG_DEBUG);
    /* ADD brokers */
    if(rd_kafka_brokers_add(rk, brokers) == 0){
        fprintf(stderr, "%% No valid brokers specified\n");
        update_state(mysql, task_id, TASK_FAIL);
        exit(1);
    }

    /* Create topic */
    rkt = rd_kafka_topic_new(rk, topic, topic_conf);

    if(run){
        size_t len = strlen(buf);
        if(buf[len-1] == '\n')
            buf[--len] = '\0';

        /* Send/Producer message */
        if(rd_kafka_produce(rkt, partition,
                RD_KAFKA_MSG_F_COPY,
                buf, len,
                NULL, 0,
                NULL) == -1){
            fprintf(stderr,
                    "%% Failed to produce to topic %s "
                    "partition %i: %s\n",
                    rd_kafka_topic_name(rkt), partition,
                    rd_kafka_err2str(rd_kafka_last_error()));
            update_state(mysql, task_id, TASK_FAIL);
                /* Poll to handle delivery reports */
            rd_kafka_poll(rk, 0);
        }
        if (!quiet)
            fprintf(stderr, "%% Sent %zd bytes to topic "
                "%s partition %i\n",
            len, rd_kafka_topic_name(rkt), partition);
        sendcnt++;
        /* Poll to handle delivery reports */
        rd_kafka_poll(rk, 0);
    }

    /* Poll to handle delivery reports */
    rd_kafka_poll(rk, 0);

    /* Wait for messages to be delivered */
    while (run && rd_kafka_outq_len(rk) > 0)
        rd_kafka_poll(rk, 100);

    update_state(mysql, task_id, TASK_WAITING);

    /* Destroy topic */
    rd_kafka_topic_destroy(rkt);

    /* Destroy the handle */
    rd_kafka_destroy(rk);

    /* Let background threads clean up and terminate cleanly. */
    run = 5;
    while (run-- > 0 && rd_kafka_wait_destroyed(1000) == -1)
        printf("Waiting for librdkafka to decommission\n");
    if (run <= 0)
        rd_kafka_dump(stdout, rk);

    cJSON_Delete(message);
}

