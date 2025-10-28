"""
Coin Grade Validation and Normalization Utilities

Provides classes and functions for validating and normalizing coin grades
according to the unified external metadata standard.

Usage:
    from scripts.utils.grade_validator import GradeValidator, GradeNormalizer

    # Normalize grade
    normalizer = GradeNormalizer()
    canonical = normalizer.normalize('MS65')  # Returns 'MS-65'

    # Validate grade
    validator = GradeValidator()
    is_valid, message = validator.validate_canonical('MS-65')
"""

import json
import re
from pathlib import Path
from typing import Tuple, Dict, List, Optional


class GradeNormalizer:
    """
    Normalizes grade strings to canonical format (MS-65).

    Accepts variations like MS65, MS 65, ms-65 and normalizes to MS-65.
    """

    @staticmethod
    def normalize(input_grade: str) -> str:
        """
        Normalize any grade format to canonical format.

        Args:
            input_grade: Grade in any format (MS65, MS 65, ms-65, etc.)

        Returns:
            Canonical format grade (MS-65)

        Raises:
            ValueError: If input is invalid

        Examples:
            >>> GradeNormalizer.normalize('MS65')
            'MS-65'
            >>> GradeNormalizer.normalize('MS 65')
            'MS-65'
            >>> GradeNormalizer.normalize('ms-65')
            'MS-65'
        """
        if not input_grade or not isinstance(input_grade, str):
            raise ValueError("Grade must be a non-empty string")

        input_clean = input_grade.strip().upper()

        # Extract abbreviation and number
        match = re.match(r'^([A-Z]{1,2})[\s-]?(\d{1,2})$', input_clean)
        if not match:
            raise ValueError(
                f"Invalid grade format: '{input_grade}'. "
                f"Expected format like 'MS-65', 'PR-69', 'AU-58'"
            )

        abbr, num = match.groups()

        # Validate abbreviation
        valid_abbrs = ['P', 'FR', 'AG', 'G', 'VG', 'F', 'VF', 'XF', 'EF', 'AU', 'MS', 'PR', 'PF', 'SP']
        if abbr not in valid_abbrs:
            raise ValueError(
                f"Unknown grade abbreviation: '{abbr}'. "
                f"Valid abbreviations: {', '.join(valid_abbrs)}"
            )

        # Return canonical format
        return f"{abbr}-{num}"

    @staticmethod
    def normalize_full_string(input_str: str) -> str:
        """
        Normalize full grade string with service and modifiers.

        Accepts variations and normalizes to canonical format.

        Args:
            input_str: Full grade string (e.g., "PCGS MS65 RD", "pcgs ms-65rd")

        Returns:
            Normalized full grade string (e.g., "PCGS MS-65 RD")

        Examples:
            >>> GradeNormalizer.normalize_full_string('PCGS MS65 RD')
            'PCGS MS-65 RD'
            >>> GradeNormalizer.normalize_full_string('pcgs ms-65rd')
            'PCGS MS-65 RD'
        """
        if not input_str or not isinstance(input_str, str):
            raise ValueError("Grade string must be non-empty")

        # Clean and split
        parts = input_str.strip().upper().replace('  ', ' ').split()

        normalized = []
        i = 0
        while i < len(parts):
            part = parts[i]

            # Check if this looks like a grade (contains digit)
            if re.search(r'\d', part):
                # Try to extract grade and any attached modifiers
                grade_match = re.match(r'^([A-Z]{1,2})[\s-]?(\d{1,2})([A-Z]+)?$', part)
                if grade_match:
                    abbr, num, modifier = grade_match.groups()
                    normalized.append(f"{abbr}-{num}")
                    if modifier:
                        # Split concatenated modifiers if possible
                        # e.g., "FBRD" -> "FB RD"
                        known_mods = ['CAM', 'DCAM', 'UCAM', 'UC', 'FB', 'FBL', 'FH', 'FS', 'RD', 'RB', 'BN', 'PL', 'DPL', 'DMPL']
                        remaining = modifier
                        while remaining:
                            found = False
                            for mod in known_mods:
                                if remaining.startswith(mod):
                                    normalized.append(mod)
                                    remaining = remaining[len(mod):]
                                    found = True
                                    break
                            if not found:
                                # Couldn't parse, just add it
                                normalized.append(remaining)
                                break
                else:
                    normalized.append(part)
            else:
                normalized.append(part)

            i += 1

        return ' '.join(normalized)


