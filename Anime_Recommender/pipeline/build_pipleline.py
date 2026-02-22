import sys
from pathlib import Path

# Add project root to path so imports work correctly
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)
# this pipeline to build an vector store 
def main():
    try:
        logger.info("Starting to build pipeline")
        # Construct absolute paths using project root
        csv_path = project_root / "data" / "anime_with_synopsis.csv"
        processed_csv_path = project_root / "data" / "anime_updated.csv"
        
        loader = AnimeDataLoader(str(csv_path), str(processed_csv_path))
        processed_csv = loader.load_and_process()
        logger.info("Data loaded and processed successfully")
        vector_builder = VectorStoreBuilder(csv_path=processed_csv)
        
        vector_builder.build_and_save_vectorstore()
        logger.info("Vector store built successfully...")
        
        logger.info("Pipeline built successfully")
        
        
    except Exception as e:
        logger.info(f"failed to execute pipeline {str(e)}")
        raise CustomException("Error during pipeline initialization", e)

if __name__ == "__main__":
    main()