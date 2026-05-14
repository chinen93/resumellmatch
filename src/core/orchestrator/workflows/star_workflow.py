"""STAR entries workflow orchestration.

This module handles the workflow for processing STAR (Situation, Task, Action, Result)
interview response data from CSV files, including both metadata and individual entries.
"""

from config.logging import get_logger
from src.core.importer import StarEntryImporter, StarMetadataImporter
from src.core.processor import StarEntryProcessor, StarMetadataProcessor
from src.data_ingestion import CSVLoader


def run_star_workflow():
    """Execute the STAR entries processing workflow.

    Imports STAR interview responses from CSV files into the system.
    Processes both metadata (experience context) and individual entries (STAR stories).

    Workflow:
        1. Load STAR metadata from CSV (star_metadata.csv)
        2. Process and validate metadata entries
        3. Load STAR entries from CSV (star_entries.csv)
        4. Process and validate individual stories
    """
    log = get_logger("StarWorkflow")
    log.info("Starting STAR responses workflow")

    csv_loader = CSVLoader()
    log.debug("CSV loader initialized")

    # Process STAR metadata
    log.info("Processing STAR metadata from CSV")
    star_metadata_processor = StarMetadataProcessor(isTest=False)
    star_metadata_importer = StarMetadataImporter(
        loader=csv_loader, processor=star_metadata_processor
    )
    star_metadata_importer.run(filename="star/star_metadata.csv")
    log.debug("STAR metadata processing completed")

    # Process STAR entries
    log.info("Processing STAR entries from CSV")
    star_entry_processor = StarEntryProcessor(isTest=False)
    star_entry_importer = StarEntryImporter(
        loader=csv_loader, processor=star_entry_processor
    )
    star_entry_importer.run(filename="star/star_entries.csv")
    log.debug("STAR entries processing completed")

    log.info("STAR responses workflow completed")