class GradeValidator:
    """
    Validates coin grades against unified standard.

    Loads reference data from grades_unified.json and provides
    validation methods for grade strings and metadata.
    """

    def __init__(self, grades_file: Optional[str] = None):
        """
        Initialize validator with grades reference file.

        Args:
            grades_file: Path to grades_unified.json. If None, uses default location.
        """
        if grades_file is None:
            # Default to project root / data/references/grades_unified.json
            project_root = Path(__file__).parent.parent.parent
            grades_file = project_root / 'data' / 'references' / 'grades_unified.json'

        self.grades_file = Path(grades_file)
        if not self.grades_file.exists():
            raise FileNotFoundError(f"Grades file not found: {self.grades_file}")

        # Load grades reference data
        with open(self.grades_file, 'r') as f:
            data = json.load(f)

        self.grades_data = data
        self.valid_grades = {g['abbreviation']: g for g in data['grades']}
        self.canonical_pattern = re.compile(data.get('canonical_format_pattern', r'^[A-Z]{1,2}-\d{1,2}$'))

    def validate_canonical(self, grade_str: str) -> Tuple[bool, str]:
        """
        Validate grade string matches canonical format.

        Args:
            grade_str: Grade string to validate (e.g., 'MS-65')

        Returns:
            Tuple of (is_valid, message)

        Examples:
            >>> validator = GradeValidator()
            >>> validator.validate_canonical('MS-65')
            (True, 'Valid')
            >>> validator.validate_canonical('MS65')
            (False, 'Does not match canonical format')
        """
        if not grade_str or not isinstance(grade_str, str):
            return False, "Grade must be a non-empty string"

        # Check format
        if not self.canonical_pattern.match(grade_str):
            return False, f"Does not match canonical format (expected: MS-65, PR-69, etc.)"

        # Check if grade exists in reference data
        if grade_str not in self.valid_grades:
            return False, f"Unknown grade: '{grade_str}'"

        return True, "Valid"

    def validate_numeric(self, numeric_value: int) -> Tuple[bool, str]:
        """
        Validate numeric grade value (1-70 on Sheldon scale).

        Args:
            numeric_value: Numeric grade value

        Returns:
            Tuple of (is_valid, message)

        Examples:
            >>> validator = GradeValidator()
            >>> validator.validate_numeric(65)
            (True, 'Valid')
            >>> validator.validate_numeric(99)
            (False, 'Numeric value must be 1-70')
        """
        if not isinstance(numeric_value, int):
            return False, "Numeric value must be an integer"

        if numeric_value < 1 or numeric_value > 70:
            return False, "Numeric value must be 1-70 (Sheldon scale)"

        return True, "Valid"

    def is_market_threshold(self, grade_str: str) -> bool:
        """
        Check if grade represents a significant market threshold.

        Market threshold grades typically see significant price increases
        (e.g., MS-63, MS-65, MS-67, PR-69, PR-70).

        Args:
            grade_str: Grade string in canonical format

        Returns:
            True if market threshold grade, False otherwise

        Examples:
            >>> validator = GradeValidator()
            >>> validator.is_market_threshold('MS-65')
            True
            >>> validator.is_market_threshold('MS-62')
            False
        """
        if grade_str in self.valid_grades:
            return self.valid_grades[grade_str].get('market_threshold', False)
        return False

    def get_grade_info(self, grade_str: str) -> Optional[Dict]:
        """
        Get full grade information from reference data.

        Args:
            grade_str: Grade string in canonical format

        Returns:
            Dictionary with grade information, or None if not found

        Examples:
            >>> validator = GradeValidator()
            >>> info = validator.get_grade_info('MS-65')
            >>> info['subcategory']
            'Gem Uncirculated'
        """
        return self.valid_grades.get(grade_str)

    def validate_modifiers(self, grade_str: str, modifiers: List[str]) -> Tuple[bool, str]:
        """
        Validate modifier compatibility with grade.

        Args:
            grade_str: Grade string in canonical format
            modifiers: List of modifier codes (e.g., ['DCAM', 'RD'])

        Returns:
            Tuple of (is_valid, message)

        Examples:
            >>> validator = GradeValidator()
            >>> validator.validate_modifiers('PR-69', ['DCAM'])
            (True, 'Valid')
            >>> validator.validate_modifiers('MS-65', ['DCAM'])
            (False, 'DCAM only applies to proof coins')
        """
        grade_info = self.get_grade_info(grade_str)
        if not grade_info:
            return False, f"Unknown grade: '{grade_str}'"

        strike_types = grade_info.get('strike_types', [])

        # Check modifier compatibility
        for modifier in modifiers:
            # CAM/DCAM only for proofs
            if modifier in ['CAM', 'DCAM', 'UCAM', 'UC']:
                if 'proof' not in strike_types and 'specimen' not in strike_types:
                    return False, f"{modifier} only applies to proof or specimen coins"

            # RD/RB/BN only for copper coins (can't check composition here, but can warn)
            if modifier in ['RD', 'RB', 'BN']:
                # This would require coin-specific validation
                pass

        # Check for mutually exclusive modifiers
        if 'CAM' in modifiers and 'DCAM' in modifiers:
            return False, "CAM and DCAM are mutually exclusive"

        if len(set(modifiers) & {'RD', 'RB', 'BN'}) > 1:
            return False, "RD, RB, and BN are mutually exclusive color designations"

        return True, "Valid"


