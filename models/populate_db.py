import csv
import argparse
from pathlib import Path
from .database import engine
from sqlmodel import Session, SQLModel
from models.tables import Group, Word, WordProgress

def erase_database():
    """Erase and recreate all tables, then add default settings."""
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
 
def populate_from_csv(csv_path: str, erase_first: bool = False):
    """Populate the database with words and groups from a CSV file.

    Parameters
    ----------
    csv_path : str
        Path to the CSV file containing word data
    erase_first : bool, optional
        If True, erases the database before populating, by default False

    Notes
    -----
    Expected CSV columns:
    - group: The group/category name for the word
    - primary_text: The word in the primary language
    - secondary_text: The word in the secondary language
    - mnemonic: Optional mnemonic device (can be empty)
    """
    if erase_first:
        erase_database()
    
    with Session(engine) as session:
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # Track groups to avoid duplicates
            groups = {}
            
            for row in csv_reader:
                group_name = row.get('group', '').strip()
                primary_text = row.get('english', '').strip()
                secondary_text = row.get('russian', '').strip()
                mnemonic = row.get('mnemonic', '').strip()  # Optional
                
                if not all([group_name, primary_text, secondary_text]):
                    continue
                
                # Get or create group
                if group_name not in groups:
                    group = Group(name=group_name)
                    session.add(group)
                    session.flush()  # To get the group ID
                    groups[group_name] = group
                else:
                    group = groups[group_name]
                
                # Create word (mnemonic will be None if not provided)
                word_entry = Word(
                    primary_text=primary_text,
                    secondary_text=secondary_text,
                    mnemonic=mnemonic if mnemonic else None,
                    group_id=group.id
                )
                session.add(word_entry)
            
            session.commit()

def populate_all_csvs(csv_path: str, erase_first: bool = False):
    if erase_first:
        erase_database()
    
    csv_path = Path(csv_path)
    if csv_path.is_dir():
        for csv_file in csv_path.glob("*.csv"):
            populate_from_csv(str(csv_file), erase_first=False)
    else:
        populate_from_csv(csv_path, erase_first=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Populate database from CSV files')
    parser.add_argument('--csv_path', help='Path to a single CSV file')
    parser.add_argument('--csv_dir', help='Path to directory containing CSV files')
    parser.add_argument('--erase', action='store_true', help='Erase database before populating')
    args = parser.parse_args()
    
    if args.csv_dir:
        populate_all_csvs(args.csv_dir, args.erase)
    elif args.csv_path:
        populate_from_csv(args.csv_path, args.erase)
    else:
        print("Please provide either --csv_path or --csv_dir")
