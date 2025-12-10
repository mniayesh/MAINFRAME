"""
Layer 1: Hardware Bridge
======================

Fixed platform layer that knows how to talk to this specific hardware box optimally.
This is the ONLY layer that touches raw hardware. Everything above depends on these functions.

For a new platform: implement this layer once, then everything above it is identical.
"""

import ctypes
import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple, Dict, Optional, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# Device Capability Detection
# ============================================================================

class DeviceCapability:
    """Auto-detect hardware capabilities."""

    def __init__(self):
        self.cpu_cores = self._detect_cpu_cores()
        self.ram_bytes = self._detect_ram()
        self.has_gpu = self._detect_gpu()
        self.has_npu = self._detect_npu()
        self.gpu_vram_bytes = self._detect_gpu_vram() if self.has_gpu else 0

    @staticmethod
    def _detect_cpu_cores() -> int:
        """Detect number of CPU cores."""
        import os
        return os.cpu_count() or 1

    @staticmethod
    def _detect_ram() -> int:
        """Detect available RAM."""
        try:
            import psutil
            return psutil.virtual_memory().total
        except:
            return 8 * (1024 ** 3)  # Fallback: assume 8 GB

    @staticmethod
    def _detect_gpu() -> bool:
        """Check if GPU is available."""
        try:
            import cupy
            return True
        except:
            return False

    @staticmethod
    def _detect_npu() -> bool:
        """Check if NPU/TPU is available."""
        try:
            import jax
            return True
        except:
            return False

    @staticmethod
    def _detect_gpu_vram() -> int:
        """Detect GPU VRAM."""
        try:
            import pynvml
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            return info.total
        except:
            return 8 * (1024 ** 3)  # Fallback: assume 8 GB


# ============================================================================
# Memory Management
# ============================================================================

@dataclass
class MemoryBlock:
    """Track an allocated memory block."""
    ptr: int
    size: int
    device: str  # 'cpu', 'gpu', 'npu'
    is_free: bool = False


