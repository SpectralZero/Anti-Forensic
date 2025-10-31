"""
 SYSTEM INFORMATION - Digital Forensics & Red Team Intelligence
ENHANCED VERSION - Advanced System Intelligence & Network Forensics
"""

import os
import platform
import logging
import time
import shutil
import socket
import getpass
import json
import hashlib
import uuid
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field

try:
    import psutil
    import requests
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️  Install required packages: pip install psutil requests")

LOG = logging.getLogger("system_info")

# Configuration
TIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
PUBLIC_IP_SERVICES = [
    "https://api.ipify.org?format=json",
    "https://ifconfig.me/ip",
    "https://ident.me",
]
GEO_IP_SERVICE = "https://ipinfo.io/{ip}/json"

class SystemInfo:
    """
    COMPATIBILITY WRAPPER - Maintains original interface while using enhanced capabilities
    This ensures main_window.py continues to work without changes
    """
    
    @staticmethod
    def get_forensic_info() -> dict:
        """Original interface method - returns data in expected format"""
        try:
            # Get enhanced data
            enhanced_info = AvancedSystemInfo.get_forensic_info()
            
            # Convert to legacy format for compatibility
            legacy_info = SystemInfo._convert_to_legacy_format(enhanced_info)
            return legacy_info
            
        except Exception as e:
            LOG.error(f"Compatible forensic info collection failed: {e}")
            return {"error": f"System information collection failed: {e}"}
    
    @staticmethod
    def _convert_to_legacy_format(enhanced_info: dict) -> dict:
        """Convert enhanced data structure to legacy format expected by main_window.py"""
        
        # Extract basic info from enhanced structure
        sys_intel = enhanced_info.get('system_intelligence', {})
        ident = sys_intel.get('identification', {})
        platform_info = sys_intel.get('platform_details', {})
        env = sys_intel.get('environment', {})
        
        # Build legacy basic_info
        basic_info = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "machine_name": ident.get('machine_name', platform.node()),
            "fqdn": ident.get('fqdn', socket.getfqdn()),
            "current_user": ident.get('current_user', getpass.getuser()),
            "user_domain": ident.get('user_domain', os.environ.get('USERDOMAIN', 'N/A')),
            "logon_server": ident.get('logon_server', os.environ.get('LOGONSERVER', 'N/A')),
            "platform": platform_info.get('platform', platform.platform()),
            "system": platform_info.get('system', platform.system()),
            "release": platform_info.get('release', platform.release()),
            "version": platform_info.get('version', platform.version()),
            "architecture": platform_info.get('architecture', platform.architecture()[0]),
            "processor": platform_info.get('processor', platform.processor()),
            "python_version": env.get('python_version', platform.python_version()),
            "admin_privileges": env.get('admin_privileges', SystemInfo._has_admin_privileges()),
            "system_uptime": env.get('system_uptime', 'Unable to determine'),
            "boot_time": env.get('boot_time', 'Unable to determine'),
        }
        
        # Build legacy hardware_info
        hw_forensics = enhanced_info.get('hardware_forensics', {})
        cpu_forensics = hw_forensics.get('cpu_forensics', {})
        memory_forensics = hw_forensics.get('memory_forensics', {})
        storage_forensics = hw_forensics.get('storage_forensics', {})
        
        hardware_info = {
            "cpu": {
                "physical_cores": cpu_forensics.get('physical_cores', 'N/A'),
                "logical_cores": cpu_forensics.get('logical_cores', 'N/A'),
                "cpu_usage": cpu_forensics.get('current_usage', 'N/A'),
                "cpu_frequency": cpu_forensics.get('current_frequency', 'N/A')
            },
            "memory": {
                "total_ram": memory_forensics.get('total', 'N/A'),
                "available_ram": memory_forensics.get('available', 'N/A'),
                "used_ram": memory_forensics.get('used', 'N/A'),
                "ram_usage": memory_forensics.get('usage_percent', 'N/A')
            },
            "disks": SystemInfo._convert_disks_to_legacy(storage_forensics.get('partitions', [])),
            "hardware_details": {"message": "Enhanced hardware data available"}
        }
        
        # Build legacy network_info
        net_intel = enhanced_info.get('network_intelligence', {})
        public_net = net_intel.get('public_network', {})
        local_net = net_intel.get('local_network', {})
        dns_info = net_intel.get('dns_info', {})
        
        network_info = {
            "hostname": dns_info.get('hostname', socket.gethostname()),
            "fqdn": dns_info.get('fqdn', socket.getfqdn()),
            "public_ip": public_net.get('public_ip', 'Unable to determine'),
            "dns_servers": dns_info.get('dns_servers', []),
            "interfaces": SystemInfo._convert_interfaces_to_legacy(net_intel.get('network_interfaces', {}))
        }
        
        # Build legacy user_activity
        user_forensics = enhanced_info.get('user_forensics', {})
        user_activity = {
            "current_users": user_forensics.get('user_sessions', []),
            "recent_files": SystemInfo._get_legacy_recent_files(),
            "user_folders": SystemInfo._get_user_folders(),
            "environment_variables": user_forensics.get('user_environment', {}).get('environment_variables', {})
        }
        
        # Build legacy system_forensics
        system_artifacts = enhanced_info.get('system_artifacts', {})
        system_forensics = {
            "log_files": system_artifacts.get('system_logs', []),
            "event_logs": system_artifacts.get('event_logs', []),
            "security_products": AvancedSystemInfo._get_security_products()
        }
        
        # Build legacy security_status
        security_posture = enhanced_info.get('security_posture', {})
        security_status = {
            "firewall_status": str(security_posture.get('firewall_status', {})),
            "uac_status": str(security_posture.get('uac_status', {}))
        }
        
        # Build other legacy sections
        process_forensics = enhanced_info.get('process_forensics', {})
        software_inventory = enhanced_info.get('software_inventory', {})
        browser_forensics_data = enhanced_info.get('browser_forensics', {})
        connections_data = net_intel.get('connections', {})
        
        return {
            "basic_info": basic_info,
            "hardware_info": hardware_info,
            "network_info": network_info,
            "user_activity": user_activity,
            "system_forensics": system_forensics,
            "security_status": security_status,
            "running_processes": process_forensics.get('process_list', []),
            "installed_software": software_inventory.get('installed_programs', []),
            "browser_forensics": browser_forensics_data.get('detected_browsers', {}),
            "network_connections": SystemInfo._convert_connections_to_legacy(connections_data),
            "collection_timestamp": datetime.now().isoformat(),
        }
    
    @staticmethod
    def _convert_disks_to_legacy(partitions: list) -> list:
        """Convert enhanced disk format to legacy format"""
        legacy_disks = []
        for partition in partitions:
            legacy_disks.append({
                "device": partition.get('device', 'N/A'),
                "mountpoint": partition.get('mountpoint', 'N/A'),
                "fstype": partition.get('fstype', 'N/A'),
                "total_size": partition.get('total_size', 'N/A'),
                "used": partition.get('used', 'N/A'),
                "free": partition.get('free', 'N/A'),
                "usage_percent": partition.get('usage_percent', 'N/A'),
            })
        return legacy_disks
    
    @staticmethod
    def _convert_interfaces_to_legacy(interfaces: dict) -> list:
        """Convert enhanced interface format to legacy format"""
        legacy_interfaces = []
        for name, info in interfaces.items():
            legacy_interfaces.append({
                "interface": name,
                "is_up": info.get('is_up', False),
                "speed": info.get('speed', 'Unknown'),
                "addresses": info.get('addresses', [])
            })
        return legacy_interfaces
    
    @staticmethod
    def _convert_connections_to_legacy(connections: dict) -> list:
        """Convert enhanced connections to legacy format"""
        legacy_connections = []
        
        # Add TCP connections
        for conn in connections.get('tcp_connections', []):
            legacy_connections.append({
                "local_address": conn.get('local_address', 'N/A'),
                "remote_address": conn.get('remote_address', 'N/A'),
                "status": conn.get('status', 'N/A'),
                "pid": conn.get('pid', 'N/A'),
                "family": conn.get('family', 'N/A')
            })
        
        # Add UDP connections
        for conn in connections.get('udp_connections', []):
            legacy_connections.append({
                "local_address": conn.get('local_address', 'N/A'),
                "remote_address": conn.get('remote_address', 'N/A'),
                "status": 'UDP',
                "pid": conn.get('pid', 'N/A'),
                "family": conn.get('family', 'N/A')
            })
        
        return legacy_connections
    
    @staticmethod
    def _get_legacy_recent_files() -> list:
        """Get recent files in legacy format"""
        try:
            recent_files = []
            recent_dir = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Recent"
            
            if recent_dir.exists():
                for file in recent_dir.glob("*.lnk"):
                    try:
                        recent_files.append({
                            "filename": file.name,
                            "path": str(file),
                            "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                            "size": file.stat().st_size
                        })
                    except:
                        continue
            
            return recent_files[:20]
        except:
            return []
    
    @staticmethod
    def _get_user_folders() -> dict:
        """Get user folder locations with error handling"""
        try:
            folders = {}
            special_folders = {
                "Desktop": Path.home() / "Desktop",
                "Documents": Path.home() / "Documents",
                "Downloads": Path.home() / "Downloads",
                "Pictures": Path.home() / "Pictures",
                "Videos": Path.home() / "Videos",
                "Music": Path.home() / "Music",
                "AppData": Path.home() / "AppData",
                "Temp": Path.home() / "AppData" / "Local" / "Temp",
            }
            
            for name, path in special_folders.items():
                if path.exists():
                    folders[name] = str(path)
            
            return folders
        except:
            return {}
    
    @staticmethod
    def _has_admin_privileges() -> bool:
        """Check admin privileges with error handling"""
        try:
            if platform.system() == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except:
            return False

    # Keep original static methods for direct access if needed
    @staticmethod
    def _get_basic_info() -> dict:
        return SystemInfo.get_forensic_info().get('basic_info', {})
    
    @staticmethod
    def _get_hardware_info() -> dict:
        return SystemInfo.get_forensic_info().get('hardware_info', {})
    
    @staticmethod
    def _get_network_info() -> dict:
        return SystemInfo.get_forensic_info().get('network_info', {})
    
    @staticmethod
    def _get_user_activity() -> dict:
        return SystemInfo.get_forensic_info().get('user_activity', {})
    
    @staticmethod
    def _get_system_forensics() -> dict:
        return SystemInfo.get_forensic_info().get('system_forensics', {})
    
    @staticmethod
    def _get_security_status() -> dict:
        return SystemInfo.get_forensic_info().get('security_status', {})
    
    @staticmethod
    def _get_running_processes() -> list:
        return SystemInfo.get_forensic_info().get('running_processes', [])
    
    @staticmethod
    def _get_installed_software() -> list:
        return SystemInfo.get_forensic_info().get('installed_software', [])
    
    @staticmethod
    def _get_browser_forensics() -> dict:
        return SystemInfo.get_forensic_info().get('browser_forensics', {})
    
    @staticmethod
    def _get_network_connections() -> list:
        return SystemInfo.get_forensic_info().get('network_connections', [])


