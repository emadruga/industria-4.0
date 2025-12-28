#!/usr/bin/env python3
"""
Evidence Format Analysis Script

Purpose: Analyze evidence format across multiple authors' DOCX documents
to understand structural patterns, variations, and extraction challenges.

Phase: 2.3 - Test extraction on multiple authors' documents
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from docx import Document
import re
from collections import defaultdict
import json

class EvidenceFormatAnalyzer:
    """Analyzes evidence format patterns across DOCX files from different authors."""

    def __init__(self, docx_directory: str):
        self.docx_dir = Path(docx_directory)
        self.analysis_results = {
            "files_analyzed": [],
            "authors": {},
            "section_patterns": defaultdict(int),
            "evidence_categories": defaultdict(set),
            "formatting_styles": defaultdict(list),
            "level_patterns": defaultdict(int),
            "quality_issues": [],
            "recommendations": []
        }

    def analyze_all_documents(self, limit: int = None) -> Dict:
        """
        Analyze all DOCX files in the directory.

        Args:
            limit: Maximum number of files to analyze (None for all)

        Returns:
            Dictionary containing comprehensive analysis results
        """
        # Search for DOCX files recursively (handles subdirectories by author)
        docx_files = list(self.docx_dir.glob("*.docx")) + list(self.docx_dir.glob("**/*.docx"))

        # Filter out temporary files and duplicates
        docx_files = [f for f in docx_files if not f.name.startswith('~$')]
        docx_files = list(set(docx_files))  # Remove duplicates
        docx_files.sort()  # Sort for consistent ordering

        if limit:
            docx_files = docx_files[:limit]

        print(f"📂 Found {len(docx_files)} DOCX files to analyze")
        print(f"📍 Directory: {self.docx_dir}\n")

        for i, docx_path in enumerate(docx_files, 1):
            print(f"[{i}/{len(docx_files)}] Analyzing: {docx_path.name}")
            try:
                self._analyze_single_document(docx_path)
            except Exception as e:
                print(f"  ⚠️  Error: {e}")
                self.analysis_results["quality_issues"].append({
                    "file": docx_path.name,
                    "issue": f"Analysis failed: {str(e)}"
                })

        self._generate_recommendations()
        return self.analysis_results

    def _analyze_single_document(self, docx_path: Path):
        """Analyze a single DOCX document for evidence patterns."""
        doc = Document(docx_path)
        file_info = {
            "filename": docx_path.name,
            "author": None,
            "sections_found": {},
            "evidence_structure": {},
            "text_sample": ""
        }

        # Extract author from document properties
        try:
            file_info["author"] = doc.core_properties.author or "Unknown"
        except:
            file_info["author"] = "Unknown"

        # Extract full text
        full_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

        # Find evidence sections
        evidence_section = self._extract_evidence_section(full_text)

        if evidence_section:
            file_info["evidence_structure"] = self._analyze_evidence_structure(
                evidence_section,
                docx_path.name
            )
            file_info["text_sample"] = evidence_section[:500] + "..." if len(evidence_section) > 500 else evidence_section
            file_info["sections_found"]["evidence"] = True
        else:
            file_info["sections_found"]["evidence"] = False
            self.analysis_results["quality_issues"].append({
                "file": docx_path.name,
                "issue": "No evidence section found"
            })

        # Store file info
        self.analysis_results["files_analyzed"].append(file_info)

        # Group by author
        author = file_info["author"]
        if author not in self.analysis_results["authors"]:
            self.analysis_results["authors"][author] = {
                "files": [],
                "common_patterns": []
            }
        self.analysis_results["authors"][author]["files"].append(docx_path.name)

    def _extract_evidence_section(self, text: str) -> str:
        """Extract the evidence section from document text."""
        # Pattern variations to search for
        patterns = [
            r'C\)\s*Sinais por n[ií]vel[:\s]+(.*?)(?=D\)|$)',
            r'Sinais por n[ií]vel[:\s]+(.*?)(?=D\)|$)',
            r'C\)\s*SINAIS POR N[ÍI]VEL[:\s]+(.*?)(?=D\)|$)',
            r'SINAIS POR N[ÍI]VEL[:\s]+(.*?)(?=D\)|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                self.analysis_results["section_patterns"][pattern] += 1
                return match.group(1).strip()

        # Try alternative patterns
        alt_patterns = [
            r'Evidências[:\s]+(.*?)(?=\n[A-Z]\)|$)',
            r'Evidence[:\s]+(.*?)(?=\n[A-Z]\)|$)'
        ]

        for pattern in alt_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                self.analysis_results["section_patterns"][pattern] += 1
                return match.group(1).strip()

        return ""

    def _analyze_evidence_structure(self, evidence_text: str, filename: str) -> Dict:
        """Analyze the structure of an evidence section."""
        structure = {
            "has_level_markers": False,
            "level_format": None,
            "levels_found": [],
            "has_category_headers": False,
            "categories_found": [],
            "formatting_type": "unknown",
            "list_style": None
        }

        # Check for level markers (N0, N1, etc.)
        level_patterns = [
            (r'N(\d):', "N0: format"),
            (r'N[ií]vel\s+(\d):', "Nível 0: format"),
            (r'Level\s+(\d):', "Level 0: format"),
            (r'(\d)\s*[-–—]\s*', "0 - format")
        ]

        for pattern, format_name in level_patterns:
            matches = re.finditer(pattern, evidence_text, re.IGNORECASE)
            levels = [match.group(1) for match in matches]
            if levels:
                structure["has_level_markers"] = True
                structure["level_format"] = format_name
                structure["levels_found"] = sorted(set(levels))
                self.analysis_results["level_patterns"][format_name] += 1
                break

        # Check for category headers
        category_patterns = {
            "artifacts": r'Artefatos[:\s]',
            "metrics": r'M[ée]tricas|KPIs?[:\s]',
            "behaviors": r'Comportamentos|Sinais\s+observ[aá]veis[:\s]',
            "questions": r'Perguntas|Quest[õo]es[:\s]'
        }

        for category, pattern in category_patterns.items():
            if re.search(pattern, evidence_text, re.IGNORECASE):
                structure["has_category_headers"] = True
                structure["categories_found"].append(category)
                self.analysis_results["evidence_categories"][category].add(filename)

        # Detect formatting type
        if structure["has_level_markers"] and structure["has_category_headers"]:
            structure["formatting_type"] = "structured"
        elif structure["has_level_markers"]:
            structure["formatting_type"] = "semi-structured"
        else:
            structure["formatting_type"] = "prose"

        # Detect list style
        if re.search(r'^\s*•', evidence_text, re.MULTILINE):
            structure["list_style"] = "bullets"
        elif re.search(r'^\s*\d+\.', evidence_text, re.MULTILINE):
            structure["list_style"] = "numbered"
        elif re.search(r'^\s*[-–—]', evidence_text, re.MULTILINE):
            structure["list_style"] = "dashes"
        else:
            structure["list_style"] = "paragraph"

        self.analysis_results["formatting_styles"][structure["formatting_type"]].append(filename)

        return structure

    def _generate_recommendations(self):
        """Generate recommendations based on analysis."""
        recommendations = []

        # Check formatting consistency
        total_files = len(self.analysis_results["files_analyzed"])
        structured_count = len(self.analysis_results["formatting_styles"]["structured"])
        prose_count = len(self.analysis_results["formatting_styles"]["prose"])

        if structured_count / total_files < 0.5:
            recommendations.append({
                "priority": "HIGH",
                "issue": f"Only {structured_count}/{total_files} files use structured format",
                "action": "Create DOCX template with clear category headers (Artefatos, Métricas, Comportamentos, Perguntas)"
            })

        if prose_count > 0:
            recommendations.append({
                "priority": "MEDIUM",
                "issue": f"{prose_count} files use prose format without level markers",
                "action": "Enhance extraction script with NLP-based parsing for prose content"
            })

        # Check level coverage
        all_levels_found = set()
        for file_info in self.analysis_results["files_analyzed"]:
            if "evidence_structure" in file_info and file_info["evidence_structure"].get("levels_found"):
                all_levels_found.update(file_info["evidence_structure"]["levels_found"])

        expected_levels = {'0', '1', '2', '3', '4', '5', '6'}
        if all_levels_found and not all_levels_found.issuperset(expected_levels):
            recommendations.append({
                "priority": "MEDIUM",
                "issue": f"Not all maturity levels covered. Found: {sorted(all_levels_found)}",
                "action": "Ensure authors document evidence for all maturity levels (0-6)"
            })

        # Check category coverage
        if len(self.analysis_results["evidence_categories"]) < 4:
            recommendations.append({
                "priority": "MEDIUM",
                "issue": f"Only {len(self.analysis_results['evidence_categories'])} evidence categories used",
                "action": "Encourage use of all 4 categories: Artefatos, Métricas, Comportamentos, Perguntas"
            })

        self.analysis_results["recommendations"] = recommendations

    def print_summary(self):
        """Print a formatted summary of the analysis."""
        print("\n" + "="*80)
        print("📊 EVIDENCE FORMAT ANALYSIS SUMMARY")
        print("="*80 + "\n")

        # Files analyzed
        total_files = len(self.analysis_results["files_analyzed"])
        print(f"📁 Total files analyzed: {total_files}\n")

        # Authors
        print("👥 Authors found:")
        for author, info in self.analysis_results["authors"].items():
            print(f"  • {author}: {len(info['files'])} file(s)")
        print()

        # Formatting types
        print("📋 Formatting styles:")
        for style, files in self.analysis_results["formatting_styles"].items():
            percentage = (len(files) / total_files * 100) if total_files > 0 else 0
            print(f"  • {style.capitalize()}: {len(files)} files ({percentage:.1f}%)")
            if len(files) <= 5:
                for f in files:
                    print(f"    - {f}")
        print()

        # Level patterns
        print("🔢 Level marker formats:")
        for pattern, count in self.analysis_results["level_patterns"].items():
            print(f"  • {pattern}: {count} file(s)")
        print()

        # Evidence categories
        print("📦 Evidence categories usage:")
        for category, files in self.analysis_results["evidence_categories"].items():
            print(f"  • {category.capitalize()}: {len(files)} file(s)")
        print()

        # Quality issues
        if self.analysis_results["quality_issues"]:
            print(f"⚠️  Quality issues found: {len(self.analysis_results['quality_issues'])}")
            for issue in self.analysis_results["quality_issues"][:10]:
                print(f"  • {issue['file']}: {issue['issue']}")
            if len(self.analysis_results["quality_issues"]) > 10:
                print(f"  ... and {len(self.analysis_results['quality_issues']) - 10} more")
            print()

        # Recommendations
        if self.analysis_results["recommendations"]:
            print("💡 RECOMMENDATIONS:")
            for i, rec in enumerate(self.analysis_results["recommendations"], 1):
                print(f"\n  {i}. [{rec['priority']}] {rec['issue']}")
                print(f"     → Action: {rec['action']}")

        print("\n" + "="*80)

    def save_detailed_report(self, output_path: str):
        """Save detailed analysis report to JSON file."""
        # Convert sets to lists for JSON serialization
        serializable_results = {
            "files_analyzed": self.analysis_results["files_analyzed"],
            "authors": self.analysis_results["authors"],
            "section_patterns": dict(self.analysis_results["section_patterns"]),
            "evidence_categories": {
                k: list(v) for k, v in self.analysis_results["evidence_categories"].items()
            },
            "formatting_styles": dict(self.analysis_results["formatting_styles"]),
            "level_patterns": dict(self.analysis_results["level_patterns"]),
            "quality_issues": self.analysis_results["quality_issues"],
            "recommendations": self.analysis_results["recommendations"]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Detailed report saved to: {output_path}")

    def print_sample_evidence(self, num_samples: int = 3):
        """Print sample evidence texts from different formatting types."""
        print("\n" + "="*80)
        print("📝 SAMPLE EVIDENCE TEXTS")
        print("="*80 + "\n")

        samples_by_type = defaultdict(list)

        for file_info in self.analysis_results["files_analyzed"]:
            if "evidence_structure" in file_info and file_info.get("text_sample"):
                fmt_type = file_info["evidence_structure"].get("formatting_type", "unknown")
                if len(samples_by_type[fmt_type]) < num_samples:
                    samples_by_type[fmt_type].append({
                        "file": file_info["filename"],
                        "sample": file_info["text_sample"]
                    })

        for fmt_type, samples in samples_by_type.items():
            print(f"\n{'─'*80}")
            print(f"Format Type: {fmt_type.upper()}")
            print(f"{'─'*80}\n")

            for i, sample in enumerate(samples, 1):
                print(f"Example {i}: {sample['file']}")
                print("-" * 40)
                print(sample['sample'])
                print("\n")


def main():
    """Main execution function."""
    # Always define script_dir for later use
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent

    # Check for command line argument first
    if len(sys.argv) > 1:
        docx_dir = Path(sys.argv[1])
        if not docx_dir.exists():
            print(f"❌ Error: Directory not found: {docx_dir}")
            sys.exit(1)
    else:
        # Auto-detect DOCX directory

        # Look for DOCX files in common locations (including subdirectories)
        possible_paths = [
            project_root / "question-base" / "docs_by_author",
            project_root / "question-base" / "docx",
            project_root / "question-base" / "documents",
            project_root / "docx",
            project_root / "documents"
        ]

        docx_dir = None
        for path in possible_paths:
            if path.exists():
                # Check for DOCX files in directory or subdirectories
                if any(path.glob("*.docx")) or any(path.glob("**/*.docx")):
                    docx_dir = path
                    break

        if not docx_dir:
            print("❌ Error: Could not find DOCX directory")
            print("\nSearched locations:")
            for path in possible_paths:
                print(f"  • {path}")
            print("\nPlease specify the DOCX directory as an argument:")
            print(f"  python {Path(__file__).name} <docx_directory>")
            sys.exit(1)

    # Run analysis
    analyzer = EvidenceFormatAnalyzer(docx_dir)

    # Analyze up to 10 files by default (can be changed)
    limit = 10
    if len(sys.argv) > 2:
        try:
            limit = int(sys.argv[2])
        except ValueError:
            print("⚠️  Warning: Invalid limit, using default of 10")

    results = analyzer.analyze_all_documents(limit=limit)

    # Print summary
    analyzer.print_summary()

    # Print sample evidence texts
    analyzer.print_sample_evidence(num_samples=2)

    # Save detailed report
    report_path = script_dir / "evidence_analysis_report.json"
    analyzer.save_detailed_report(str(report_path))

    print("\n✅ Analysis complete!")
    print(f"\nNext steps:")
    print(f"  1. Review the detailed report: {report_path}")
    print(f"  2. Check sample evidence texts above to understand format variations")
    print(f"  3. Implement recommendations to improve extraction accuracy")
    print(f"  4. Update extract_evidence.py to handle identified patterns")


if __name__ == "__main__":
    main()
