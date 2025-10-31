# 🛡️ Anti-Forensic Toolkit v2.0

**Advanced Digital Forensic Countermeasures & System Intelligence**

> A comprehensive Python-based toolkit for digital privacy, forensic countermeasures, and system intelligence gathering. Built with security professionals and red teams in mind.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)
![Version](https://img.shields.io/badge/Version-2.0-purple.svg)

## 🌟 Overview

The **Anti-Forensic Toolkit** is a powerful, feature-rich application designed to provide comprehensive digital privacy protection and forensic countermeasures. It combines military-grade file destruction capabilities with advanced system intelligence gathering in a modern, user-friendly interface.

###  Use Cases

- ** Security Professionals**: Conduct authorized penetration testing and security assessments
- ** Privacy-Conscious Users**: Protect personal data from forensic recovery  
- ** IT Administrators**: Securely decommission hardware and destroy sensitive data
- ** Digital Forensics Students**: Learn about anti-forensic techniques and countermeasures
- ** Red Teams**: Conduct operational security and clean-up activities

---

##  Features

###  Secure File Destruction
- **Multiple Wiping Algorithms**:
  -  **Simple Random**: Fast single-pass overwrite with random data
  -  **US DoD 5220.22-M**: 3-pass military standard (0x00, 0xFF, random)
  -  **Gutmann Method**: 7-pass maximum security overwrite patterns
  -  **RCMP OPS-II**: 4-pass Canadian government standard

- **Advanced Metadata Obfuscation**:
  -  Multiple secure file renames before deletion
  -  Timestamp manipulation and randomization
  -  File size and attribute obfuscation

- **Smart Safety Features**:
  -  System directory protection
  -  Python installation detection and blocking
  -  SSD detection with appropriate warnings
  -  Real-time progress monitoring with cancellation

###  Comprehensive System Cleaning
- **Browser Data Removal**:
  -  Chrome, Firefox, Edge, Opera, Brave cache and temporary files
  -  Complete browser profile cleaning
  -  Session data and cookie removal

- **System Artifact Cleaning**:
  -  Windows Event Log clearing (with admin privileges)
  -  Temporary file directory cleaning
  -  Recent documents history removal
  -  DNS cache flushing

- **Free Space Wiping**:
  -  Secure overwrite of deleted file remnants
  -  Configurable pass count (1-3 passes)
  -  Progress tracking with estimated time remaining

###  Advanced System Intelligence
- **Hardware Forensics**:
  -  Complete system specifications
  -  CPU, memory, and storage detailed analysis
  -  Sensor data and battery information
  -  Performance metrics and usage statistics

- **Network Intelligence**:
  -  Public IP detection with geolocation
  -  Local network interface analysis
  -  Active connections and listening ports
  -  DNS configuration and routing tables

- **Security Posture Assessment**:
  -  Privilege level analysis
  -  Firewall status detection
  -  UAC/Admin rights verification
  -  Antivirus product detection

- **Threat Detection**:
  -  Suspicious process identification
  -  Network anomaly detection
  -  Persistence mechanism analysis
  -  Browser forensic artifact enumeration

###  Cryptographic Utilities
- **Multi-Algorithm Hashing**:
  -  MD5, SHA-1, SHA-256, SHA-512
  -  SHA3-256, SHA3-512
  -  BLAKE2b, BLAKE2s

- **File Integrity Verification**:
  -  Multiple hash comparison
  -  Progress-tracked large file processing
  -  Checksum validation against known values

- **Performance Benchmarking**:
  -  Algorithm speed testing
  -  Throughput measurement in MB/s
  -  Comparative performance analysis

---

##  Quick Start

### Prerequisites
- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Administrator/root privileges** (for full functionality)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SpectralZero/Anti-Forensic.git
   cd Anti-Forensic
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

###  Platform-Specific Notes

| Platform | Support Level | Key Features | Limitations |
|----------|---------------|--------------|-------------|
| **Windows 10/11** | 🟢 Full | All features supported | Admin rights needed for logs |
| **Windows 8/8.1** | 🟡 Partial | Most features | Some newer APIs unavailable |
| **Linux** | 🟡 Partial | Core functionality | Windows-specific features limited |
| **macOS** | 🟡 Partial | Basic operations | System cleaning features limited |

---

##  Project Structure

```
anti-forensic-toolkit/
│
├── 📄 main.py                 # Main application entry point
│
├── 📁 core/                   # Core functionality modules
│   ├── forensic_utilities.py  # System cleaning & wiping operations
│   ├── secure_delete.py       # File shredding algorithms & safety
│   ├── hash_calculator.py     # Cryptographic hashing utilities
│   ├── system_info.py         # System intelligence gathering
│   └── __init__.py
│
├── 📁 ui/                     # User interface components
│   ├── main_window.py         # Main application window & navigation
│   ├── shredder_dialogs.py    # Secure shredding interface
│   ├── hash_generator.py      # Hash calculator GUI
│   ├── theme.py               # Cyberpunk UI theme system
│   └── __init__.py
│
├── 📁 assets/                 # Resources and icons
│   └── icons/
│       └── .gitkeep
│
├── 📁 logs/                   # Application logs
│   └── anti_forensic_toolkit.log
│
├── 📄 requirements.txt        # Python dependencies
└── 📄 README.md              # This file
```

---

##  Usage Guide

###  Secure File Shredding

1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Access Secure Shredder**
   - Click " Secure Shredder" in the sidebar
   - Or use the quick action button on the dashboard

3. **Configure Shredding Options**
   - Select wiping algorithm based on security needs
   - Choose pass count (1-7 for files, 1-3 for free space)
   - Enable metadata obfuscation for maximum security
   - Optionally preserve garbled files for verification

4. **Execute Destruction**
   - Select files or directories for shredding
   - Confirm irreversible operation
   - Monitor real-time progress with cancellation option

###  System Intelligence Gathering

1. **Navigate to System Intel**
   - Click " System Intel" in the sidebar
   - Wait for comprehensive data collection (10-20 seconds)

2. **Explore Intelligence Tabs**:
   - **Collection Info**: Metadata about the intelligence gathering
   - **System Intel**: OS, platform, and environment details
   - **Hardware**: CPU, memory, storage, and sensor data
   - **Network Intel**: IP addresses, connections, and routing
   - **User Forensics**: Sessions, recent files, and activity
   - **Security**: Privileges, firewall, UAC, and antivirus status
   - **Process Intel**: Running processes and threat analysis
   - **Software**: Installed programs and services
   - **Browser Intel**: Detected browsers and forensic artifacts
   - **System Artifacts**: Logs, prefetch files, and registry data
   - **Threat Intel**: Suspicious indicators and anomalies

3. **Refresh Data**
   - Use " REFRESH INTEL" button for current system state
   - Data updates in real-time for dynamic system changes

###  Comprehensive System Cleaning

1. **Quick Clean Operations**
   - Access " Quick Clean" section
   - Individual operations:
     -  Clear Browser Data
     -  Clear System Logs
     -  Wipe Free Space
     -  Clear DNS Cache

2. **Full System Clean**
   - Click " FULL SYSTEM CLEAN" for comprehensive cleaning
   - Review destructive operations warning
   - Monitor progress through multiple cleaning stages
   - Restart system recommended after completion

###  Hash Generation & Verification

1. **Open Hash Generator**
   - Navigate to " Hash Generator"
   - Select desired hash algorithms
   - Choose input method: file or text

2. **Generate Hashes**
   - For files: Browse and select target file
   - For text: Enter text in provided field
   - Monitor progress for large files
   - Copy results to clipboard with " COPY ALL"

---

##  Configuration & Customization

### Algorithm Customization

Modify `core/secure_delete.py` to adjust wiping parameters:

```python
# Example: Custom wipe pattern
CUSTOM_PATTERN = [
    lambda size: b'\xDE\xAD\xBE\xEF' * (size // 4),  # Custom pattern
    lambda size: os.urandom(size),                   # Random data
    lambda size: b'\x00' * size,                     # Zero fill
]
```

### UI Theme Modification

Edit `ui/theme.py` for visual customization:

```python
# Custom color scheme
COLORS = {
    "bg_primary": "#0a0a12",
    "accent_primary": "#your_color",  # Change accent colors
    "accent_danger": "#ff4444",
    # ... additional color customizations
}
```

### Safety Configuration

Adjust safety checks in `core/forensic_utilities.py`:

```python
# Add protected directories
PROTECTED_PATHS = [
    "C:\\Windows\\",
    "C:\\Program Files\\",
    "/bin/", "/etc/", "/usr/",
    # ... custom protected paths
]
```

---

##  Security Features & Safety

### Protective Mechanisms

-  **System Path Validation**: Automatic blocking of critical system directories
-  **Python Installation Protection**: Prevents accidental deletion of Python environments
-  **Admin Privilege Detection**: Warns when operations require elevated rights
-  **SSD Awareness**: Appropriate warnings for solid-state drive limitations
-  **Real-time Cancellation**: Stop operations at any point during execution

### Forensic Countermeasures

-  **Multiple Overwrite Passes**: Renders data recovery virtually impossible
-  **File Renaming Obfuscation**: Breaks file system forensic analysis
-  **Timestamp Manipulation**: Alters creation/modification/access times
-  **Free Space Wiping**: Removes previously deleted file remnants
-  **Metadata Destruction**: Comprehensive attribute obfuscation

---

##  Important Disclaimer

### Legal and Ethical Use

**This tool is intended for:**

✅ Authorized penetration testing and security assessments  
✅ Educational purposes and security research  
✅ Personal privacy protection on owned devices  
✅ IT administration and secure data destruction  
✅ Digital forensics training and study  

**Strictly Prohibited:**

❌ Unauthorized access to systems or data  
❌ Illegal data destruction or evidence tampering  
❌ Malicious attacks on third-party systems  
❌ Circumvention of legal investigations  

### Responsibility

**Users are solely responsible for:**

- Ensuring proper authorization for all activities
- Compliance with local, state, and federal laws
- Ethical use in accordance with security best practices
- Consequences resulting from misuse or unauthorized use

> **The developers assume no liability for misuse of this software.**

---

## 🔧 Technical Specifications

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **RAM** | 2GB | 4GB |
| **Storage** | 50MB | 100MB+ |
| **Python** | 3.8+ | 3.10+ |
| **Permissions** | User-level | Admin/Root |

### Architecture Details

- **Modular Design**: Independent components for easy maintenance and updates
- **Threaded Operations**: Non-blocking UI during resource-intensive tasks
- **Progress Tracking**: Real-time feedback for all long-running operations
- **Comprehensive Logging**: Detailed audit trail of all activities
- **Error Handling**: Graceful failure recovery and user notifications

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Permission Denied Errors
```bash
# Windows: Run as Administrator
Right-click → Run as Administrator

# Linux/macOS: Use sudo
sudo python main.py
```

#### Missing Dependencies
```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt

# Check Python version
python --version
```

#### UI Rendering Problems
- Update graphics drivers
- Try different compatibility modes
- Check display scaling settings

#### Antivirus False Positives
- Add exception for application directory
- Disable real-time protection during use (temporarily)
- Use built-in Windows Defender exclusion settings

### Logs and Debugging

Check `logs/anti_forensic_toolkit.log` for:
- Detailed error messages
- Operation timestamps and durations
- System compatibility information
- Performance metrics and warnings

### Performance Optimization

**For Large File Operations:**
- Close other resource-intensive applications
- Use simpler algorithms for large datasets
- Monitor system resources during operation
- Consider operating in safe mode for critical operations

**For System Scanning:**
- The initial scan may take 10-20 seconds
- Subsequent refreshes are faster due to caching
- Network operations depend on internet connectivity

---

##  Contributing

We welcome contributions from the security community!

### Development Setup

1. **Fork the Repository**
2. **Set Up Development Environment**
   ```bash
   git clone [your-fork-url]
   cd anti-forensic-toolkit
   pip install -r requirements.txt
   ```
3. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Make Your Changes**
5. **Test Thoroughly**
6. **Submit Pull Request**

### Contribution Guidelines

- Follow PEP 8 coding standards
- Add comprehensive docstrings for new functions
- Include error handling for all operations
- Update documentation for new features
- Test on multiple platforms when possible

### Feature Requests

We're particularly interested in:
- Additional wiping algorithms
- Enhanced platform support
- New forensic countermeasures
- Performance improvements
- UI/UX enhancements

---

##  Version History

### v2.0 (Current)
- **Enhanced System Intelligence**: Comprehensive hardware, network, and security profiling
- **Advanced Threat Detection**: Suspicious process and anomaly identification
- **Modern UI**: Cyberpunk-themed interface with improved usability
- **Better Safety Features**: Enhanced path validation and system protection
- **Performance Optimizations**: Faster operations and better resource management

### v1.5
- Multiple wiping algorithm support
- Basic system cleaning capabilities
- Foundation UI framework
- Core file operations

### v1.0
- Initial release with basic file shredding
- Simple hash generation
- Basic GUI interface


---

##  Acknowledgments

- ** Author**: SpectralZero - Cyber Security Student at World Islamic Science and Education (WISE)
- ** Security Community**: For valuable feedback and testing
- ** Open Source Projects**: That inspired and enabled this toolkit
- ** Contributors**: Everyone who helped improve this project
- ** Testers**: For thorough testing across multiple platforms

---

<div align="center">

**Last Updated**: Version 2.0 | 2024

[![GitHub](https://img.shields.io/badge/GitHub-SpectralZero/Anti--Forensic-blue?style=for-the-badge&logo=github)](https://github.com/SpectralZero/Anti-Forensic)

</div>
