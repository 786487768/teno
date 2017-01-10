/*
 * producer - x system common tools
 *
 * Connect with kafka and produce command messages to kafka
 */

 #include "src/tenoc/tenoc.h"

 static int run = 1;
 static rd_kafka_t *rk;
 static int exit_eof = 0;
 static int quiet = 0;
 static enum{
    OUTPUT_HEXDUMP,
    OUTPUT_RAW,
 } output = OUTPUT_RAW;

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

static void msg_consume (rd_kafka_message_t *rkmessage,
             void *opaque) {
    cJSON *message;
    char *exec;
    char *argv;
    uint32_t uid;
    char result[256];
    char errinfo[256];
    PyObject *call_slurm;
    if (rkmessage->err) {
        if (rkmessage->err == RD_KAFKA_RESP_ERR__PARTITION_EOF) {
            fprintf(stderr,
                "%% Consumer reached end of %s [%"PRId32"] "
                   "message queue at offset %"PRId64"\n",
                   rd_kafka_topic_name(rkmessage->rkt),
                   rkmessage->partition, rkmessage->offset);

            if (exit_eof)
                run = 0;

            return;
        }

        fprintf(stderr, "%% Consume error for topic \"%s\" [%"PRId32"] "
               "offset %"PRId64": %s\n",
               rd_kafka_topic_name(rkmessage->rkt),
               rkmessage->partition,
               rkmessage->offset,
               rd_kafka_message_errstr(rkmessage));

                if (rkmessage->err == RD_KAFKA_RESP_ERR__UNKNOWN_PARTITION ||
                    rkmessage->err == RD_KAFKA_RESP_ERR__UNKNOWN_TOPIC)
                        run = 0;
        return;
    }

    if (!quiet) {
        rd_kafka_timestamp_type_t tstype;
        int64_t timestamp;
        fprintf(stdout, "%% Message (offset %"PRId64", %zd bytes):\n",
            rkmessage->offset, rkmessage->len);

        timestamp = rd_kafka_message_timestamp(rkmessage, &tstype);
        if (tstype != RD_KAFKA_TIMESTAMP_NOT_AVAILABLE) {
            const char *tsname = "?";
            if (tstype == RD_KAFKA_TIMESTAMP_CREATE_TIME)
                tsname = "create time";
            else if (tstype == RD_KAFKA_TIMESTAMP_LOG_APPEND_TIME)
                tsname = "log append time";

            fprintf(stdout, "%% Message timestamp: %s %"PRId64
                " (%ds ago)\n",
                tsname, timestamp,
                !timestamp ? 0 :
                (int)time(NULL) - (int)(timestamp/1000));
        }
    }

/*    if (rkmessage->key_len) {
        if (output == OUTPUT_HEXDUMP)
            hexdump(stdout, "Message Key",
                rkmessage->key, rkmessage->key_len);
        else
            printf("Key: %.*s\n",
                   (int)rkmessage->key_len, (char *)rkmessage->key);
    }
    if (output == OUTPUT_HEXDUMP)
        hexdump(stdout, "Message Payload",
            rkmessage->payload, rkmessage->len);
    else
        printf("%.*s\n",
               (int)rkmessage->len, (char *)rkmessage->payload);
*/
    message = cJSON_Parse((char *)rkmessage->payload);
    exec = cJSON_GetObjectItem(message, "exec")->valuestring;
    argv = cJSON_Print(cJSON_GetObjectItem(message, "argv"));
    uid = cJSON_GetObjectItem(message, "uid")->valueint;
    printf("exec = %s, argv = %s, uid = %u\n", exec, argv, uid);

    printf("begin stdout is %ld\n", ftell(stdout));
    if(setuid(uid) < 0)
        fprintf(stderr, "set uid failed\n");

    Py_Initialize();
    PyRun_SimpleString("import sys; sys.path.append('..')");
    call_slurm = import_name("slurm.slurm", "run");
    printf("%s\n", get_task_result(call_slurm, exec, argv));
    Py_DECREF(call_slurm);
    Py_Finalize();

}

