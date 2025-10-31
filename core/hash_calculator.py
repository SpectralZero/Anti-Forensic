"""
hash_calculator.py
MULTI-ALGORITHM HASH GENERATOR 
Comprehensive cryptographic hash calculation for forensic analysis
"""

import hashlib
import os
import threading
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Callable
import mmap

class HashCalculator:
    """Calculate multiple hash algorithms simultaneously"""
    
    SUPPORTED_ALGORITHMS = {
        'MD5': hashlib.md5,
        'SHA-1': hashlib.sha1,
        'SHA-256': hashlib.sha256,
        'SHA-512': hashlib.sha512,
        'SHA3-256': hashlib.sha3_256,
        'SHA3-512': hashlib.sha3_512,
        'BLAKE2b': hashlib.blake2b,
        'BLAKE2s': hashlib.blake2s,
    }
    
    @classmethod
    def calculate_file_hashes(
        cls,
        file_path: str | Path,
        algorithms: List[str] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Dict[str, str]:
        """
        Calculate multiple hashes for a file with progress tracking
        """
        if algorithms is None:
            algorithms = list(cls.SUPPORTED_ALGORITHMS.keys())
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Initialize hashers
        hashers = {}
        for algo in algorithms:
            if algo in cls.SUPPORTED_ALGORITHMS:
                hashers[algo] = cls.SUPPORTED_ALGORITHMS[algo]()
        
        file_size = file_path.stat().st_size
        bytes_processed = 0
        
        # Use memory mapping for efficient large file reading
        with open(file_path, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                chunk_size = 8192  # 8KB chunks
                
                while True:
                    chunk = mm.read(chunk_size)
                    if not chunk:
                        break
                    
                    # Update all hashers
                    for hasher in hashers.values():
                        hasher.update(chunk)
                    
                    bytes_processed += len(chunk)
                    if progress_callback:
                        progress_callback(bytes_processed, file_size)
        
        # Return results
        results = {}
        for algo, hasher in hashers.items():
            results[algo] = hasher.hexdigest()
        
        return results
    
    @classmethod
    def calculate_text_hashes(cls, text: str, algorithms: List[str] = None) -> Dict[str, str]:
        """Calculate hashes for text input"""
        if algorithms is None:
            algorithms = list(cls.SUPPORTED_ALGORITHMS.keys())
        
        text_bytes = text.encode('utf-8')
        results = {}
        
        for algo in algorithms:
            if algo in cls.SUPPORTED_ALGORITHMS:
                hasher = cls.SUPPORTED_ALGORITHMS[algo]()
                hasher.update(text_bytes)
                results[algo] = hasher.hexdigest()
        
        return results
    
    @classmethod
    def verify_file_integrity(
        cls,
        file_path: str | Path,
        expected_hashes: Dict[str, str],
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Dict[str, bool]:
        """
        Verify file against expected hashes
        Returns dict with algorithm: is_correct
        """
        calculated = cls.calculate_file_hashes(
            file_path, 
            list(expected_hashes.keys()),
            progress_callback
        )
        
        results = {}
        for algo, expected_hash in expected_hashes.items():
            results[algo] = (calculated.get(algo, "").lower() == expected_hash.lower())
        
        return results

class HashBenchmark:
    """Performance benchmarking for hash algorithms"""
    
    @staticmethod
    def benchmark_algorithms(
        test_data: bytes,
        algorithms: List[str] = None
    ) -> Dict[str, float]:
        """
        Benchmark hash algorithm speed
        Returns algorithm -> MB/s
        """
        if algorithms is None:
            algorithms = list(HashCalculator.SUPPORTED_ALGORITHMS.keys())
        
        import time
        results = {}
        data_size_mb = len(test_data) / (1024 * 1024)
        
        for algo_name in algorithms:
            if algo_name not in HashCalculator.SUPPORTED_ALGORITHMS:
                continue
            
            hasher_class = HashCalculator.SUPPORTED_ALGORITHMS[algo_name]
            
            # Warmup
            for _ in range(10):
                hasher = hasher_class()
                hasher.update(test_data)
                hasher.hexdigest()
            
            # Benchmark
            start_time = time.time()
            iterations = 100
            
            for _ in range(iterations):
                hasher = hasher_class()
                hasher.update(test_data)
                hasher.hexdigest()
            
            end_time = time.time()
            total_data_mb = data_size_mb * iterations
            mb_per_second = total_data_mb / (end_time - start_time)
            
            results[algo_name] = mb_per_second
        
        return results