class CertificationValidator:
    """
    Validates grading service certification numbers.
    """

    def __init__(self, services_file: Optional[str] = None):
        """
        Initialize validator with grading services reference file.

        Args:
            services_file: Path to grading_services.json. If None, uses default location.
        """
        if services_file is None:
            project_root = Path(__file__).parent.parent.parent
            services_file = project_root / 'data' / 'references' / 'grading_services.json'

        self.services_file = Path(services_file)
        if not self.services_file.exists():
            raise FileNotFoundError(f"Services file not found: {self.services_file}")

        with open(self.services_file, 'r') as f:
            data = json.load(f)

        self.services = {s['code']: s for s in data['services']}

    def validate_cert_number(self, service_code: str, cert_number: str) -> Tuple[bool, str]:
        """
        Validate certification number format for specific service.

        Args:
            service_code: Service code (PCGS, NGC, etc.)
            cert_number: Certification number

        Returns:
            Tuple of (is_valid, message)

        Examples:
            >>> validator = CertificationValidator()
            >>> validator.validate_cert_number('PCGS', '12345678')
            (True, 'Valid')
            >>> validator.validate_cert_number('PCGS', '123')
            (False, 'PCGS cert numbers must match pattern: \\d{8}')
        """
        if service_code not in self.services:
            return False, f"Unknown grading service: '{service_code}'"

        service = self.services[service_code]
        cert_format = service.get('cert_number_format')

        if not cert_format:
            return False, f"No cert format defined for {service_code}"

        pattern = cert_format.get('validation_regex') or cert_format.get('pattern')
        if not re.match(pattern, cert_number):
            return False, f"{service_code} cert numbers must match pattern: {pattern}"

        return True, "Valid"


# Convenience functions
def normalize_grade(input_grade: str) -> str:
    """Convenience function to normalize a grade string."""
    return GradeNormalizer.normalize(input_grade)


def validate_grade(grade_str: str) -> Tuple[bool, str]:
    """Convenience function to validate a grade string."""
    validator = GradeValidator()
    return validator.validate_canonical(grade_str)


if __name__ == '__main__':
    # Quick tests
    print("Testing GradeNormalizer...")
    normalizer = GradeNormalizer()

    test_cases = [
        'MS65', 'MS 65', 'ms-65', 'MS-65',
        'PR69', 'AU58', 'VF30'
    ]

    for test in test_cases:
        try:
            result = normalizer.normalize(test)
            print(f"  {test:10} -> {result}")
        except ValueError as e:
            print(f"  {test:10} -> ERROR: {e}")

    print("\nTesting GradeValidator...")
    validator = GradeValidator()

    test_grades = ['MS-65', 'PR-69', 'AU-58', 'ZZ-99']

    for grade in test_grades:
        is_valid, message = validator.validate_canonical(grade)
        status = "✓" if is_valid else "✗"
        print(f"  {status} {grade:10} - {message}")

    print("\nTesting market thresholds...")
    threshold_grades = ['MS-63', 'MS-64', 'MS-65', 'PR-69', 'PR-70']

    for grade in threshold_grades:
        is_threshold = validator.is_market_threshold(grade)
        marker = "💎" if is_threshold else "  "
        print(f"  {marker} {grade}")

    print("\nTesting CertificationValidator...")
    cert_validator = CertificationValidator()

    test_certs = [
        ('PCGS', '12345678'),
        ('PCGS', '123'),
        ('NGC', '1234567'),
        ('NGC', '123456')
    ]

    for service, cert_num in test_certs:
        is_valid, message = cert_validator.validate_cert_number(service, cert_num)
        status = "✓" if is_valid else "✗"
        print(f"  {status} {service} {cert_num:10} - {message}")
