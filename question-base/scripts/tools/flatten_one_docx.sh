#!/bin/bash
# Convert one DOCX file through DOC format to flatten changes

if [ $# -eq 0 ]; then
    echo "Usage: $0 <path_to_docx_file>"
    exit 1
fi

DOCX_FILE="$1"

if [ ! -f "$DOCX_FILE" ]; then
    echo "❌ File not found: $DOCX_FILE"
    exit 1
fi

# Get file path components
DIRNAME=$(dirname "$DOCX_FILE")
BASENAME=$(basename "$DOCX_FILE" .docx)
DOC_FILE="$DIRNAME/${BASENAME}.doc"

echo "Converting: $DOCX_FILE"
echo "  → Saving as .doc format..."

osascript - "$DOCX_FILE" "$DOC_FILE" <<'APPLESCRIPT'
on run argv
    set docxPath to item 1 of argv
    set docPath to item 2 of argv

    tell application "Microsoft Word"
        activate

        -- Open DOCX
        open POSIX file docxPath
        set theDoc to active document

        -- Save as DOC
        save as theDoc file name docPath file format format document97
        close theDoc saving no

        return "Saved as .doc"
    end tell
end run
APPLESCRIPT

if [ $? -ne 0 ]; then
    echo "  ❌ Failed to save as .doc"
    exit 1
fi

echo "  ✅ Saved as .doc"
echo "  → Converting back to .docx..."

osascript - "$DOC_FILE" "$DOCX_FILE" <<'APPLESCRIPT'
on run argv
    set docPath to item 1 of argv
    set docxPath to item 2 of argv

    tell application "Microsoft Word"
        activate

        -- Open DOC
        open POSIX file docPath
        set theDoc to active document

        -- Save as DOCX
        save as theDoc file name docxPath file format format document
        close theDoc saving no

        return "Saved as .docx"
    end tell
end run
APPLESCRIPT

if [ $? -ne 0 ]; then
    echo "  ❌ Failed to save as .docx"
    exit 1
fi

echo "  ✅ Converted back to .docx"

# Delete temporary .doc file
if [ -f "$DOC_FILE" ]; then
    rm "$DOC_FILE"
    echo "  🗑️  Removed temporary .doc file"
fi

echo "✅ Done: $DOCX_FILE"
