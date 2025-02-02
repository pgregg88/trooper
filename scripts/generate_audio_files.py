"""Script to generate audio file structure for Stormtrooper quotes."""

import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.quotes import QuoteManager, Quote
from src.audio.effects import StormtrooperEffect
from src.audio.utils import generate_filename

def check_directories(root_dir: Path) -> Tuple[List[Path], List[Path]]:
    """Check which required directories exist and which need to be created.
    
    Args:
        root_dir: Project root directory
        
    Returns:
        Tuple of (existing directories, missing directories)
    """
    required_dirs = [
        root_dir / "assets" / "audio" / "polly_raw",
        root_dir / "assets" / "audio" / "processed"
    ]
    
    existing = []
    missing = []
    
    for dir_path in required_dirs:
        if dir_path.exists():
            existing.append(dir_path)
            logger.info(f"Found existing directory: {dir_path}")
        else:
            missing.append(dir_path)
            logger.warning(f"Missing directory: {dir_path}")
    
    return existing, missing

def create_directories(directories: List[Path]) -> None:
    """Create the specified directories.
    
    Args:
        directories: List of directories to create
    """
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")

def get_required_files(quote_manager: QuoteManager, root_dir: Path) -> Dict[Path, Quote]:
    """Get mapping of required audio files to their quotes.
    
    Args:
        quote_manager: Quote manager instance
        root_dir: Project root directory
        
    Returns:
        Dictionary mapping file paths to quotes
    """
    required_files = {}
    voice = "Matthew"  # Only using Matthew's voice
    
    # Group quotes by category and context
    quote_groups = {}
    for quote in quote_manager.quotes:
        key = (quote.category.value, quote.context)
        if key not in quote_groups:
            quote_groups[key] = []
        quote_groups[key].append(quote)
    
    # Generate filenames with indices
    for (category, context), quotes in quote_groups.items():
        for i, quote in enumerate(quotes):
            filename = generate_filename(voice, quote, i)
            filepath = root_dir / "assets" / "audio" / "polly_raw" / filename
            required_files[filepath] = quote
    
    return required_files

def check_audio_files(required_files: Dict[Path, Quote]) -> Tuple[Dict[Path, Quote], Dict[Path, Quote]]:
    """Check which required audio files exist and which need to be created.
    
    Args:
        required_files: Dictionary mapping file paths to quotes
        
    Returns:
        Tuple of (existing files mapping, missing files mapping)
    """
    existing = {f: q for f, q in required_files.items() if f.exists()}
    missing = {f: q for f, q in required_files.items() if not f.exists()}
    
    if existing:
        logger.info(f"Found {len(existing)} existing audio files")
        for f in sorted(existing.keys()):
            logger.debug(f"Found: {f.name}")
    
    if missing:
        logger.warning(f"Missing {len(missing)} audio files")
        for f, q in sorted(missing.items()):
            logger.debug(f"Missing: {f.name} -> {q.text}")
    
    return existing, missing

def process_audio_files(files_to_process: Dict[Path, Quote], effect: StormtrooperEffect) -> None:
    """Process audio files with Stormtrooper effect.
    
    Args:
        files_to_process: Dictionary mapping file paths to quotes
        effect: StormtrooperEffect instance
    """
    for filepath, quote in files_to_process.items():
        if filepath.exists():
            try:
                # Process the file with appropriate urgency
                processed_file = effect.process_file(
                    filepath,
                    urgency=quote.urgency
                )
                logger.info(f"Processed: {filepath.name} -> {Path(processed_file).name}")
            except Exception as e:
                logger.error(f"Failed to process {filepath.name}: {str(e)}")
        else:
            logger.warning(f"Cannot process missing file: {filepath.name}")

def generate_audio_files(root_dir: Path, dry_run: bool = False) -> None:
    """Generate audio file structure.
    
    Args:
        root_dir: Project root directory
        dry_run: If True, only check what needs to be done without making changes
    """
    # Check directory structure
    existing_dirs, missing_dirs = check_directories(root_dir)
    
    # Initialize components
    quotes_file = root_dir / "config" / "quotes.yaml"
    quote_manager = QuoteManager(quotes_file)
    effect = StormtrooperEffect()
    
    # Get required files
    required_files = get_required_files(quote_manager, root_dir)
    
    # Check existing files
    existing_files, missing_files = check_audio_files(required_files)
    
    if dry_run:
        logger.info("Dry run complete. No changes made.")
        return
    
    # Create missing directories
    if missing_dirs:
        logger.info(f"Creating {len(missing_dirs)} missing directories")
        create_directories(missing_dirs)
    
    # Process existing files
    if existing_files:
        logger.info(f"Processing {len(existing_files)} existing audio files")
        process_audio_files(existing_files, effect)
    
    # Report missing files that need to be created
    if missing_files:
        logger.warning(
            f"Missing {len(missing_files)} audio files that need to be created with AWS Polly:\n" +
            "\n".join(f"- {f.name}: {q.text}" for f, q in missing_files.items())
        )
    
    logger.info("Audio file structure is complete")
    logger.info(f"Total directories: {len(existing_dirs) + len(missing_dirs)}")
    logger.info(f"Total audio files needed: {len(required_files)}")
    logger.info(f"Files to create with Polly: {len(missing_files)}")

def main():
    """Run the audio file generation script."""
    # First do a dry run to check what exists
    logger.info("Performing dry run to check existing files...")
    generate_audio_files(project_root, dry_run=True)
    
    # Ask for confirmation before making changes
    response = input("\nWould you like to process the existing audio files? [y/N] ")
    if response.lower() == 'y':
        logger.info("Processing audio files...")
        generate_audio_files(project_root, dry_run=False)
    else:
        logger.info("No changes made.")

if __name__ == "__main__":
    main() 