static void 
sig_usr1(int sig){
    rd_kafka_dump(stdout, rk);
}

int main()
{
    rd_kafka_conf_t *conf;
    rd_kafka_topic_conf_t *topic_conf;
    rd_kafka_topic_partition_list_t *topics;
    rd_kafka_resp_err_t err;
    /* Kafka configure, will be a struct in later */
    char *brokers = "localhost:9092";
    char *topic = "test";
    char *group = "teno";
    int partition = 0;

    char errstr[512];
    char tmp[16];

    signal(SIGINT, stop);
    signal(SIGUSR1, sig_usr1);

    /* Kafka configuration */
    conf = rd_kafka_conf_new();
    /* Set looger */
    rd_kafka_conf_set_log_cb(conf, logger);
    /* Quick termination */
    snprintf(tmp, sizeof(tmp), "%i", SIGIO);
    rd_kafka_conf_set(conf, "internal.termination.signal", tmp, NULL, 0);

    /* Topic configuration */
    topic_conf = rd_kafka_topic_conf_new();
    /* Set group */
    if(rd_kafka_conf_set(conf, "group.id", group,
                        errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK){
        fprintf(stderr, "%% %s\n", errstr);
        exit(1);
    }
    /* Consumer groups always use broker based offset storage */
    if(rd_kafka_topic_conf_set(topic_conf, "offset.store.method",
                            "broker",
                            errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK){
        fprintf(stderr, "%% %s\n", errstr);
        exit(1);
    }
    /* Set default topic config for pattern-matched topics. */
    rd_kafka_conf_set_default_topic_conf(conf, topic_conf);
    /* Create Kafka handle*/
    if(!(rk = rd_kafka_new(RD_KAFKA_CONSUMER, conf,
            errstr, sizeof(errstr)))){
        fprintf(stderr, 
            "%% Failed to create new consumer %s\n", 
            errstr);
        exit(1);
    }
    /* Set log level*/
    rd_kafka_set_log_level(rk, LOG_LEVEL_DEBUG);

    /* Add brokers*/
    if(rd_kafka_brokers_add(rk, brokers) == 0){
        fprintf(stderr, "%% No valid brokers specified\n");
        exit(1);
    }

    /* Redirect rd_kafka_poll() to consumer_poll() */
    rd_kafka_poll_set_consumer(rk);

    topics = rd_kafka_topic_partition_list_new(1);
    rd_kafka_topic_partition_list_add(topics, topic, partition);
    /* Subscribe to topics*/
    if((err = rd_kafka_subscribe(rk, topics))){
        fprintf(stderr, 
                "%% Failed to start consumer topics : %s\n", 
                rd_kafka_err2str(err));
        exit(1);
    }
    while(run){
        rd_kafka_message_t *rkmessage;

        rkmessage = rd_kafka_consumer_poll(rk, 1000);
        if(!rkmessage)
            continue;
        if(fork() == 0)
            msg_consume(rkmessage, NULL);

        /* Return messages to kafka*/
        rd_kafka_message_destroy(rkmessage);   
        
    }
done:
        err = rd_kafka_consumer_close(rk);
        if (err)
                fprintf(stderr, "%% Failed to close consumer: %s\n",
                        rd_kafka_err2str(err));
        else
                fprintf(stderr, "%% Consumer closed\n");
        /* Destory topic info*/
        rd_kafka_topic_partition_list_destroy(topics);
        /* Destroy handle */
        rd_kafka_destroy(rk);

    /* Let background threads clean up and terminate cleanly. */
    run = 5;
    while (run-- > 0 && rd_kafka_wait_destroyed(1000) == -1)
        printf("Waiting for librdkafka to decommission\n");
    if (run <= 0)
        rd_kafka_dump(stdout, rk);

    return 0;

}

