#!/bin/bash
# Flatten all tracked changes in Word documents by converting DOCX -> DOC -> DOCX

# Directory containing the files
DOCX_DIR="/Users/emadruga/proj/industria-4.0/mdic-suframa/templates/Organização"

# Files to process
FILES=(
    "Organizacao - Desenvolvimento profissional continuo.docx"
    "Organizacao - Prover competencias digitais.docx"
    "Organizacao - Reconhecer o valor dos erros.docx"
)

echo "========================================="
echo "Flattening Word documents"
echo "========================================="
echo ""

for file in "${FILES[@]}"; do
    filepath="$DOCX_DIR/$file"
    echo "Processing: $file"

    if [ ! -f "$filepath" ]; then
        echo "  ❌ File not found: $filepath"
        continue
    fi

    # Run the conversion using AppleScript
    osascript <<EOF
        set docxFile to POSIX file "$filepath" as alias

        tell application "Microsoft Word"
            activate

            -- Open the DOCX file
            open docxFile

            -- Get the active document
            set theDoc to active document
            set docPath to path of theDoc

            -- Create .doc path
            set docPath to text 1 thru -6 of docPath & ".doc"

            -- Save as .doc (Word 97-2004 format - code 0)
            save as theDoc file name docPath file format format document97

            -- Close
            close theDoc saving no

            -- Open the .doc file
            set docFile to POSIX file docPath as alias
            open docFile

            set theDoc to active document

            -- Save back as .docx
            set docxPath to text 1 thru -5 of docPath & ".docx"
            save as theDoc file name docxPath file format format document

            -- Close
            close theDoc saving no
        end tell

        -- Delete the temporary .doc file
        tell application "Finder"
            delete (POSIX file docPath as alias)
        end tell

        return "✅ Converted: $file"
EOF

    if [ $? -eq 0 ]; then
        echo "  ✅ Success"
    else
        echo "  ❌ Failed"
    fi
    echo ""
done

echo "========================================="
echo "Done! Files have been flattened."
echo "========================================="
