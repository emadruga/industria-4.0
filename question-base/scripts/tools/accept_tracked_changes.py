#!/usr/bin/env python3
"""
Accept all tracked changes and remove comments from DOCX files.

This script processes DOCX files to finalize all pending edits by:
- Accepting all tracked changes
- Removing all comments
- Saving the clean version

Usage:
    python accept_tracked_changes.py <file_or_directory>
"""

import sys
import argparse
from pathlib import Path
from zipfile import ZipFile
import shutil
from lxml import etree

# XML namespaces used in DOCX files
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'w15': 'http://schemas.microsoft.com/office/word/2012/wordml',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006'
}


def accept_tracked_changes(docx_path):
    """
    Accept all tracked changes in a DOCX file by modifying its XML.

    Args:
        docx_path: Path to the DOCX file

    Returns:
        True if successful, False otherwise
    """
    docx_path = Path(docx_path)

    if not docx_path.exists():
        print(f"❌ File not found: {docx_path}")
        return False

    print(f"\nProcessing: {docx_path.name}")

    # Create backup
    backup_path = docx_path.with_suffix('.docx.backup')
    shutil.copy2(docx_path, backup_path)
    print(f"  📦 Backup created: {backup_path.name}")

    # Create temp directory
    temp_dir = docx_path.parent / f"_temp_{docx_path.stem}"
    temp_dir.mkdir(exist_ok=True)

    try:
        # Extract DOCX (it's a ZIP file)
        with ZipFile(docx_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Process document.xml
        doc_xml_path = temp_dir / 'word' / 'document.xml'
        if doc_xml_path.exists():
            changes_made = process_document_xml(doc_xml_path)
            if changes_made:
                print(f"  ✅ Accepted tracked changes in document.xml")

        # Remove comments.xml if it exists
        comments_path = temp_dir / 'word' / 'comments.xml'
        if comments_path.exists():
            comments_path.unlink()
            print(f"  ✅ Removed comments.xml")

            # Also remove comments reference from document.xml.rels
            rels_path = temp_dir / 'word' / '_rels' / 'document.xml.rels'
            if rels_path.exists():
                remove_comments_relationship(rels_path)

        # Remove commentsExtended.xml if it exists
        comments_ext_path = temp_dir / 'word' / 'commentsExtended.xml'
        if comments_ext_path.exists():
            comments_ext_path.unlink()
            print(f"  ✅ Removed commentsExtended.xml")

        # Repack into DOCX
        with ZipFile(docx_path, 'w') as zip_ref:
            for file_path in temp_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(temp_dir)
                    zip_ref.write(file_path, arcname)

        print(f"  ✅ Saved cleaned document")

        # Clean up temp directory
        shutil.rmtree(temp_dir)

        return True

    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        # Restore from backup
        if backup_path.exists():
            shutil.copy2(backup_path, docx_path)
            print(f"  ↩️  Restored from backup")
        # Clean up temp directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        return False


def process_document_xml(xml_path):
    """
    Process document.xml to accept all tracked changes.

    Tracked changes in Word are stored as:
    - <w:ins> - insertions
    - <w:del> - deletions
    - <w:moveFrom> - moved from
    - <w:moveTo> - moved to

    To accept changes:
    - Keep content inside <w:ins> and <w:moveTo>
    - Remove <w:del> and <w:moveFrom> entirely
    - Remove the wrapping change tags

    Args:
        xml_path: Path to document.xml

    Returns:
        True if changes were made, False otherwise
    """
    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(str(xml_path), parser)
    root = tree.getroot()

    changes_made = False

    # Accept insertions - unwrap content from <w:ins> tags
    for ins in root.findall('.//w:ins', NAMESPACES):
        # Move all children up to parent level
        parent = ins.getparent()
        index = list(parent).index(ins)
        for child in ins:
            parent.insert(index, child)
            index += 1
        parent.remove(ins)
        changes_made = True

    # Accept deletions - remove <w:del> tags entirely
    for del_elem in root.findall('.//w:del', NAMESPACES):
        parent = del_elem.getparent()
        parent.remove(del_elem)
        changes_made = True

    # Accept moves - handle moveTo (keep) and moveFrom (remove)
    for move_to in root.findall('.//w:moveTo', NAMESPACES):
        parent = move_to.getparent()
        index = list(parent).index(move_to)
        for child in move_to:
            parent.insert(index, child)
            index += 1
        parent.remove(move_to)
        changes_made = True

    for move_from in root.findall('.//w:moveFrom', NAMESPACES):
        parent = move_from.getparent()
        parent.remove(move_from)
        changes_made = True

    # Remove comment references
    for comment_ref in root.findall('.//w:commentReference', NAMESPACES):
        parent = comment_ref.getparent()
        parent.remove(comment_ref)
        changes_made = True

    for comment_range_start in root.findall('.//w:commentRangeStart', NAMESPACES):
        parent = comment_range_start.getparent()
        parent.remove(comment_range_start)
        changes_made = True

    for comment_range_end in root.findall('.//w:commentRangeEnd', NAMESPACES):
        parent = comment_range_end.getparent()
        parent.remove(comment_range_end)
        changes_made = True

    # Save modified XML
    if changes_made:
        tree.write(str(xml_path), xml_declaration=True, encoding='UTF-8', standalone=True)

    return changes_made


def remove_comments_relationship(rels_path):
    """Remove comments relationship from document.xml.rels"""
    try:
        parser = etree.XMLParser(remove_blank_text=False)
        tree = etree.parse(str(rels_path), parser)
        root = tree.getroot()

        # Namespace for relationships
        rels_ns = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}

        # Remove comments relationship
        for rel in root.findall('.//r:Relationship[@Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"]', rels_ns):
            root.remove(rel)

        # Remove commentsExtended relationship
        for rel in root.findall('.//r:Relationship[@Type="http://schemas.microsoft.com/office/2011/relationships/commentsExtended"]', rels_ns):
            root.remove(rel)

        tree.write(str(rels_path), xml_declaration=True, encoding='UTF-8', standalone=True)
    except Exception as e:
        print(f"  ⚠️  Could not update relationships: {e}")


def process_directory(directory_path, pattern="*.docx"):
    """Process all DOCX files in a directory."""
    directory_path = Path(directory_path)

    if not directory_path.exists():
        print(f"❌ Directory not found: {directory_path}")
        return

    docx_files = list(directory_path.glob(pattern))

    # Exclude backup and temporary files
    docx_files = [f for f in docx_files if not f.name.startswith('~$') and '.backup' not in f.name]

    if not docx_files:
        print(f"No DOCX files found in {directory_path}")
        return

    print(f"Found {len(docx_files)} DOCX files")

    success_count = 0
    for docx_file in docx_files:
        if accept_tracked_changes(docx_file):
            success_count += 1

    print(f"\n{'='*60}")
    print(f"SUMMARY: {success_count}/{len(docx_files)} files processed successfully")
    print(f"{'='*60}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Accept all tracked changes and remove comments from DOCX files'
    )
    parser.add_argument('path', help='Path to DOCX file or directory')
    parser.add_argument('-p', '--pattern', default='*.docx',
                        help='File pattern for directory processing (default: *.docx)')

    args = parser.parse_args()

    path = Path(args.path)

    if path.is_file():
        accept_tracked_changes(path)
    elif path.is_dir():
        process_directory(path, args.pattern)
    else:
        print(f"❌ Invalid path: {path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
