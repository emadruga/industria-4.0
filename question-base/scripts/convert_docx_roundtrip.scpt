-- AppleScript to convert DOCX -> DOC -> DOCX (flattens tracked changes)
-- This forces Word to accept all changes and finalize the document

on run argv
	if (count of argv) < 1 then
		display dialog "Usage: osascript convert_docx_roundtrip.scpt <path_to_docx_file>"
		return
	end if

	set docxFile to POSIX file (item 1 of argv) as alias

	tell application "Microsoft Word"
		activate

		-- Open the DOCX file
		open docxFile

		-- Get the active document
		set theDoc to active document
		set docPath to path of theDoc

		-- Create .doc path (replace .docx with .doc)
		set docPath to text 1 thru -6 of docPath & ".doc"

		-- Save as .doc (Word 97-2004 format)
		-- Format code 0 = Word 97-2004 Document (.doc)
		save as theDoc file name docPath file format format document97

		-- Close the document
		close theDoc saving no

		-- Open the .doc file
		set docFile to POSIX file docPath as alias
		open docFile

		set theDoc to active document

		-- Save back as .docx (modern format)
		-- Format code 12 = Word Document (.docx)
		set docxPath to text 1 thru -5 of docPath & ".docx"
		save as theDoc file name docxPath file format format document

		-- Close the document
		close theDoc saving no

		-- Delete the temporary .doc file
		tell application "Finder"
			delete (POSIX file docPath as alias)
		end tell

		quit
	end tell

	return "Successfully converted: " & docxPath
end run
