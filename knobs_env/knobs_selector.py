from knobs import Knobs


class KnobsSelector:
    def __init__(self):
        self.knobs = Knobs()

    def select_and_evaluate(self):
        selected_knobs = {
            "autovacuum_work_mem": self.evaluate_knob("autovacuum_work_mem"),
            "effective_cache_size": self.evaluate_knob("effective_cache_size"),
            "max_wal_size": self.evaluate_knob("max_wal_size"),
            "min_wal_size": self.evaluate_knob("min_wal_size"),
            "shared_buffers": self.evaluate_knob("shared_buffers"),
            "temp_buffers": self.evaluate_knob("temp_buffers"),
            "wal_buffers": self.evaluate_knob("wal_buffers"),
            "work_mem": self.evaluate_knob("work_mem"),
            "autovacuum_max_workers": self.evaluate_knob("autovacuum_max_workers"),
            "autovacuum_naptime": self.evaluate_knob("autovacuum_naptime"),
            "bgwriter_delay": self.evaluate_knob("bgwriter_delay"),
            "bgwriter_lru_maxpages": self.evaluate_knob("bgwriter_lru_maxpages"),
            "bgwriter_lru_multiplier": self.evaluate_knob("bgwriter_lru_multiplier"),
            "checkpoint_completion_target": self.evaluate_knob("checkpoint_completion_target"),
            "checkpoint_timeout": self.evaluate_knob("checkpoint_timeout"),
            "commit_delay": self.evaluate_knob("commit_delay"),
            "default_statistics_target": self.evaluate_knob("default_statistics_target"),
            "fillfactor": self.evaluate_knob("fillfactor"),
            "hash_mem_multiplier": self.evaluate_knob("hash_mem_multiplier"),
            "pg_prewarm.autoprewarm_interval": self.evaluate_knob("pg_prewarm.autoprewarm_interval"),
            "synchronous_commit": self.evaluate_knob("synchronous_commit"),
            "enable_memoize": self.evaluate_knob("enable_memoize"),
            "wal_compression": self.evaluate_knob("wal_compression"),
            "wal_level": self.evaluate_knob("wal_level"),
            "wal_recycle": self.evaluate_knob("wal_recycle"),
            "wal_sync_method": self.evaluate_knob("wal_sync_method"),
        }
        return selected_knobs

    def evaluate_knob(self, knob_name):
        knob_info = self.knobs.knobs(knob_name, None)
        if knob_info:
            return knob_info
