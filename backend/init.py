"""
Backend Package
File: backend/__init__.py
Description: Initialize backend module and expose main classes
"""

from .ollama_client import OllamaClient
from .pdf_extractor import PDFTextExtractor
from .summarizer import AISummarizer
from .exporter import SummaryExporter
from .utils import (
    calculate_statistics,
    validate_text_length,
    estimate_processing_time,
    clean_text,
    split_into_chunks,
    format_time,
    get_file_size_mb,
    truncate_filename,
    count_sentences,
    get_reading_time,
    extract_key_stats
)

__all__ = [
    'OllamaClient',
    'PDFTextExtractor',
    'AISummarizer',
    'SummaryExporter',
    'calculate_statistics',
    'validate_text_length',
    'estimate_processing_time',
    'clean_text',
    'split_into_chunks',
    'format_time',
    'get_file_size_mb',
    'truncate_filename',
    'count_sentences',
    'get_reading_time',
    'extract_key_stats'
]

__version__ = '1.0.0'
__author__ = 'Academic Project'
__description__ = 'Backend module for AI-powered PDF summarization'
