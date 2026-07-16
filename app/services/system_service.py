# app/services/system_service.py
import psutil
import platform
import shutil
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class SystemService:
    """
    Service untuk monitoring sistem Jetson Nano
    Menggunakan psutil untuk cross-platform compatibility
    """
    
    def get_cpu_info(self) -> Dict:
        """Get CPU usage and info"""
        return {
            "usage_percent": psutil.cpu_percent(interval=1),
            "count_physical": psutil.cpu_count(logical=False),
            "count_logical": psutil.cpu_count(logical=True),
            "freq_current": psutil.cpu_freq().current if psutil.cpu_freq() else 0
        }
    
    def get_memory_info(self) -> Dict:
        """Get RAM usage info"""
        memory = psutil.virtual_memory()
        return {
            "total_mb": round(memory.total / 1024 / 1024, 2),
            "available_mb": round(memory.available / 1024 / 1024, 2),
            "used_mb": round(memory.used / 1024 / 1024, 2),
            "percent": memory.percent
        }
    
    def get_disk_info(self) -> Dict:
        """Get disk usage info"""
        disk = shutil.disk_usage("/")
        return {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": round((disk.used / disk.total) * 100, 2)
        }
    
    def get_temperature(self) -> Dict:
        """
        Get temperature info
        Untuk Jetson Nano, baca dari /sys/class/thermal/
        """
        try:
            # Coba baca dari thermal zone (Jetson Nano)
            import os
            temp_file = "/sys/class/thermal/thermal_zone0/temp"
            if os.path.exists(temp_file):
                with open(temp_file, "r") as f:
                    temp = int(f.read().strip()) / 1000.0
            else:
                # Fallback untuk development di Windows/Linux lain
                temp = 45.0  # Dummy temperature
        except Exception as e:
            logger.warning(f"Could not read temperature: {e}")
            temp = 45.0
        
        return {
            "cpu_celsius": round(temp, 2),
            "status": "NORMAL" if temp < 70 else "WARNING" if temp < 85 else "CRITICAL"
        }
    
    def get_network_info(self) -> Dict:
        """Get network interfaces info"""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent_mb": round(net_io.bytes_sent / 1024 / 1024, 2),
            "bytes_recv_mb": round(net_io.bytes_recv / 1024 / 1024, 2),
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
    
    def get_system_info(self) -> Dict:
        """Get general system info"""
        return {
            "platform": platform.system(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "hostname": platform.node()
        }
    
    def get_full_system_status(self) -> Dict:
        """Get comprehensive system status"""
        return {
            "system": self.get_system_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "temperature": self.get_temperature(),
            "network": self.get_network_info()
        }

# Singleton instance
system_service = SystemService()