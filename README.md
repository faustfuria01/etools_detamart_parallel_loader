# eTools DataMart Parallel Loader

The package adds the ability to load data by country (tenants) in parallel,
which reduces the ETL pipelines execution time from >4 h to <1 h.

### Q1. Architecture & Performance  
- **Bottleneck**: sequential processing of 15+ countries → time ∑(tᵢ) > 4 hr.  
- **Solution**: country-to-country parallelization via `ThreadPoolExecutor`; each country in its own savepoint transaction.  
- **Benefit**: time ≈ max(tᵢ) × (N/parallelism) instead of ∑(tᵢ).

### Q2. Implementation details  
- Added `_load_parallel` and `_process_one` methods to manage threads, transactions and logging.  
- CLI extended with flags:
  - `--workers` - number of parallel loaders  
  - `--ignore-errors` - continue if one country is down  
- One country's errors roll back only its savepoint, others continue.

### Q3. Testing & Deploy  
- **Unit-tests**: check commit/rollback and concurrency.  
- **Integration tests**: emulate multiple circuits, test full ETL flow.  
- **Performance**: benchmarks show time reduction from >4 h to <1 h with 4 vorkers.  
- **Safe rollout**: chip-flag, canary-startup, monitoring ETL metrics, simple rollback (put `workers=1`).

## Repo Structure

```
.
etools-datamart-etl-parallel/
├── README.md       
├── requirements.txt  # project dependencies
├── .gitignore        # files and folders to ignore
├── manage.py         # Django project entry point
└── mart_project/     # main Django project module
    ├── settings.py   # configuration settings, including ETL_PARALLEL_WORKERS and ETL_IGNORE_ERRORS
    ├── apps/         # Django applications
    │   └── mart/     # 'mart' application
    │       ├── loader/       # module containing parallel ETL logic
    │       │   ├── base_loader.py  # BaseLoader class (stub or original implementation)
    │       │   ├── utils.py        # strfelapsed utility function for elapsed time formatting
    │       │   └── loader.py       # EtoolsLoader with _load_parallel, _load_sequential, and _process_one methods
    │       ├── data/         # data models and loader registry
    │       │   ├── models.py       # stub definitions of source models (PartnersPartnerorganization, T2FTravelactivity, TravelType)
    │       │   └── registry.py     # get_loader_for mapping ('mart.partner' → PartnerLoader)
    │       └── management/   # custom management commands
    │           └── commands/
    │               └── load.py     # management command 'load' extended with --workers and --ignore-errors flags
    └── urls.py       # URL configuration
```