class MemoryManager:
    """CPU and GPU memory allocation/deallocation."""

    def __init__(self, device: str = 'cpu'):
        self.device = device
        self.blocks: Dict[int, MemoryBlock] = {}
        self.next_ptr = 0x10000000  # Start high in virtual address space

    def allocate(self, size: int) -> int:
        """Allocate size bytes, return pointer."""
        if self.device == 'cpu':
            ptr = self.next_ptr
            self.next_ptr += ((size + 4095) // 4096) * 4096  # Page align

            block = MemoryBlock(ptr=ptr, size=size, device='cpu')
            self.blocks[ptr] = block

            # In real implementation, mmap or malloc here
            logger.debug(f"Allocated {size} bytes at {hex(ptr)} on CPU")
            return ptr

        elif self.device == 'gpu':
            try:
                import cupy as cp
                gpu_mem = cp.cuda.alloc(size)
                ptr = gpu_mem.ptr
                block = MemoryBlock(ptr=ptr, size=size, device='gpu')
                self.blocks[ptr] = block
                logger.debug(f"Allocated {size} bytes at {hex(ptr)} on GPU")
                return ptr
            except Exception as e:
                logger.error(f"GPU allocation failed: {e}")
                raise

    def free(self, ptr: int) -> None:
        """Release allocated memory."""
        if ptr not in self.blocks:
            logger.warning(f"Freeing unknown pointer {hex(ptr)}")
            return

        block = self.blocks[ptr]
        if self.device == 'gpu':
            try:
                import cupy as cp
                mem = cp.cuda.MemoryPointer(cp.cuda.Context.get_current(), ptr, block.size)
                mem.free()
            except:
                pass

        block.is_free = True
        logger.debug(f"Freed {block.size} bytes at {hex(ptr)}")

    def get_block(self, ptr: int) -> Optional[MemoryBlock]:
        """Get metadata for a block."""
        return self.blocks.get(ptr)


# ============================================================================
# Layer 1 API: Hardware Bridge
# ============================================================================

class HardwareBridge(ABC):
    """
    Base class for platform-specific hardware bridge.
    Implement once per hardware platform, then swap and go.
    """

    def __init__(self):
        self.capabilities = DeviceCapability()
        self.cpu_mem = MemoryManager('cpu')
        self.gpu_mem = MemoryManager('gpu') if self.capabilities.has_gpu else None
        logger.info(f"Hardware Bridge initialized: {self.capabilities.cpu_cores} CPU cores, "
                   f"{self.capabilities.ram_bytes / (1024**3):.1f} GB RAM, "
                   f"GPU: {self.capabilities.has_gpu}")

    # ========== CPU Execution ==========

    def cpu_exec(self, code_ptr: int, arg_ptr: int) -> int:
        """
        Execute machine code at code_ptr with arguments at arg_ptr.
        Returns result in processor register.

        This is where machine code JIT'd from Layer 2 gets executed.
        """
        raise NotImplementedError("Implement in platform-specific subclass")

    # ========== Memory Operations ==========

    def mem_alloc(self, size: int) -> int:
        """Allocate size bytes on CPU, return pointer."""
        return self.cpu_mem.allocate(size)

    def mem_free(self, ptr: int) -> None:
        """Release memory."""
        self.cpu_mem.free(ptr)

    def mem_read(self, ptr: int, length: int) -> bytes:
        """Read length bytes from ptr."""
        block = self.cpu_mem.get_block(ptr)
        if not block:
            raise ValueError(f"Unknown memory block at {hex(ptr)}")

        if length > block.size:
            raise ValueError(f"Read size {length} exceeds block size {block.size}")

        # In real implementation, memcpy or ctypes here
        logger.debug(f"Read {length} bytes from {hex(ptr)}")
        return bytes(length)  # Placeholder

    def mem_write(self, ptr: int, data: bytes) -> None:
        """Write data to ptr."""
        block = self.cpu_mem.get_block(ptr)
        if not block:
            raise ValueError(f"Unknown memory block at {hex(ptr)}")

        if len(data) > block.size:
            raise ValueError(f"Write size {len(data)} exceeds block size {block.size}")

        logger.debug(f"Wrote {len(data)} bytes to {hex(ptr)}")

    # ========== GPU Operations ==========

    def gpu_alloc(self, size: int) -> int:
        """Allocate GPU memory."""
        if not self.capabilities.has_gpu:
            raise RuntimeError("GPU not available")
        return self.gpu_mem.allocate(size)

    def gpu_free(self, ptr: int) -> None:
        """Free GPU memory."""
        if not self.capabilities.has_gpu:
            raise RuntimeError("GPU not available")
        self.gpu_mem.free(ptr)

    def gpu_read(self, gpu_ptr: int, length: int) -> bytes:
        """Copy from GPU to CPU."""
        if not self.capabilities.has_gpu:
            raise RuntimeError("GPU not available")

        logger.debug(f"GPU→CPU transfer: {length} bytes from {hex(gpu_ptr)}")

        try:
            import cupy as cp
            gpu_mem = cp.asarray(gpu_ptr)  # Placeholder
            return gpu_mem.get().tobytes()
        except Exception as e:
            logger.error(f"GPU read failed: {e}")
            raise

    def gpu_write(self, gpu_ptr: int, data: bytes) -> None:
        """Copy from CPU to GPU."""
        if not self.capabilities.has_gpu:
            raise RuntimeError("GPU not available")

        logger.debug(f"CPU→GPU transfer: {len(data)} bytes to {hex(gpu_ptr)}")

        try:
            import cupy as cp
            cp.copyto(cp.asarray(gpu_ptr), cp.asarray(np.frombuffer(data, dtype=np.uint8)))
        except Exception as e:
            logger.error(f"GPU write failed: {e}")
            raise

    def gpu_run(self, kernel_id: int, buffers: List[int], params: Dict) -> None:
        """
        Execute GPU kernel.
        kernel_id: identifier of kernel to run
        buffers: list of GPU memory pointers
        params: scalar parameters (learning rates, thresholds, etc.)
        """
        if not self.capabilities.has_gpu:
            raise RuntimeError("GPU not available")

        logger.debug(f"GPU kernel {kernel_id} executed on {len(buffers)} buffers")

    # ========== NPU Operations ==========

    def npu_run(self, graph_id: int, tensors: List[int]) -> None:
        """Execute NPU inference graph."""
        if not self.capabilities.has_npu:
            logger.warning("NPU not available, falling back to CPU")
            return

        logger.debug(f"NPU graph {graph_id} executed on {len(tensors)} tensors")

    # ========== Disk I/O ==========

    def disk_read(self, lba: int, count: int, dst_ptr: int) -> None:
        """
        Read count sectors from LBA into memory at dst_ptr.
        (LBA = logical block address, typically 512 bytes/sector)
        """
        sector_size = 512
        total_bytes = count * sector_size

        logger.debug(f"Disk read: LBA {lba}, {count} sectors → {hex(dst_ptr)}")

        # In real implementation, use os.read or async I/O

    def disk_write(self, lba: int, count: int, src_ptr: int) -> None:
        """Write count sectors from src_ptr to LBA."""
        sector_size = 512
        total_bytes = count * sector_size

        logger.debug(f"Disk write: LBA {lba}, {count} sectors ← {hex(src_ptr)}")

    # ========== Timing ==========

    def get_timestamp(self) -> int:
        """Return nanoseconds since boot."""
        import time
        return int(time.time_ns())

    def sleep_ns(self, ns: int) -> None:
        """Sleep for at least ns nanoseconds."""
        import time
        time.sleep(ns / 1e9)

    # ========== Sensor I/O (if robot) ==========

    def read_sensor(self, sensor_id: int) -> bytes:
        """Read sensor data."""
        logger.debug(f"Read sensor {sensor_id}")
        return bytes(64)  # Placeholder: 64 bytes of sensor data

    def write_actuator(self, actuator_id: int, command: bytes) -> None:
        """Send command to actuator."""
        logger.debug(f"Write actuator {actuator_id}: {len(command)} bytes")

    # ========== Utility ==========

    def get_capabilities_summary(self) -> str:
        """Return human-readable hardware description."""
        return (
            f"CPU: {self.capabilities.cpu_cores} cores\n"
            f"RAM: {self.capabilities.ram_bytes / (1024**3):.1f} GB\n"
            f"GPU: {self.capabilities.has_gpu}\n"
            f"GPU VRAM: {self.capabilities.gpu_vram_bytes / (1024**3):.1f} GB\n"
            f"NPU: {self.capabilities.has_npu}"
        )


# ============================================================================
# Platform-Specific Implementations
# ============================================================================

class CPUOnlyBridge(HardwareBridge):
    """Implementation for CPU-only systems."""

    def __init__(self):
        super().__init__()
        logger.info("Using CPU-only bridge (no GPU/NPU)")

    def cpu_exec(self, code_ptr: int, arg_ptr: int) -> int:
        """Execute CPU code using ctypes or direct interpreter."""
        # Placeholder: would use ctypes.CFUNCTYPE or similar
        logger.debug(f"CPU exec at {hex(code_ptr)}")
        return 0


class GPUAwareBridge(HardwareBridge):
    """Implementation for systems with GPU."""

    def __init__(self):
        super().__init__()
        if self.capabilities.has_gpu:
            logger.info("GPU detected and initialized")

    def cpu_exec(self, code_ptr: int, arg_ptr: int) -> int:
        logger.debug(f"CPU exec at {hex(code_ptr)}")
        return 0


# ============================================================================
# Factory
# ============================================================================

def get_hardware_bridge() -> HardwareBridge:
    """Auto-detect hardware and return appropriate bridge."""
    capabilities = DeviceCapability()

    if capabilities.has_gpu:
        return GPUAwareBridge()
    else:
        return CPUOnlyBridge()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Example: instantiate bridge
    bridge = get_hardware_bridge()
    print(bridge.get_capabilities_summary())

    # Example: allocate memory
    ptr = bridge.mem_alloc(1024)
    print(f"Allocated 1024 bytes at {hex(ptr)}")

    bridge.mem_free(ptr)
    print(f"Freed memory at {hex(ptr)}")
