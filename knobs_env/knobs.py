"""
    description: all known knobs in dict format
    {'name_param': ['type_format', ['possible_values]]}, where
    type_format - integer/float/string
    possible_values - enum strings/min-max values

    for integer values format like this:
    @key: ["integer", [min, max, default]]

    for float values format like this:
    @key: ["float", [min, max, default]]

    for boolean values format like this:
    @key: ["boolean", [@defaultValue("false", "true")]

    for enum values format like this:
    @key: ["enum", ["some", "enum", "values"], "@defaultValue"]

    created by: minegoodfeeling@gmail.com

    Made with official documentation of settings:
    https://www.postgresql.org/docs/current/runtime-config-wal.html
"""

# TODO make a flag of knob setting only by start, and for tuning them we need to restart server
# TODO make a "turning off" value that not in interval, like @value in [0,10], but can have @value=-1 for turning off parameter
# TODO mark a set "danger" parameters, that could crash a DB without a problem - think how we can pass them - fixed by picking only safe set of params

memory = 1 * 1024 * 1024 * 1024  # 1 GB of RAM
disk = 10 * 1024 * 1024 * 1024  # 10 GB in disk
max_connections = 16
max_files_per_process = 2000


class Knobs:
    def __init__(self):
        self.knobs = {}
        self.init_knobs()

    def init_knobs(self):
        extended_knobs = {
            # === connection knobs ===
            "max_connections": ["integer", [1, 200, 100]],
            "reserved_connections": ["integer", [0, 200, 0]],
            "superuser_reserved_connections": ["integer", [1, 200, 3]],
            "bonjour": ["boolean", "false"],

            # === tcp settings knobs ===
            # if 0 - this take a default value in the OS
            # think about skipping those knobs
            # "tcp_keepalives_idle": ["integer", [0, 2 * 60 * 60, 0]],
            # "tcp_keepalives_interval": ["integer", [0, 5, 0]],
            # "tcp_keepalives_count": ["integer", [1, 3, 0]],
            # "tcp_user_timeout": ["integer", [1, 3000, 0]],
            # "client_connection_check_interval": ["integer", [0, 5000, 0]],

            # === auth knobs ===
            # think - better skip it, because they don't have any a performance gain

            # BLCKSZ is not 8kB, the default and maximum values scale proportionally to it
            # === mem knobs ===
            "shared_buffers": ["integer", [0, memory, 128 * 1024 * 1024]],
            "huge_page_size": ["integer", [0, memory, 2 * 1024 * 1024]],  # TODO
            "temp_buffers": ["integer", [0, memory, 8 * 1024 * 1024]],
            "work_mem": ["integer", [0, memory, 4 * 1024 * 1024]],
            "maintenance_work_mem": ["integer", [0, memory, 64 * 1024 * 1024]],
            "autovacuum_work_mem": ["integer", [0, memory, 64 * 1024 * 1024]],
            "vacuum_buffer_usage_limit": ["integer", [0, memory, 1 / 8 * 128 * 1024 * 1024]],  # 1/8 of shared_buffers
            "logical_decoding_work_mem": ["integer", [0, memory, 64 * 1024 * 1024]],
            "max_stack_depth": ["integer", [0, memory, 2 * 1024 * 1024]],
            "min_dynamic_shared_memory": ["integer", [0, memory, 0]],

            # === mem flags ===
            "huge_pages": ["enum", ["try", "on", "off"], "try"],
            "shared_memory_type": ["enum", ["mmap", "sysv", "windows"], "mmap"],  # TODO
            "dynamic_shared_memory_type": ["enum", ["posix", "sysv", "windows"], "posix"],  # TODO

            # === counted knobs ===
            "max_prepared_transactions": ["integer", [0, max_connections, max_connections]],
            "hash_mem_multiplier": ["float", [0.0, 4.0, 2.0]],

            # === disk knobs ===
            "temp_file_limit": ["integer", [0, disk, disk]],

            # === kernel process ===
            "max_files_per_process": ["integer", [1, max_files_per_process, 1000]],

            # === vacuum knobs ===
            # vacuum_cost_delay * accumulated_balance / vacuum_cost_limit
            # with a maximum of vacuum_cost_delay * 4. TODO - add this dependency
            "vacuum_cost_delay": ["integer", [0, 1000, 0]],
            "vacuum_cost_page_hit": ["integer", [0, 10, 1]],
            "vacuum_cost_page_miss": ["integer", [0, 10, 2]],
            "vacuum_cost_page_dirty": ["integer", [0, 100, 20]],
            "vacuum_cost_limit": ["integer", [0, 1000, 200]],

            # === background writer knobs ===
            # best - 10 ms, param can be set on the server cmd or postgresql.conf
            "bgwriter_delay": ["integer", [0, 1000, 200]],
            "bgwriter_lru_maxpages": ["integer", [0, 1000, 100]],
            # careful tuning
            "bgwriter_lru_multiplier": ["float", [0.01, 3.0, 2.0]],
            "bgwriter_flush_after": ["integer", [0, 2 * 1024 * 1024, 512 * 1024]],

            # === async behaviour knobs ===
            "backend_flush_after": ["integer", [0, 2 * 1024 * 1024, 0]],
            # if more ssd - higher value is avaible (100), depends on OS
            "effective_io_concurrency": ["integer", [0, 1000, 1]],
            "maintenance_io_concurrency": ["integer", [0, 100, 10]],
            "max_worker_processes": ["integer", [0, 16, 8]],
            # may consume more CPU time and be not effective
            "max_parallel_workers_per_gather": ["integer", [0, 4, 2]],
            # using in CREATE INDEX and VACUUM without FULL option
            "max_parallel_maintenance_workers": ["integer", [0, 4, 2]],
            "max_parallel_workers": ["integer", [0, 16, 8]],
            "parallel_leader_participation": ["boolean", ["true"]],
            # measuring in minutes. Maybe it is not a good feature
            "old_snapshot_threshold": ["integer", [-1, 24 * 60, -1]],

            # === WAL knobs ===
            # "wal_level": # cannot upgrade any performance
            "fsync": ["boolean", ["true"]],
            "synchronous_commit": ["enum", ["remote_apply", "on", "remote_write", "local", "off"], "on"],
            "wal_sync_method": ["enum", ["open_datasync", "fdatasync", "fsync", "fsync_writethrough", "open_sync"],
                                "fsync"],  # works if only fsync is false think about it
            "full_page_writes": ["boolean", "true"],
            "wal_log_hints": ["boolean", "false"],
            # maybe cannot tune this, because we need decode/encode data with all type of compression. Can raze a CPUtime
            "wal_compression": ["enum", ["pglz", "lz4", "zstd", "off"], "off"],
            # pglz, lz4, zstd params depends on how PostgreSQL was compiled
            "wal_init_zero": ["boolean", "false"],  # TODO need to know: is it OS a CoW OS? Or not?
            "wal_recycle": ["boolean", "true"],  # TODO the same issue
            "wal_buffers": ["integer", [64 * 1024, 32 * 1024 * 1024, 1 / 32 * 128 * 1024 * 1024]],
            # TODO 1/32 of shared_buffer
            "wal_writer_delay": ["integer", [10, 400, 200]],  # measured in ms
            "wal_writer_flush_after": ["integer", [0, 2 * 1024 * 1024, 1 * 1024 * 1024]],
            "wal_skip_threshold": ["integer", [8, 4 * 1024, 2 * 1024]],
            # measured in kB if value is specified without units
            "commit_delay": ["integer", [0, 100000, 0]],  # measured in micro seconds
            "commit_siblings": ["integer", [0, 10, 5]],

            # === checkpoints knobs ===
            "checkpoint_timeout": ["integer", [30, 24 * 60 * 60, 5 * 60]],  # helpful for recovery, maybe can turn off
            # maybe other cannot be helpful in performance gains

            # === sending servers knobs ===
            # thinks about replication parameters, thinks about how we can tune on the replica

            # === query planning ===
            "enable_async_append": ["boolean", "true"],
            "enable_bitmapscan": ["boolean", "true"],
            "enable_gathermerge": ["boolean", "true"],
            "enable_hashagg": ["boolean", "true"],
            "enable_hashjoin": ["boolean", "true"],
            "enable_incremental_sort": ["boolean", "true"],
            "enable_indexscan": ["boolean", "true"],
            "enable_indexonlyscan": ["boolean", "true"],
            "enable_material": ["boolean", "true"],
            "enable_memoize": ["boolean", "true"],
            "enable_mergejoin": ["boolean", "true"],
            "enable_nestloop": ["boolean", "true"],
            "enable_parallel_append": ["boolean", "true"],
            "enable_parallel_hash": ["boolean", "true"],
            "enable_partition_pruning": ["boolean", "true"],
            "enable_partitionwise_join": ["boolean", "true"],
            "enable_partitionwise_aggregate": ["boolean", "true"],
            "enable_presorted_aggregate": ["boolean", "true"],
            "enable_seqscan": ["boolean", "true"],
            "enable_sort": ["boolean", "true"],
            "enable_tidscan": ["boolean", "true"],

            # === planner cost constants knobs ===
            "seq_page_cost": ["float", [0.0, 1.0, 1.0]],
            "random_page_cost": ["float", [0.0, 6.0, 4.0]],
            "cpu_tuple_cost": ["float", [0.0, 0.5, 0.01]],
            "cpu_index_tuple_cost": ["float", [0.0, 0.5, 0.005]],
            "cpu_operator_cost": ["float", [0.0, 0.5, 0.0025]],
            "parallel_setup_cost": ["float", [0.0, 2000, 1000]],
            "parallel_tuple_cost": ["float", [0.0, 1.0, 0.1]],
            "min_parallel_table_scan_size": ["integer", [8 * 1024, 16 * 1024 * 1024, 8 * 1024 * 1024]],
            "min_parallel_index_scan_size": ["integer", [8 * 1024, 2 * 1024 * 1024, 512 * 1024]],
            "effective_cache_size": ["integer",
                                     [1 * 1024 * 1024 * 1024, 6 * 1024 * 1024 * 1024, 4 * 1024 * 1024 * 1024]],
            "jit_above_cost": ["float", [-1.0, 200000.0, 100000.0]],
            "jit_inline_above_cost": ["float", [-1.0, 1000000.0, 500000.0]],
            "jit_optimize_above_cost": ["float", [-1.0, 1000000.0, 500000.0]],

            # === genetic query optimizer knobs ===
            "geqo": ["boolean", "true"],
            "geqo_threshold": ["integer", [1, 24, 12]],
            "geqo_effort": ["integer", [1, 10, 5]],
            "geqo_pool_size": ["integer", [100, 1000, 0]],  # TODO add turning off flag
            "geqo_generations": ["integer", [0, 6, 0]],
            "geqo_selection_bias": ["integer", [1.50, 2.00, 2.00]],
            "geqo_seed": ["integer", [0.00, 1.00, 0.50]],

            # === other planning options knobs ===
            "default_statistics_target": ["integer", [50, 200, 100]],  # for ANALYZE
            "constraint_exclusion": ["enum", ["on", "off", "partition"], "partition"],
            "cursor_tuple_fraction": ["float", [0.01, 1.0, 0.1]],
            "from_collapse_limit": ["integer", [1, 16, 8]],
            "jit": ["boolean", "true"],
            "join_collapse_limit": ["integer", [1, 16, 8]],
            "plan_cache_mode": ["enum", ["auto", "force_custom_plan", "force_generic_plan"], "auto"],
            "recursive_worktable_factor": ["float", [1.0, 16.0, 10.0]],

            # === skipping logging knobs, because it is optional ===

            "track_activities": ["boolean", "true"],
            "track_activity_query_size": ["integer", [512, 2048, 1024]],  # measured in bytes
            "track_counts": ["boolean", "true"],
            "track_io_timing": ["boolean", "false"],
            "track_wal_io_timing": ["boolean", "false"],
            "track_functions": ["enum", ["p1", "all", "none"], "none"],
            "stats_fetch_consistency": ["enum", ["none", "cache", "snapshot"], "cache"],

            # === statistics monitoring ===
            "compute_query_id": ["enum", ["off", "on", "auto"], "auto"],

            # === automatic vacuuming ===
            "autovacuum": ["boolean", "true"],
            "autovacuum_max_workers": ["integer", [1, 6, 3]],
            "autovacuum_naptime": ["integer", [30, 180, 60]],
            "autovacuum_vacuum_threshold": ["integer", [25, 100, 50]],
            "autovacuum_vacuum_insert_threshold": ["integer", [-1, 2000, 1000]],  # TODO specific value -1
            "autovacuum_analyze_threshold": ["integer", [25, 100, 50]],
            "autovacuum_vacuum_scale_factor": ["float", [0.01, 0.4, 0.2]],
            "autovacuum_vacuum_insert_scale_factor": ["float", [0.01, 0.4, 0.2]],
            "autovacuum_analyze_scale_factor": ["float", [0.05, 0.4, 0.1]],
            # "autovacuum_freeze_max_age": ["integer", [150000000, 250000000, 200000000]],  # hard to tune
            # "autovacuum_multixact_freeze_max_age": ["integer", []]   # hard to tune
            "autovacuum_vacuum_cost_delay": ["float", [0.2, 4, 2]],  # TODO specific flag -1
            # "autovacuum_vacuum_cost_limit": ["integer", [-1, 2, 1]],   # hard to tune


            # === statement behavior ===
            "client_min_messages": ["enum", ["DEBUG5", "DEBUG4", "DEBUG3", "DEBUG2", "DEBUG1", "LOG", "NOTICE", "WARNING", "ERROR"], "NOTICE"],
            "default_transaction_isolation": ["enum", ["read uncommited", "read commited", "repeatable read", "serializable"], "read commited"],  # TODO need to think
            "default_transaction_read_only": ["boolean", "false"],
            "default_transaction_deferrable": ["boolean", "false"],  # if serializable
            # "statement_timeout": ["integer", [0, 100, 0]],  # not recommended for tuning by official documentation
            # "lock_timeout": ["integer", [0, 100, 0]],   # not recommended for tuning by official documentation
            "idle_in_transaction_session_timeout": ["integer", [0, 10000, 0]],
            "idle_session_timeout": ["integer", [0, 10000, 0]],
            "gin_pending_list_limit": ["integer", [1 * 1024 * 1024, 16 * 1024 * 1024, 4 * 1024 * 1024]],
            "gin_fuzzy_search_limit": ["integer", [1 * 1024 * 1024, 16 * 1024 * 1024, 4 * 1024 * 1024]],

            # === lock management ===
            "deadlock_timeout": ["integer", [1000, 20000, 1000]],
            "max_locks_per_transaction": ["integer", [32, 128, 64]],
            "max_pred_locks_per_transaction": ["integer", [32, 128, 64]],
            "max_pred_locks_per_page": ["integer", [2, 4, 2]],

            # === backward compatibility ===
            "array_nulls": ["boolean", "true"],
            "synchronize_seqscans": ["boolean", "true"],


            # ===  error handling ===
            "recovery_init_sync_method": ["enum", ["fsync", "syncfs"]],

            # === preset options ===
            # "block_size": ["integer", [8192, 32768, 8192]]   affects on many other parameters, hard to tune
            "shared_memory_size": ["integer", [1024 * 1024, 4 * 1024 * 1024, 1024 * 1024]],

        }
        self.knobs = extended_knobs

