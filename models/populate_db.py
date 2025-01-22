import csv
import argparse
from .database import engine
from sqlmodel import Session, SQLModel
from models.tables import Group, Word

def populate_from_csv(csv_path: str, erase_first: bool = False):
    if erase_first:
        # Drop all tables and recreate them
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # Track groups to avoid duplicates
            groups = {}
            
            for row in csv_reader:
                group_name = row.get('group', '').strip()
                english = row.get('english', '').strip()
                russian = row.get('russian', '').strip()
                mnemonic = row.get('mnemonic', '').strip()  # Now optional
                
                if not all([group_name, english, russian]):  # Removed mnemonic from required fields
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
                    english=english,
                    russian=russian,
                    mnemonic=mnemonic if mnemonic else None,
                    group_id=group.id
                )
                session.add(word_entry)
            
            session.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Populate database from CSV file')
    parser.add_argument('--csv_path', default="words.csv", help='Path to the CSV file')
    parser.add_argument('--erase', action='store_true', help='Erase database before populating')
    args = parser.parse_args()
    
    populate_from_csv(args.csv_path, args.erase)