class AvancedSystemInfo:
    """ SYSTEM INFORMATION - Advanced Digital Forensics & Red Team Intelligence"""
    
    @staticmethod
    def get_forensic_info() -> dict:
        """Comprehensive forensic system intelligence gathering with enhanced capabilities"""
        try:
            info = {
                "collection_metadata": {
                    "timestamp_utc": datetime.utcnow().strftime(TIME_FMT),
                    "timestamp_local": datetime.now().strftime(TIME_FMT),
                    "tool_version": "2.0",
                    "collection_mode": "COMPREHENSIVE_FORENSICS"
                },
                "system_intelligence": AvancedSystemInfo._get_system_intelligence(),
                "hardware_forensics": AvancedSystemInfo._get_hardware_forensics(),
                "network_intelligence": AvancedSystemInfo._get_network_intelligence(),
                "user_forensics": AvancedSystemInfo._get_user_forensics(),
                "security_posture": AvancedSystemInfo._get_security_posture(),
                "process_forensics": AvancedSystemInfo._get_process_forensics(),
                "software_inventory": AvancedSystemInfo._get_software_inventory(),
                "browser_forensics": AvancedSystemInfo._get_browser_forensics(),
                "system_artifacts": AvancedSystemInfo._get_system_artifacts(),
                "threat_indicators": AvancedSystemInfo._get_threat_indicators(),
            }
            return info
        except Exception as e:
            LOG.error(f"collection failed: {e}")
            return {"error": f"intelligence collection failed: {e}"}
    
    @staticmethod
    def _get_system_intelligence() -> dict:
        """Advanced system identification with enhanced capabilities"""
        try:
            sys_intel = {
                "identification": {
                    "machine_name": platform.node(),
                    "fqdn": socket.getfqdn(),
                    "unique_system_id": hashlib.sha256(str(uuid.getnode()).encode()).hexdigest(),
                    "current_user": getpass.getuser(),
                    "user_domain": os.environ.get('USERDOMAIN', 'N/A'),
                    "logon_server": os.environ.get('LOGONSERVER', 'N/A'),
                },
                "platform_details": {
                    "platform": platform.platform(),
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "architecture": platform.architecture()[0],
                    "processor": platform.processor(),
                },
                "environment": {
                    "python_version": platform.python_version(),
                    "admin_privileges": AvancedSystemInfo._has_admin_privileges(),
                    "system_uptime": AvancedSystemInfo._get_enhanced_uptime(),
                    "boot_time": AvancedSystemInfo._get_enhanced_boot_time(),
                    "timezone": str(datetime.now().astimezone().tzinfo),
                }
            }
            return sys_intel
        except Exception as e:
            LOG.error(f"System intelligence failed: {e}")
            return {"error": f"System intelligence unavailable: {e}"}
    
    @staticmethod
    def _get_hardware_forensics() -> dict:
        """Advanced hardware intelligence with forensic details"""
        if not PSUTIL_AVAILABLE:
            return {"error": "psutil required - pip install psutil"}
        
        try:
            hw_forensics = {
                "cpu_forensics": AvancedSystemInfo._get_cpu_forensics(),
                "memory_forensics": AvancedSystemInfo._get_memory_forensics(),
                "storage_forensics": AvancedSystemInfo._get_storage_forensics(),
                "hardware_components": AvancedSystemInfo._get_hardware_components(),
            }
            return hw_forensics
        except Exception as e:
            LOG.error(f"Hardware forensics failed: {e}")
            return {"error": f"Hardware forensics unavailable: {e}"}
    
    @staticmethod
    def _get_cpu_forensics() -> dict:
        """Advanced CPU forensic information"""
        try:
            cpu_info = {
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_cores": psutil.cpu_count(logical=True),
                "current_usage": f"{psutil.cpu_percent(interval=0.5)}%",
                "per_core_usage": [f"{percent}%" for percent in psutil.cpu_percent(interval=0.5, percpu=True)],
                "cpu_times": dict(psutil.cpu_times()._asdict()),
            }
            
            # Enhanced CPU info
            try:
                freq = psutil.cpu_freq()
                if freq:
                    cpu_info.update({
                        "current_frequency": f"{freq.current:.1f} MHz",
                        "min_frequency": f"{freq.min:.1f} MHz" if freq.min else "N/A",
                        "max_frequency": f"{freq.max:.1f} MHz" if freq.max else "N/A",
                    })
            except:
                cpu_info["frequency_info"] = "Unavailable"
            
            # CPU stats
            try:
                cpu_stats = psutil.cpu_stats()
                cpu_info.update({
                    "ctx_switches": cpu_stats.ctx_switches,
                    "interrupts": cpu_stats.interrupts,
                    "soft_interrupts": cpu_stats.soft_interrupts,
                    "syscalls": cpu_stats.syscalls,
                })
            except:
                cpu_info["cpu_stats"] = "Unavailable"
            
            return cpu_info
            
        except Exception as e:
            return {"error": f"CPU forensics failed: {e}"}
    
    @staticmethod
    def _get_memory_forensics() -> dict:
        """Advanced memory forensic information"""
        try:
            memory = psutil.virtual_memory()
            mem_info = {
                "total": f"{memory.total // (1024**3)} GB",
                "available": f"{memory.available // (1024**3)} GB",
                "used": f"{memory.used // (1024**3)} GB",
                "usage_percent": f"{memory.percent}%",
                "active": f"{getattr(memory, 'active', 'N/A')}",
                "inactive": f"{getattr(memory, 'inactive', 'N/A')}",
                "cached": f"{getattr(memory, 'cached', 'N/A')}",
            }
            
            # Swap memory with enhanced error handling
            try:
                swap = psutil.swap_memory()
                mem_info.update({
                    "swap_total": f"{swap.total // (1024**3)} GB",
                    "swap_used": f"{swap.used // (1024**3)} GB",
                    "swap_free": f"{swap.free // (1024**3)} GB",
                    "swap_percent": f"{swap.percent}%",
                })
            except Exception as e:
                mem_info["swap_info"] = f"Unavailable: {e}"
            
            return mem_info
            
        except Exception as e:
            return {"error": f"Memory forensics failed: {e}"}
    
    @staticmethod
    def _get_storage_forensics() -> dict:
        """Advanced storage forensic information"""
        try:
            storage_info = {
                "partitions": [],
                "io_counters": {},
                "disk_usage_details": []
            }
            
            # Partition information
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    partition_info = {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "opts": partition.opts,
                        "total_size": f"{usage.total // (1024**3)} GB",
                        "used": f"{usage.used // (1024**3)} GB",
                        "free": f"{usage.free // (1024**3)} GB",
                        "usage_percent": f"{usage.percent}%",
                    }
                    storage_info["partitions"].append(partition_info)
                except (PermissionError, OSError) as e:
                    partition_info = {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "error": f"Access denied: {e}"
                    }
                    storage_info["partitions"].append(partition_info)
                except Exception as e:
                    LOG.warning(f"Partition {partition.mountpoint} failed: {e}")
            
            # Disk I/O counters
            try:
                disk_io = psutil.disk_io_counters()
                if disk_io:
                    storage_info["io_counters"] = {
                        "read_count": disk_io.read_count,
                        "write_count": disk_io.write_count,
                        "read_bytes": f"{disk_io.read_bytes // (1024**2)} MB",
                        "write_bytes": f"{disk_io.write_bytes // (1024**2)} MB",
                        "read_time": f"{disk_io.read_time} ms",
                        "write_time": f"{disk_io.write_time} ms",
                    }
            except Exception as e:
                storage_info["io_counters"] = {"error": f"Unavailable: {e}"}
            
            return storage_info
            
        except Exception as e:
            return {"error": f"Storage forensics failed: {e}"}
    
    @staticmethod
    def _get_hardware_components() -> dict:
        """Additional hardware component information"""
        try:
            components = {
                "sensors": AvancedSystemInfo._get_sensor_info(),
                "battery": AvancedSystemInfo._get_battery_info(),
            }
            return components
        except Exception as e:
            return {"error": f"Hardware components failed: {e}"}
    
    @staticmethod
    def _get_sensor_info() -> dict:
        """System sensor information"""
        try:
            sensors = {}
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                for name, entries in temps.items():
                    sensors[name] = [entry._asdict() for entry in entries]
            
            if hasattr(psutil, "sensors_fans"):
                fans = psutil.sensors_fans()
                for name, entries in fans.items():
                    sensors[name] = [entry._asdict() for entry in entries]
            
            if hasattr(psutil, "sensors_battery"):
                battery = psutil.sensors_battery()
                if battery:
                    sensors["battery"] = battery._asdict()
            
            return sensors if sensors else {"message": "No sensor data available"}
        except:
            return {"error": "Sensor information unavailable"}
    
    @staticmethod
    def _get_battery_info() -> dict:
        """Battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": f"{battery.percent}%",
                    "power_plugged": battery.power_plugged,
                    "secsleft": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited",
                }
            return {"message": "No battery available"}
        except:
            return {"error": "Battery information unavailable"}
    
    @staticmethod
    def _get_network_intelligence() -> dict:
        """Advanced network intelligence gathering"""
        try:
            net_intel = {
                "public_network": AvancedSystemInfo._get_public_network_info(),
                "local_network": AvancedSystemInfo._get_local_network_info(),
                "network_interfaces": AvancedSystemInfo._get_network_interfaces(),
                "connections": AvancedSystemInfo._get_enhanced_connections(),
                "dns_info": AvancedSystemInfo._get_dns_info(),
                "routing_table": AvancedSystemInfo._get_routing_table(),
            }
            return net_intel
        except Exception as e:
            LOG.error(f"Network intelligence failed: {e}")
            return {"error": f"Network intelligence unavailable: {e}"}
    
    @staticmethod
    def _get_public_network_info() -> dict:
        """Enhanced public IP and geolocation information"""
        public_ip, geo_info = AvancedSystemInfo._get_public_ip_and_geo()
        
        public_net = {
            "public_ip": public_ip,
            "geolocation": geo_info,
            "hostname": socket.getfqdn(),
        }
        
        return public_net
    
    @staticmethod
    def _get_public_ip_and_geo() -> Tuple[Optional[str], Optional[Dict]]:
        """Get public IP and geolocation with multiple fallbacks"""
        for url in PUBLIC_IP_SERVICES:
            try:
                response = requests.get(url, timeout=5, verify=True)
                response.raise_for_status()
                
                if response.headers.get("content-type", "").startswith("application/json"):
                    ip = response.json().get("ip", "").strip()
                else:
                    ip = response.text.strip()
                
                if ip:
                    # Get geolocation
                    try:
                        geo_response = requests.get(GEO_IP_SERVICE.format(ip=ip), timeout=3)
                        if geo_response.status_code == 200:
                            geo_info = geo_response.json()
                            return ip, geo_info
                    except:
                        return ip, None
                    
            except Exception:
                continue
        
        return None, None
    
    @staticmethod
    def _get_local_network_info() -> dict:
        """Enhanced local network information"""
        try:
            local_ips = {}
            mac_addresses = {}
            default_gateway = None
            
            # Network interfaces
            for interface, addrs in psutil.net_if_addrs().items():
                interface_ips = []
                for addr in addrs:
                    if addr.family in (socket.AF_INET, socket.AF_INET6):
                        interface_ips.append(addr.address)
                    elif addr.family == psutil.AF_LINK:
                        mac_addresses[interface] = addr.address
                
                if interface_ips:
                    local_ips[interface] = interface_ips
            
            # Default gateway
            try:
                gateways = psutil.net_if_stats()
                # Get default gateway using socket
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                default_gateway = '.'.join(local_ip.split('.')[:-1] + ['1'])  # Simple heuristic
            except:
                pass
            
            local_net = {
                "local_ip_addresses": local_ips,
                "mac_addresses": mac_addresses,
                "default_gateway": default_gateway,
            }
            
            return local_net
            
        except Exception as e:
            return {"error": f"Local network info failed: {e}"}
    
    @staticmethod
    def _get_network_interfaces() -> dict:
        """Detailed network interface information"""
        try:
            interfaces = {}
            
            for interface, stats in psutil.net_if_stats().items():
                interfaces[interface] = {
                    "is_up": stats.isup,
                    "duplex": stats.duplex,
                    "speed": f"{stats.speed} Mbps" if stats.speed else "Unknown",
                    "mtu": stats.mtu,
                }
            
            # Interface addresses
            for interface, addrs in psutil.net_if_addrs().items():
                if interface not in interfaces:
                    interfaces[interface] = {}
                
                addr_info = []
                for addr in addrs:
                    addr_info.append({
                        "family": "IPv4" if addr.family == socket.AF_INET else 
                                 "IPv6" if addr.family == socket.AF_INET6 else 
                                 "MAC" if addr.family == psutil.AF_LINK else "Other",
                        "address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast": addr.broadcast,
                    })
                
                interfaces[interface]["addresses"] = addr_info
            
            return interfaces
            
        except Exception as e:
            return {"error": f"Network interfaces failed: {e}"}
    
    @staticmethod
    def _get_enhanced_connections() -> dict:
        """Enhanced network connections information"""
        try:
            connections = {
                "tcp_connections": [],
                "udp_connections": [],
                "listening_ports": [],
            }
            
            if not PSUTIL_AVAILABLE:
                return {"error": "psutil required for connection details"}
            
            # TCP connections
            for conn in psutil.net_connections(kind='tcp'):
                try:
                    conn_info = {
                        "family": "IPv4" if conn.family == socket.AF_INET else "IPv6",
                        "type": "TCP",
                        "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
                        "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        "status": conn.status,
                        "pid": conn.pid,
                    }
                    
                    if conn.status == 'LISTEN':
                        connections["listening_ports"].append(conn_info)
                    else:
                        connections["tcp_connections"].append(conn_info)
                        
                except Exception as e:
                    continue
            
            # UDP connections
            for conn in psutil.net_connections(kind='udp'):
                try:
                    conn_info = {
                        "family": "IPv4" if conn.family == socket.AF_INET else "IPv6",
                        "type": "UDP",
                        "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
                        "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        "pid": conn.pid,
                    }
                    connections["udp_connections"].append(conn_info)
                except Exception as e:
                    continue
            
            return connections
            
        except Exception as e:
            return {"error": f"Enhanced connections failed: {e}"}
    
    @staticmethod
    def _get_dns_info() -> dict:
        """DNS configuration information"""
        try:
            dns_info = {
                "hostname": socket.gethostname(),
                "fqdn": socket.getfqdn(),
                "dns_servers": [],
            }
            
            # Try to get DNS servers (platform specific)
            if platform.system() == "Windows":
                try:
                    import subprocess
                    result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
                    lines = result.stdout.split('\n')
                    dns_servers = []
                    for line in lines:
                        if 'DNS Servers' in line:
                            parts = line.split(':')
                            if len(parts) > 1:
                                dns_servers.append(parts[1].strip())
                    dns_info["dns_servers"] = dns_servers
                except:
                    pass
            
            return dns_info
        except Exception as e:
            return {"error": f"DNS info failed: {e}"}
    
    @staticmethod
    def _get_routing_table() -> list:
        """System routing table"""
        try:
            routes = []
            if platform.system() == "Windows":
                try:
                    result = subprocess.run(['route', 'print'], capture_output=True, text=True)
                    lines = result.stdout.split('\n')
                    # Parse route table (simplified)
                    for line in lines:
                        if line.strip() and not line.startswith('='):
                            parts = line.split()
                            if len(parts) >= 5 and parts[0] != 'Network':
                                route_info = {
                                    "destination": parts[0],
                                    "netmask": parts[1],
                                    "gateway": parts[2],
                                    "interface": parts[3],
                                    "metric": parts[4] if len(parts) > 4 else "N/A",
                                }
                                routes.append(route_info)
                except:
                    pass
            return routes
        except Exception as e:
            return [{"error": f"Routing table failed: {e}"}]
    
    @staticmethod
    def _get_user_forensics() -> dict:
        """Enhanced user activity and forensic information"""
        try:
            user_forensics = {
                "user_sessions": AvancedSystemInfo._get_user_sessions(),
                "recent_activity": AvancedSystemInfo._get_enhanced_recent_files(),
                "user_environment": AvancedSystemInfo._get_user_environment(),
                "login_history": AvancedSystemInfo._get_login_history(),
            }
            return user_forensics
        except Exception as e:
            return {"error": f"User forensics failed: {e}"}
    
    @staticmethod
    def _get_user_sessions() -> list:
        """Get user session information"""
        try:
            sessions = []
            if PSUTIL_AVAILABLE:
                users = psutil.users()
                for user in users:
                    session_info = {
                        "username": user.name,
                        "terminal": user.terminal,
                        "host": user.host,
                        "started": datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M:%S'),
                        "pid": user.pid,
                    }
                    sessions.append(session_info)
            return sessions
        except:
            return []
    
    @staticmethod
    def _get_enhanced_recent_files() -> dict:
        """Enhanced recent files tracking"""
        try:
            recent_data = {
                "windows_recent": AvancedSystemInfo._get_windows_recent_files(),
                "downloads": AvancedSystemInfo._get_downloads_folder(),
                "desktop_files": AvancedSystemInfo._get_desktop_files(),
            }
            return recent_data
        except Exception as e:
            return {"error": f"Recent files failed: {e}"}
    
    @staticmethod
    def _get_windows_recent_files() -> list:
        """Windows recent files with enhanced details"""
        try:
            recent_files = []
            recent_dir = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Recent"
            
            if recent_dir.exists():
                for file in recent_dir.glob("*.*"):
                    try:
                        if file.stat().st_size < 50 * 1024 * 1024:  # 50MB limit
                            file_info = {
                                "filename": file.name,
                                "path": str(file),
                                "size": file.stat().st_size,
                                "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                                "created": datetime.fromtimestamp(file.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                                "accessed": datetime.fromtimestamp(file.stat().st_atime).strftime('%Y-%m-%d %H:%M:%S'),
                                "extension": file.suffix.lower(),
                            }
                            recent_files.append(file_info)
                    except:
                        continue
            
            return sorted(recent_files, key=lambda x: x["modified"], reverse=True)[:25]
        except:
            return []
    
    @staticmethod
    def _get_downloads_folder() -> list:
        """Recent downloads"""
        try:
            downloads = []
            downloads_dir = Path.home() / "Downloads"
            
            if downloads_dir.exists():
                for file in downloads_dir.iterdir():
                    try:
                        if file.is_file():
                            file_info = {
                                "filename": file.name,
                                "size": file.stat().st_size,
                                "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                                "extension": file.suffix.lower(),
                            }
                            downloads.append(file_info)
                    except:
                        continue
            
            return sorted(downloads, key=lambda x: x["modified"], reverse=True)[:15]
        except:
            return []
    
    @staticmethod
    def _get_desktop_files() -> list:
        """Desktop files"""
        try:
            desktop_files = []
            desktop_dir = Path.home() / "Desktop"
            
            if desktop_dir.exists():
                for file in desktop_dir.iterdir():
                    try:
                        if file.is_file():
                            file_info = {
                                "filename": file.name,
                                "size": file.stat().st_size,
                                "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                                "extension": file.suffix.lower(),
                            }
                            desktop_files.append(file_info)
                    except:
                        continue
            
            return desktop_files
        except:
            return []
    
    @staticmethod
    def _get_user_environment() -> dict:
        """User environment with security filtering"""
        try:
            env_vars = {}
            sensitive_keywords = ['pass', 'key', 'secret', 'token', 'pwd', 'auth', 'cred']
            
            for key, value in os.environ.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keywords):
                    env_vars[key] = "🔒 REDACTED"
                else:
                    env_vars[key] = value
            
            return {
                "environment_variables": env_vars,
                "current_directory": os.getcwd(),
                "home_directory": str(Path.home()),
                "temp_directory": os.environ.get('TEMP', 'N/A'),
            }
        except Exception as e:
            return {"error": f"User environment failed: {e}"}
    
    @staticmethod
    def _get_login_history() -> list:
        """User login history (simplified)"""
        try:
            history = []
            if PSUTIL_AVAILABLE:
                boot_time = psutil.boot_time()
                history.append({
                    "event": "System Boot",
                    "timestamp": datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S'),
                })
            return history
        except:
            return []
    
    @staticmethod
    def _get_security_posture() -> dict:
        """Enhanced security posture assessment"""
        try:
            security = {
                "privilege_analysis": AvancedSystemInfo._get_privilege_analysis(),
                "firewall_status": AvancedSystemInfo._get_enhanced_firewall_status(),
                "uac_status": AvancedSystemInfo._get_enhanced_uac_status(),
                "antivirus_status": AvancedSystemInfo._get_antivirus_status(),
                "system_updates": AvancedSystemInfo._get_update_status(),
            }
            return security
        except Exception as e:
            return {"error": f"Security posture failed: {e}"}
    
    @staticmethod
    def _get_privilege_analysis() -> dict:
        """Detailed privilege analysis"""
        return {
            "admin_privileges": AvancedSystemInfo._has_admin_privileges(),
            "integrity_level": AvancedSystemInfo._get_integrity_level(),
            "user_groups": AvancedSystemInfo._get_user_groups(),
        }
    
    @staticmethod
    def _has_admin_privileges() -> bool:
        """Check admin privileges"""
        try:
            if platform.system() == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except:
            return False
    
    @staticmethod
    def _get_integrity_level() -> str:
        """Get Windows integrity level (simplified)"""
        try:
            if platform.system() == "Windows":
                if AvancedSystemInfo._has_admin_privileges():
                    return "High (Admin)"
                else:
                    return "Medium (User)"
            return "N/A (Non-Windows)"
        except:
            return "Unknown"
    
    @staticmethod
    def _get_user_groups() -> list:
        """Get user groups (simplified)"""
        try:
            import grp
            groups = []
            for group in grp.getgrall():
                if getpass.getuser() in group.gr_mem:
                    groups.append(group.gr_name)
            return groups
        except:
            return ["Group information unavailable"]
    
    @staticmethod
    def _get_enhanced_firewall_status() -> dict:
        """Enhanced firewall status checking"""
        try:
            if platform.system() == "Windows":
                try:
                    result = subprocess.run(
                        ['netsh', 'advfirewall', 'show', 'allprofiles'], 
                        capture_output=True, text=True, timeout=10
                    )
                    return {
                        "status": "Windows Firewall details available",
                        "raw_output": result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout
                    }
                except:
                    return {"status": "Windows Firewall - Unable to query"}
            elif platform.system() == "Linux":
                try:
                    # Check iptables
                    result = subprocess.run(['iptables', '-L'], capture_output=True, text=True)
                    return {
                        "status": "iptables configured" if result.stdout.strip() else "No iptables rules",
                        "type": "iptables"
                    }
                except:
                    return {"status": "Firewall status unknown"}
            else:
                return {"status": "Platform specific check required"}
        except Exception as e:
            return {"error": f"Firewall check failed: {e}"}
    
    @staticmethod
    def _get_enhanced_uac_status() -> dict:
        """Enhanced UAC status checking"""
        try:
            if platform.system() == "Windows":
                try:
                    import winreg
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                      r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System") as key:
                        try:
                            uac_value = winreg.QueryValueEx(key, "EnableLUA")[0]
                            return {
                                "uac_enabled": uac_value == 1,
                                "level": "Enabled" if uac_value == 1 else "Disabled"
                            }
                        except FileNotFoundError:
                            return {"uac_enabled": False, "level": "Disabled (Registry key not found)"}
                except Exception as e:
                    return {"error": f"UAC registry query failed: {e}"}
            return {"status": "UAC is a Windows-only feature"}
        except Exception as e:
            return {"error": f"UAC check failed: {e}"}
    
    @staticmethod
    def _get_antivirus_status() -> dict:
        """Antivirus status detection"""
        av_products = AvancedSystemInfo._get_security_products()
        return {
            "detected_products": av_products,
            "count": len(av_products),
            "status": "Protected" if av_products else "No AV detected"
        }
    
    @staticmethod
    def _get_update_status() -> dict:
        """System update status (simplified)"""
        return {
            "last_boot": AvancedSystemInfo._get_enhanced_boot_time(),
            "system_uptime": AvancedSystemInfo._get_enhanced_uptime(),
            "update_status": "Manual check required for detailed update info"
        }
    
    @staticmethod
    def _get_process_forensics() -> dict:
        """Enhanced process forensic analysis"""
        try:
            processes = AvancedSystemInfo._get_enhanced_process_list()
            return {
                "total_processes": len(processes),
                "process_list": processes[:50],  # Limit for readability
                "suspicious_indicators": AvancedSystemInfo._analyze_processes(processes),
            }
        except Exception as e:
            return {"error": f"Process forensics failed: {e}"}
    
    @staticmethod
    def _get_enhanced_process_list() -> list:
        """Enhanced process listing with detailed information"""
        try:
            if not PSUTIL_AVAILABLE:
                return [{"error": "psutil required for process details"}]
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent', 'cpu_percent', 'create_time', 'status']):
                try:
                    process_info = proc.info
                    process_info['create_time'] = datetime.fromtimestamp(process_info['create_time']).strftime('%Y-%m-%d %H:%M:%S') if process_info['create_time'] else 'N/A'
                    process_info['memory_mb'] = f"{proc.memory_info().rss // 1024 // 1024} MB"
                    
                    # Get command line if available
                    try:
                        process_info['cmdline'] = ' '.join(proc.cmdline()) if proc.cmdline() else 'N/A'
                    except:
                        process_info['cmdline'] = 'Access denied'
                    
                    processes.append(process_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return sorted(processes, key=lambda x: x.get('memory_percent', 0), reverse=True)
            
        except Exception as e:
            return [{"error": f"Process listing failed: {e}"}]
    
    @staticmethod
    def _analyze_processes(processes: list) -> dict:
        """Analyze processes for suspicious indicators"""
        suspicious_keywords = ['mimikatz', 'bloodhound', 'metasploit', 'cobalt', 'empire', 'invoke-']
        suspicious_extensions = ['.exe', '.dll', '.scr', '.com']
        
        analysis = {
            "suspicious_names": [],
            "high_memory_usage": [],
            "high_cpu_usage": [],
        }
        
        for proc in processes:
            try:
                name = proc.get('name', '').lower()
                cmdline = proc.get('cmdline', '').lower()
                
                # Check for suspicious keywords
                if any(keyword in name or keyword in cmdline for keyword in suspicious_keywords):
                    analysis["suspicious_names"].append({
                        "pid": proc.get('pid'),
                        "name": proc.get('name'),
                        "reason": "Known offensive tool"
                    })
                
                # High memory usage
                if proc.get('memory_percent', 0) > 10.0:
                    analysis["high_memory_usage"].append({
                        "pid": proc.get('pid'),
                        "name": proc.get('name'),
                        "memory_percent": proc.get('memory_percent')
                    })
                
                # High CPU usage
                if proc.get('cpu_percent', 0) > 20.0:
                    analysis["high_cpu_usage"].append({
                        "pid": proc.get('pid'),
                        "name": proc.get('name'),
                        "cpu_percent": proc.get('cpu_percent')
                    })
                    
            except:
                continue
        
        return analysis
    
    @staticmethod
    def _get_software_inventory() -> dict:
        """Enhanced software inventory"""
        try:
            software = {
                "installed_programs": AvancedSystemInfo._get_enhanced_installed_software(),
                "running_services": AvancedSystemInfo._get_services(),
                "browser_extensions": AvancedSystemInfo._get_browser_extensions(),
            }
            return software
        except Exception as e:
            return {"error": f"Software inventory failed: {e}"}
    
    @staticmethod
    def _get_enhanced_installed_software() -> list:
        """Enhanced installed software detection"""
        software_list = []
        
        try:
            # Common installation directories
            install_dirs = [
                Path("C:/Program Files"),
                Path("C:/Program Files (x86)"),
                Path.home() / "AppData" / "Local" / "Programs",
            ]
            
            for install_dir in install_dirs:
                if install_dir.exists():
                    try:
                        for item in install_dir.iterdir():
                            if item.is_dir():
                                software_info = {
                                    "name": item.name,
                                    "path": str(item),
                                    "type": "Program",
                                    "size": "N/A",
                                    "modified": datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S') if item.exists() else "N/A",
                                }
                                
                                # Try to get size
                                try:
                                    total_size = 0
                                    for file in item.rglob('*'):
                                        if file.is_file():
                                            total_size += file.stat().st_size
                                    software_info["size"] = f"{total_size // (1024**2)} MB"
                                except:
                                    software_info["size"] = "Access denied"
                                
                                software_list.append(software_info)
                    except:
                        continue
            
            return sorted(software_list, key=lambda x: x["name"])[:100]  # Limit to 100
            
        except Exception as e:
            return [{"error": f"Software enumeration failed: {e}"}]
    
    @staticmethod
    def _get_services() -> list:
        """Get system services"""
        try:
            if not PSUTIL_AVAILABLE:
                return []
            
            services = []
            for service in psutil.win_service_iter() if platform.system() == "Windows" and hasattr(psutil, 'win_service_iter') else []:
                try:
                    service_info = {
                        "name": service.name(),
                        "display_name": service.display_name(),
                        "status": service.status(),
                        "binpath": service.binpath() if hasattr(service, 'binpath') else "N/A",
                    }
                    services.append(service_info)
                except:
                    continue
            
            return services
        except:
            return []
    
    @staticmethod
    def _get_browser_extensions() -> dict:
        """Browser extensions (simplified)"""
        return {
            "chrome": "Manual inspection required",
            "firefox": "Manual inspection required", 
            "edge": "Manual inspection required",
            "note": "Browser extension analysis requires direct database access"
        }
    
    @staticmethod
    def _get_browser_forensics() -> dict:
        """Enhanced browser forensic information"""
        try:
            browsers = AvancedSystemInfo._get_browser_detection()
            return {
                "detected_browsers": browsers,
                "forensic_artifacts": AvancedSystemInfo._get_browser_artifacts(),
            }
        except Exception as e:
            return {"error": f"Browser forensics failed: {e}"}
    
    @staticmethod
    def _get_browser_detection() -> dict:
        """Detect installed browsers"""
        browsers = {}
        browser_paths = {
            "Chrome": Path.home() / "AppData/Local/Google/Chrome",
            "Firefox": Path.home() / "AppData/Roaming/Mozilla/Firefox",
            "Edge": Path.home() / "AppData/Local/Microsoft/Edge",
            "Opera": Path.home() / "AppData/Roaming/Opera Software",
            "Brave": Path.home() / "AppData/Local/BraveSoftware/Brave-Browser",
        }
        
        for browser, path in browser_paths.items():
            browsers[browser] = {
                "installed": path.exists(),
                "profile_path": str(path) if path.exists() else "Not found",
            }
        
        return browsers
    
    @staticmethod
    def _get_browser_artifacts() -> dict:
        """Browser forensic artifacts"""
        return {
            "history": "Requires direct database parsing",
            "cookies": "Requires decryption and parsing", 
            "passwords": "Requires master key decryption",
            "downloads": "Available in browser profile folders",
            "sessions": "Session restoration data",
            "note": "Advanced browser forensics requires specialized tools"
        }
    
    @staticmethod
    def _get_system_artifacts() -> dict:
        """System forensic artifacts"""
        try:
            artifacts = {
                "event_logs": AvancedSystemInfo._get_enhanced_event_logs(),
                "prefetch_files": AvancedSystemInfo._get_prefetch_files(),
                "system_logs": AvancedSystemInfo._get_system_logs(),
                "registry_artifacts": AvancedSystemInfo._get_registry_artifacts(),
            }
            return artifacts
        except Exception as e:
            return {"error": f"System artifacts failed: {e}"}
    
    @staticmethod
    def _get_enhanced_event_logs() -> list:
        """Enhanced Windows event log information"""
        try:
            if platform.system() != "Windows":
                return [{"note": "Event logs are Windows-specific"}]
            
            import subprocess
            result = subprocess.run(['wevtutil', 'el'], capture_output=True, text=True, timeout=10)
            event_logs = []
            
            for log_name in result.stdout.split('\n'):
                log_name = log_name.strip()
                if log_name:
                    event_logs.append(log_name)
            
            return event_logs[:20]  # Limit to 20 logs
            
        except Exception as e:
            return [{"error": f"Event logs unavailable: {e}"}]
    
    @staticmethod
    def _get_prefetch_files() -> list:
        """Windows prefetch files"""
        try:
            prefetch_files = []
            prefetch_dir = Path("C:/Windows/Prefetch")
            
            if prefetch_dir.exists():
                for file in prefetch_dir.glob("*.pf"):
                    try:
                        if file.stat().st_size < 5 * 1024 * 1024:  # 5MB limit
                            prefetch_files.append({
                                "filename": file.name,
                                "size": file.stat().st_size,
                                "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                            })
                    except:
                        continue
            
            return sorted(prefetch_files, key=lambda x: x["modified"], reverse=True)[:15]
        except:
            return []
    
    @staticmethod
    def _get_system_logs() -> list:
        """System log files"""
        try:
            system_logs = []
            log_locations = [
                Path("C:/Windows/Logs"),
                Path("C:/Windows/System32/winevt/Logs"),
                Path.home() / "AppData/Local/Temp",
            ]
            
            for location in log_locations:
                if location.exists():
                    try:
                        for log_file in location.rglob("*.log"):
                            try:
                                if log_file.stat().st_size < 10 * 1024 * 1024:  # 10MB limit
                                    system_logs.append({
                                        "path": str(log_file),
                                        "size": log_file.stat().st_size,
                                        "modified": datetime.fromtimestamp(log_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                                    })
                            except:
                                continue
                    except:
                        continue
            
            return sorted(system_logs, key=lambda x: x["modified"], reverse=True)[:20]
        except:
            return []
    
    @staticmethod
    def _get_registry_artifacts() -> dict:
        """Registry forensic artifacts"""
        return {
            "run_keys": "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            "run_once": "HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce", 
            "user_assist": "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist",
            "note": "Registry analysis requires direct registry access"
        }
    
    @staticmethod
    def _get_threat_indicators() -> dict:
        """System threat indicators"""
        try:
            indicators = {
                "suspicious_processes": AvancedSystemInfo._get_suspicious_processes(),
                "network_anomalies": AvancedSystemInfo._get_network_anomalies(),
                "persistence_mechanisms": AvancedSystemInfo._get_persistence_indicators(),
            }
            return indicators
        except Exception as e:
            return {"error": f"Threat indicators failed: {e}"}
    
    @staticmethod
    def _get_suspicious_processes() -> list:
        """Detect suspicious processes"""
        suspicious = []
        known_suspicious = ['mimikatz', 'powersploit', 'metasploit', 'cobaltstrike', 'empire']
        
        try:
            if PSUTIL_AVAILABLE:
                for proc in psutil.process_iter(['name']):
                    try:
                        proc_name = proc.info['name'].lower()
                        if any(susp in proc_name for susp in known_suspicious):
                            suspicious.append({
                                "process": proc_name,
                                "pid": proc.pid,
                                "risk_level": "HIGH"
                            })
                    except:
                        continue
        except:
            pass
        
        return suspicious
    
    @staticmethod
    def _get_network_anomalies() -> list:
        """Network connection anomalies"""
        anomalies = []
        
        try:
            if PSUTIL_AVAILABLE:
                for conn in psutil.net_connections():
                    try:
                        # Check for unusual listening ports
                        if conn.status == 'LISTEN' and conn.laddr:
                            port = conn.laddr.port
                            if port > 49151:  # Ephemeral ports
                                anomalies.append({
                                    "type": "High port listening",
                                    "port": port,
                                    "pid": conn.pid,
                                    "risk": "MEDIUM"
                                })
                    except:
                        continue
        except:
            pass
        
        return anomalies
    
    @staticmethod
    def _get_persistence_indicators() -> list:
        """Persistence mechanism indicators"""
        return [
            "Scheduled Tasks",
            "Windows Services", 
            "Registry Run Keys",
            "Startup Folder",
            "Browser Extensions",
            "WMI Event Subscriptions"
        ]
    
    @staticmethod
    def _get_security_products() -> list:
        """Enhanced security product detection"""
        try:
            security_products = []
            security_keywords = [
                'avast', 'avg', 'bitdefender', 'kaspersky', 'norton', 
                'mcafee', 'eset', 'malware', 'security', 'antivirus',
                'defender', 'firewall', 'crowdstrike', 'sentinel', 'sophos'
            ]
            
            # Check common security directories
            security_dirs = [
                Path("C:/Program Files"),
                Path("C:/Program Files (x86)"),
            ]
            
            for security_dir in security_dirs:
                if security_dir.exists():
                    try:
                        for item in security_dir.iterdir():
                            if any(keyword in item.name.lower() for keyword in security_keywords):
                                security_products.append({
                                    "name": item.name,
                                    "path": str(item),
                                    "type": "Security Product"
                                })
                    except:
                        continue
            
            return list({product['name']: product for product in security_products}.values())  # Remove duplicates
            
        except Exception as e:
            return [{"error": f"Security products detection failed: {e}"}]
    
    @staticmethod
    def _get_enhanced_uptime() -> str:
        """Enhanced system uptime calculation"""
        try:
            if PSUTIL_AVAILABLE:
                boot_time = psutil.boot_time()
                uptime_seconds = time.time() - boot_time
                
                # Convert to readable format
                days = int(uptime_seconds // (24 * 3600))
                hours = int((uptime_seconds % (24 * 3600)) // 3600)
                minutes = int((uptime_seconds % 3600) // 60)
                seconds = int(uptime_seconds % 60)
                
                return f"{days}d {hours}h {minutes}m {seconds}s"
            return "psutil required for uptime"
        except:
            return "Unable to determine"
    
    @staticmethod
    def _get_enhanced_boot_time() -> str:
        """Enhanced boot time detection"""
        try:
            if PSUTIL_AVAILABLE:
                boot_time = psutil.boot_time()
                return datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')
            return "psutil required for boot time"
        except:
            return "Unable to determine"


# Usage Example
if __name__ == "__main__":
    # Test both interfaces
    print("🛡️  Testing SystemInfo (Legacy Interface)...")
    legacy_info = SystemInfo.get_forensic_info()
    print(f"✅ Legacy interface works: {len(legacy_info)} sections")
    
    print("🛡️  Testing AdvancedSystemInfo (Enhanced Interface)...")
    enhanced_info = AvancedSystemInfo.get_forensic_info()
    print(f"✅ Enhanced interface works: {len(enhanced_info)} sections")