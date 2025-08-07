import time, logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.conf import settings
from django.db import transaction, connections
from .base_loader import BaseLoader
from .utils import strfelapsed
from types import SimpleNamespace

logger = logging.getLogger(__name__)

class EtoolsLoader(BaseLoader):
    def load(self, *, countries=None, workers=None,
             ignore_errors=None, verbosity=0, stdout=None, **kwargs):
        conn = connections['etools']
        raw = countries or conn.get_tenants()
        # wrap strings if any
        if raw and isinstance(raw[0], str):
            countries = [SimpleNamespace(name=c.title(), schema_name=c) for c in raw]
        else:
            countries = raw

        workers = workers or settings.ETL_PARALLEL_WORKERS
        ignore_errors = (ignore_errors if ignore_errors is not None
                         else settings.ETL_IGNORE_ERRORS)

        if workers > 1:
            return self._load_parallel(countries, workers,
                                       ignore_errors, verbosity, stdout)
        return self._load_sequential(countries, verbosity, stdout)

    def _load_sequential(self, countries, verbosity, stdout):
        self.results = []
        total = len(countries)
        for idx, country in enumerate(countries, 1):
            if stdout and verbosity>0:
                stdout.write(f"{idx}/{total} {country.name} … ")
            self._process_one(country, verbosity, stdout)
        return self.results

    def _load_parallel(self, countries, workers,
                       ignore_errors, verbosity, stdout):
        self.results = []
        errors = {}
        with ThreadPoolExecutor(max_workers=workers) as pool:
            future_map = {
                pool.submit(self._process_one, country, verbosity, stdout): country
                for country in countries
            }
            for f in as_completed(future_map):
                c = future_map[f]
                try:
                    self.results.append(f.result())
                except Exception:
                    errors[c.schema_name] = True
                    logger.error(f"[{c.schema_name}] failed", exc_info=True)
                    if not ignore_errors:
                        raise
        if errors:
            logger.warning(f"Failed countries: {list(errors)}")
        return self.results

    def _process_one(self, country, verbosity, stdout):
        sid = transaction.savepoint()
        try:
            self.context['country'] = country
            connections['etools'].set_schemas([country.schema_name])
            start = time.time()

            self.process_country()
            self.post_process_country()
            if self.config.sync_deleted_records(self):
                self.remove_deleted()

            elapsed = time.time() - start
            transaction.savepoint_commit(sid)
            if stdout and verbosity>0:
                stdout.write(f"in {strfelapsed(elapsed)}\n")
            return {'country': country.schema_name, 'time': elapsed}
        except Exception:
            transaction.savepoint_rollback(sid)
            raise